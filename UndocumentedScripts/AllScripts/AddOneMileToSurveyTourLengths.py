import pandas as pd

infile = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\DaySimSummaries\data\dvrpc_tourx6.dat'
outfile = infile.replace('.dat', '+1.dat')

print('Reading')
data = pd.read_csv(infile, '\t')
data['tautodist'] += 1
print('Writing')
data.to_csv(outfile, '\t')
print('Arithmetic')