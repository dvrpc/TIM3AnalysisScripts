import pandas as pd

outfile = r'D:\TIM3\PnRDebug0714PATCO_CC.csv'
infile = r'D:\TIM3.1\DaySimLab\scenario\Output\run_2021-07-14_13h03m.log'

print('Reading')
f = open(infile, 'r')
lines = f.read().split('\n')
f.close()

pnr_file = r'D:\TIM3.1\DaySimLab\scenario\inputs\DVRPC_p_rNodes.dat'
pnr = pd.read_csv(pnr_file, '\t', index_col = 0)

print('Unpacking')
df = pd.DataFrame()
c = 0
for line in lines:
    if line[4:9] != 'opcl:':
        continue
    df[c] = pd.Series(dict(entry.split(':') for entry in line.replace(' ', '').replace('Parcel:', '').split(',')))
    c += 1
    if c % 10000 == 0:
        print(c)

df = df.T
df['PnRLot'] = df['PnRLot'].astype(int).map(pnr['ZoneID'])

print('Writing')
df.to_csv(outfile)

print('Done')