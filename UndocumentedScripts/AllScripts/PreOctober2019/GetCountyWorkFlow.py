import pandas as pd
import numpy as np
import time
import sys
sys.path.append(r'D:\TIM3')
from daysim_loader import load_daysim_files

base_path = r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output'
taz2county_file = r'D:\TIM3\taz2county.csv'
acs_file = r'D:\TIM3\ACS5yr2011-2015.csv'

outfile = r'D:\TIM3\HomeWorkCountyFlow.xlsx'
outsheet = 'County Work Flows'

def aggregate_od_matrix(matrix, aggregator):
    return pd.DataFrame(np.dot(np.dot(aggregator.T, matrix), aggregator),
                        index   = aggregator.columns,
                        columns = aggregator.columns)

#def write_table(df, sheet, name, startrow = 0, startcol = 0):


# # # # # # # # # # # # # MAIN SCRIPT # # # # # # # # # # # # #

results = {}

print('Reading Files')
t0 = time.time()
files = load_daysim_files(base_path, ['hh', 'per'])

taz2county = pd.read_csv(taz2county_file, index_col = 0)['County']
results['ACS'] = pd.read_csv(acs_file, index_col = 0)

t1 = time.time()
print('Files read in ' + str(round(t1-t0,1)) + ' seconds')

hhper = files['hh'].merge(files['per'], on = 'hhno')
del files

workers = hhper[hhper['pwtaz'] > 0] #Filter for workers
workers['hhcounty'] = workers['hhtaz'].map(taz2county)
workers['pwcounty'] = workers['pwtaz'].map(taz2county)
results['DaySim'] = workers[['hhcounty', 'pwcounty', 'psexpfac']].groupby(['hhcounty', 'pwcounty']).sum().reset_index().pivot(index = 'hhcounty', columns = 'pwcounty', values = 'psexpfac')

results['Difference'] = results['DaySim'] - results['ACS']
results['%Diff'] = results['Difference'] / results['ACS']

#Get River Crossings
county2side = pd.DataFrame(np.zeros((results['ACS'].shape[0], 2)), index = results['ACS'].index, columns = ['W', 'E'])
county2side.loc['Bucks', 'W'] += 1
county2side.loc['Chester', 'W'] += 1
county2side.loc['Delaware', 'W'] += 1
county2side.loc['Montgomery', 'W'] += 1
county2side.loc['Philadelphia', 'W'] += 1
county2side.loc['Rest of PA', 'W'] += 1
county2side.loc['Rest of Outer Counties', 'W'] += 1
county2side.loc['Burlington', 'E'] += 1
county2side.loc['Camden', 'E'] += 1
county2side.loc['Gloucester', 'E'] += 1
county2side.loc['Mercer', 'E'] += 1
county2side.loc['Rest of NJ', 'E'] += 1

rx = {}
rx['ACS'] = aggregate_od_matrix(results['ACS'], county2side)
rx['DaySim'] = aggregate_od_matrix(results['DaySim'], county2side)
rx['Difference'] = rx['DaySim'] - rx['ACS']
rx['%Diff'] = rx['Difference'] / rx['ACS']

writer = pd.ExcelWriter(outfile)

#Write county flows
results['ACS'].to_excel(writer, outsheet, startrow = 0, startcol = 0)#, float_format = '{:,}')
results['DaySim'].to_excel(writer, outsheet, startrow = 0, startcol = 15)#, float_format = '{:,}')
results['Difference'].to_excel(writer, outsheet, startrow = 15, startcol = 0)#, float_format = '{:,}')
results['%Diff'].to_excel(writer, outsheet, startrow = 15, startcol = 15)#, float_format = '{0:.0%}')

#Write river crossing flows
sheet = 'River Crossings'
rx['ACS'].to_excel(writer, sheet, startrow = 0, startcol = 0)
rx['DaySim'].to_excel(writer, sheet, startrow = 0, startcol = 5)
rx['Difference'].to_excel(writer, sheet, startrow = 5, startcol = 0)
rx['%Diff'].to_excel(writer, sheet, startrow = 5, startcol = 5)

writer.save()

print('Done')