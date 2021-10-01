import pandas as pd
import numpy as np

infile = r'D:\TIM3.1\190909_AssignmentConv1e-4\scenario\Output\_trip_2.dat'
print('Reading Trip File')
trip = pd.read_csv(infile, '\t')
print('Reading Person File')
per = pd.read_csv(infile.replace('trip', 'person'), '\t')

purps = ['HBW', 'HBShop', 'HBSchool', 'HBU', 'HBO', 'NHBW', 'NHBO']
purpindex = np.arange(1, len(purps) + 1, dtype = int)

purpmap = dict(zip(purpindex, purps))

print('Classifying trip person types')
per['under18'] = (per['pptyp'] == 6) | (per['pptyp'] == 7) | (per['pptyp'] == 8)
per['hhperid'] = list(zip(per['hhno'], per['pno']))
trip['hhperid'] = list(zip(trip['hhno'], trip['pno']))
trip['under18'] = trip['hhperid'].map(per.set_index('hhperid')['under18'])

print('Identifying TIM2 trip purposes')
#Create dummy variables for each purpose
trip['HB']          = (trip['opurp'] == 0) | (trip['dpurp'] == 0)
trip['HBW']         = trip['HB'] & ((trip['opurp'] == 1) | (trip['dpurp'] == 1))
trip['HBShop']      = trip['HB'] & ((trip['opurp'] == 5) | (trip['dpurp'] == 5))
trip['HBSchool']    = trip['HB'] & trip['under18'] & ((trip['opurp'] == 2) | (trip['dpurp'] == 2))
trip['HBU']         = trip['HB'] & ~trip['under18'] & ((trip['opurp'] == 2) | (trip['dpurp'] == 2))
trip['HBO']         = trip['HB'] & ~(trip['HBW'] | trip['HBShop'] | trip['HBSchool'] | trip['HBU'])
trip['NHBW']        = ~trip['HB'] & ((trip['opurp'] == 1) | (trip['dpurp'] == 1))
trip['NHBO']        = ~(trip['HB'] | trip['NHBW'])
#Perform matrix-vector multiplication with dummy variables and unique purpose codes and decode the resulting array
trip['tim2_purpose'] = (trip[purps] @ purpindex).map(purpmap)

trips_by_purpose = trip[['tim2_purpose', 'trexpfac']].groupby('tim2_purpose').sum()['trexpfac']
print(trips_by_purpose)

print('Done')