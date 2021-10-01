from __future__ import division #Not needed if running in Python 3
import pandas as pd
import numpy as np

infile = r'D:\TIM3\DSOutputsYoshi0621\PnRZoneToMAZandSA.csv'
outfile = infile.replace('.csv', 'WithDistAndTime.csv')
df = pd.read_csv(infile, index_col = 0)

dist_file = r'D:\TIM3\DSOutputsYoshi0621\microzonetostopareadistance.dat'
dist = pd.read_csv(dist_file, ' ')

def get_dist(args):
    '''
    Obtains the distance from input microzone and stop area

    Parameters
    ----------
    args (tuple):
        Length-2 tuple where the first entry is the microzone number and the second entry is the stop area number

    Returns
    -------
    distance (float):
        Distance in feet from the input microzone to the input stop area
    '''
    global dist
    maz = args[0]
    sa = args[1]
    try:
        return dist.query('zoneid == @maz and stopareaid == @sa')['distance'].iloc[0]
    except IndexError:
        print('Index error for MAZ {0} and stop area {1}'.format(maz, sa))
        return np.nan

df['args'] = list(zip(df['MAZ'], df['SA']))
df['dist'] = df['args'].apply(get_dist)
df['time'] = (20/5280)*df['dist']
del df['args']

df.to_csv(outfile)

print('Go')