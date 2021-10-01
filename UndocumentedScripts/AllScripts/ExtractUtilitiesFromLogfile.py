import pandas as pd
import numpy as np

def line2dict(l):
    outdict = {}
    for element in l:
        split = element.split(':')
        outdict[split[0]] = split[1]
    return outdict

print('Reading Log File')
fp = r'D:\TIM3.1\DaySimLab\scenario\Output\run_2021-05-20_16h26m.log'
f = open(fp, 'r')
lines = f.read().split('\n')
f.close()

print('Isolating Lines with Utilities')
utils = []
#tofar = []
for line in lines:
    #if line.replace(' ', '')[:5] == 'otaz:':
    if 'otaz:' in line:
        utils.append(line.replace(',,', ',').replace(' ', '').replace('TransitUtil', ',TransitUtil').split(','))
    #if 'is too far away from origin zone' in line:
    #    split = line[4:].split(' ')
    #    tofar.append([int(split[2]), int(split[-1])])
utils = pd.Series(utils).apply(line2dict)
#tofar = pd.DataFrame(np.array(tofar), columns = ['node', 'taz'])

print('Rearranging Into Data Frame')
cols = list(utils.loc[0].keys())
M = utils.shape[0]
N = len(cols)
df = pd.DataFrame(np.zeros((M, N), str), utils.index, cols)
for col in cols:
    df[col] = utils.apply(lambda x: x[col])

print('Writing File')
outfile = r'D:\TIM3\PnRNodeUtilities0520b.dat'
df.to_csv(outfile, '\t')
#tofar.to_csv(r'D:\TIM3\ToFar0520.dat', '\t')

print('Go')