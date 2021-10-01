import pandas as pd
import sys
import os
import datetime

day_label = datetime.datetime.now().strftime('%y%m%d%H%M%S')

base_path = sys.argv[1]
infile = os.path.join(base_path, 'microzonetostopareadistance.dat')
outfile = os.path.join(r'D:\TIM3', 'n_mazs_by_sa_{}.csv'.format(day_label))

print('Reading File')
df = pd.read_csv(infile, ' ')
print('Grouping MAZs by Stop Area')
mazs_by_sa = df.groupby('stopareaid').count()['zoneid']
print('Writing File')
mazs_by_sa.to_csv(outfile)
print('Done')