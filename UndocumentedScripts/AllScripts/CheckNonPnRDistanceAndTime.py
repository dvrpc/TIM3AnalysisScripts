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
    t = args[2] #Time Period
    return (skims['time'][t].loc[o, d], skims['dist'][t].loc[o, d])

def classify_time(args):
    if args[2] == 1:
        t = args[0]
    else:
        t = args[1]
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
trip_file = r'D:\TIM3.1\DaySimLab\scenario\Output\05201612\_trip_2.dat'
trip = pd.read_csv(trip_file, '\t')

#log('Reading Tour Data')
#tour_file = trip_file.replace('trip', 'tour')
#tour = pd.read_csv(tour_file, '\t')

log('Merging and Querying')
#trip = tour.merge(trip, on = ['hhno', 'pno', 'day', 'tour']) #Merge tour info to trip info
#trip = trip.query('(opurp != 0 or dpurp != 10) and (opurp != 10 or dpurp != 0)') #From home to PnR or vice-versa
trip = trip.query('opurp != 10 and dpurp != 10')

log('Setting Up Table')
trip['direction'] = np.where(trip['dpurp'] == 10, 'ToPnR', 'FromPnR')
trip['tod_args'] = list(zip(trip['arrtm'], trip['deptm'], trip['half']))
trip['tod'] = trip['tod_args'].apply(classify_time)

log('Getting Skim Values')
trip['skim_args'] = list(zip(trip['otaz'], trip['dtaz'], trip['tod']))
trip['skims'] = trip['skim_args'].apply(get_skims)
trip['skimtime'] = trip['skims'].apply(lambda x: x[0])
trip['skimdist'] = trip['skims'].apply(lambda x: x[1])

log('Comparing')
trip['timediff'] = trip['skimtime'] - trip['travtime']
trip['distdiff'] = trip['skimdist'] - trip['travdist']

log('Writing')
outfile = r'D:\TIM3\NonPnRTripsWithVISUMSkims.csv'
trip.to_csv(outfile)

log('Done')