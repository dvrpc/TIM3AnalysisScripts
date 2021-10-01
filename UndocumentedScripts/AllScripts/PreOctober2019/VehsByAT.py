import pandas as pd

taz2at_file = r'D:\TIM3\taz2areatype.csv'
hh_file = r'T:\TIM_3.1\DVRPC_ABM_Testing\scenario\Output\_household_2.dat'
outfile = r'D:\TIM3\VehsByAT.csv'

print('Reading Data')
taz2at = pd.read_csv(taz2at_file, index_col = 0)['AREA_TYPE']
hh = pd.read_csv(hh_file, '\t').query('hhtaz < 50000')

print('Calculating')
hh['area_type'] = hh['hhtaz'].map(taz2at)
gbatveh = hh[['area_type', 'hhvehs', 'hhexpfac']].groupby(['area_type', 'hhvehs']).sum().reset_index()
output = gbatveh.pivot('area_type', 'hhvehs', 'hhexpfac')

print('Writing File')
output.to_csv(outfile)