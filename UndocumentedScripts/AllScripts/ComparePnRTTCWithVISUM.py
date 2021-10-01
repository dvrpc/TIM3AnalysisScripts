import pandas as pd
import numpy as np
import VisumPy.helpers as h
import os

util_file = r'D:\TIM3\PnRNodeUtilities0519.dat'
#tofar_file = r'D:\TIM3\ToFar0518.dat'
pnr_file = r'D:\TIM3.1\DaySimLab\scenario\inputs\DVRPC_p_rNodes.dat'

def log(msg):
    Visum.Log(20480, msg)

def unpivot(tt, name):
    '''
    Unpivots a trip table
    '''
    N = tt.shape[0]
    outdf = pd.DataFrame(np.empty((N**2, 3)), columns = ['O', 'D', name])
    outdf['O'] = np.repeat(tt.index, N)
    outdf['D'] = np.hstack(N*list(tt.columns))
    outdf[name] = np.reshape(tt.values, N**2)
    return outdf

log('Reading DAT files')
util = pd.read_csv(util_file, '\t')
#tofar = pd.read_csv(tofar_file, '\t')
pnr = pd.read_csv(pnr_file, '\t').set_index('NodeID')

log('Loading Time Skims')
zones = np.array(h.GetMulti(Visum.Net.Zones, 'No'))
ttc = pd.DataFrame(h.GetMatrix(Visum, 302)+h.GetMatrix(Visum, 304).T, zones, zones)

log('Unpivoting Time Skims')
ttc = unpivot(ttc, 'ttc')

ttc['OD'] = list(zip(ttc['O'], ttc['D']))

log('Adding Travel Time to Utility Table')
util['dtaz'] = util['PnRnode'].map(pnr['ZoneID'])
util['OD'] = list(zip(util['otaz'], util['dtaz']))
util['ttc'] = util['OD'].map(ttc.set_index('OD')['ttc'])
util['timediff'] = util['ttc'] - util['time']

del ttc
log('Loading Distance Skims')
dis = pd.DataFrame(h.GetMatrix(Visum, 402) + h.GetMatrix(Visum, 404), zones, zones)

log('Unpivoting Distance Skims')
dis = unpivot(dis, 'dis')
dis['OD'] = list(zip(dis['O'], dis['D']))

log('Adding Distance to Utility Table')
util['dis'] = util['OD'].map(dis.set_index('OD')['dis'])
util['distdiff'] = util['dis'] - util['distance']

del dis

log('Writing')
outfile = r'D:\TIM3\PnRUtilitiesWithTimeCheck0519.dat'
util.to_csv(outfile, '\t')

log('Done')