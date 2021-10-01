import pandas as pd
import os

#base_path = r'Y:\TIM_3.1\DVRPC_ABM_VISUM18patch\scenario'
base_path = r'T:\TIM_3.1\190308_TestNewTruckDistr\scenario'
infile = os.path.join(base_path, 'microzonetostopareadistance.dat')
outfile = os.path.join(base_path, 'SuburbanAccessibleMAZs.csv')

print('Reading File')
df = pd.read_csv(infile, ' ')
print('Getting Suburban MAZs')
sub_mazs = df[df['stopareaid'] == 1103]
print('Writing Output')
sub_mazs.to_csv(outfile)
print('Done')