import pandas as pd
import numpy as np
import VisumPy.helpers as h

def log(msg):
    Visum.Log(20480, msg)

log('Reading Skims')
zones = np.array(h.GetMulti(Visum.Net.Zones, "No"))

def read_skim_tofrom_pnr(matno):
    global zones
    skim = pd.DataFrame(h.GetMatrix(Visum, matno), zones, zones)
    return {'ToPnR':   skim.loc[:60000, 90000:90300],
            'FromPnR': skim.loc[90000:90300, :60000]}

def read_skim(matno):
    global zones
    return pd.DataFrame(h.GetMatrix(Visum, matno), zones, zones)

skims= {'time': {'0000': read_skim(301),
                 '0600': read_skim(302),
                 '1000': read_skim(303),
                 '1500': read_skim(304),
                 '1900': read_skim(305)},
        'dist': {'0000': read_skim(401),
                 '0600': read_skim(402),
                 '1000': read_skim(403),
                 '1500': read_skim(404),
                 '1900': read_skim(405)}}

def get_skims(args):
    global skims
    o = args[0] #Origin
    d = args[1] #Destination
    t1 = args[2] #Time Period
    t2 = args[3]
    return (0.5*(skims['time'][t1].loc[o, d]+skims['time'][t2].loc[o, d]),
            0.5*(skims['dist'][t1].loc[o, d]+skims['dist'][t2].loc[o, d]))

def classify_time(t):
    if t < 360:
        return '0000'
    elif t < 600:
        return '0600'
    elif t < 900:
        return '1000'
    elif t < 1140:
        return '1500'
    else:
        return '1900'

log('Reading Trip Data')
trip_file = r'D:\TIM3.1\DaySimLab\scenario\Output\05201612\_tour_2.dat'
trip = pd.read_csv(trip_file, '\t')

#log('Reading Tour Data')
#tour_file = trip_file.replace('trip', 'tour')
#tour = pd.read_csv(tour_file, '\t')

log('Merging and Querying')
#trip = tour.merge(trip, on = ['hhno', 'pno', 'day', 'tour']) #Merge tour info to trip info
#trip = trip.query('(opurp != 0 or dpurp != 10) and (opurp != 10 or dpurp != 0)') #From home to PnR or vice-versa
#trip = trip.query('opurp != 10 and dpurp != 10')

log('Setting Up Table')
#trip['direction'] = np.where(trip['dpurp'] == 10, 'ToPnR', 'FromPnR')
#trip['tod_args'] = list(zip(trip['tardest'], trip['tlvorig'], np.ones_like(trip.index)))
trip['tod1'] = trip['tardest'].apply(classify_time)
trip['tod2'] = trip['tlvdest'].apply(classify_time)

log('Getting Skim Values')
trip['skim_args'] = list(zip(trip['totaz'], trip['tdtaz'], trip['tod1'], trip['tod2']))
trip['skims'] = trip['skim_args'].apply(get_skims)
trip['skimtime'] = trip['skims'].apply(lambda x: x[0])
trip['skimdist'] = trip['skims'].apply(lambda x: x[1])

log('Comparing')
trip['timediff'] = trip['skimtime'] - trip['tautotime']
trip['distdiff'] = trip['skimdist'] - trip['tautodist']

log('Writing')
outfile = r'D:\TIM3\ToursWithVISUMSkimsAvg.csv'
trip.to_csv(outfile)

log('Done')