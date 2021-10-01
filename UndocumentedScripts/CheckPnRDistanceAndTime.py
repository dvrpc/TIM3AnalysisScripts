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
    return skim

skims= {'time': {'0000': read_skim_tofrom_pnr(301),
                 '0600': read_skim_tofrom_pnr(302),
                 '1000': read_skim_tofrom_pnr(303),
                 '1500': read_skim_tofrom_pnr(304),
                 '1900': read_skim_tofrom_pnr(305)},
        'dist': {'0000': read_skim_tofrom_pnr(401),
                 '0600': read_skim_tofrom_pnr(402),
                 '1000': read_skim_tofrom_pnr(403),
                 '1500': read_skim_tofrom_pnr(404),
                 '1900': read_skim_tofrom_pnr(405)}}

def get_skims(args):
    global skims
    o = args[0] #Origin
    d = args[1] #Destination
    t = args[2] #Time Period
    r = args[3] #Direction
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

log('Reading maz2taz correspondence')
maz2taz_file = r'D:\TIM3.1\DaySimLab\scenario\inputs\parcels_buffered.dat'
maz2taz = pd.read_csv(maz2taz_file, ' ', index_col = 0)

log('Reading Trip Data')
trip_file = r'D:\TIM3.1\DaySimLab\scenario\Output\05201612\_trip_2.dat'
trip = pd.read_csv(trip_file, '\t')

trip['otaz'] = trip['opcl'].map(maz2taz['taz_p'])
trip['dtaz'] = trip['dpcl'].map(maz2taz['taz_p'])

log('Reading Tour Data')
tour_file = trip_file.replace('trip', 'tour')
tour = pd.read_csv(tour_file, '\t')

log('Merging and Querying')
trip = tour.merge(trip, on = ['hhno', 'pno', 'day', 'tour']) #Merge tour info to trip info
trip = trip.query('(opurp == 0 and dpurp == 10) or (opurp == 10 and dpurp == 0)') #From home to PnR or vice-versa

log('Setting Up Table')
trip['direction'] = np.where(trip['dpurp'] == 10, 'ToPnR', 'FromPnR')
trip['tod_args'] = list(zip(trip['arrtm'], trip['deptm'], trip['half']))
trip['tod'] = trip['tod_args'].apply(classify_time)

log('Getting Skim Values')
trip['skim_args'] = list(zip(trip['otaz'], trip['dtaz'], trip['tod'], trip['direction']))
trip['skims'] = trip['skim_args'].apply(get_skims)
trip['skimtime'] = trip['skims'].apply(lambda x: x[0])
trip['skimdist'] = trip['skims'].apply(lambda x: x[1])

log('Comparing')
trip['timediff'] = trip['skimtime'] - trip['travtime']
trip['distdiff'] = trip['skimdist'] - trip['travdist']

log('Writing')
outfile = r'D:\TIM3\PnRTripsWithVISUMSkimsReclassifyZones.csv'
trip.to_csv(outfile)

log('Done')