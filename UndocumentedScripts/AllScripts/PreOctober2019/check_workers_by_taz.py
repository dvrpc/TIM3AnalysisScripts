import pandas as pd
import os
from subprocess import Popen

runs = ['run0', 'run1a', 'run2a']



students_by_taz = pd.DataFrame()
BASE_PATH = r'D:\Debugging\Runs'


taz2county_file = os.path.join(os.path.split(BASE_PATH)[0], 'taz2county.csv')
taz2county = pd.read_csv(taz2county_file, index_col = 0)['County']

unknown_worker_share_by_county = pd.DataFrame()

for run in runs:
    hh = pd.read_table(os.path.join(BASE_PATH, run, '_household_2.dat'), usecols = ['hhno', 'hhtaz', 'hhparcel'])
    per = pd.read_table(os.path.join(BASE_PATH, run, '_person_2.dat'), usecols = ['hhno', 'pwtaz', 'pwpcl', 'pwtyp', 'psexpfac', 'pwautime'])
    per['hpcl'] = per['hhno'].map(hh.set_index('hhno')['hhparcel'])
    per['htaz'] = per['hhno'].map(hh.set_index('hhno')['hhtaz'])
    per['hcounty'] = per['htaz'].map(taz2county)
    per['wcounty'] = per['pwtaz'].map(taz2county)
    #per = per[per['htaz'] < 50000] #Uncomment to select only people living in DVRPC region
    #students_by_taz[run] = per.groupby('pwtaz').sum()['psexpfac']
    #workers = per[per['pwtyp'] != 0]['psexpfac'].sum()
    #emp = students_by_taz.iloc[1:][run].sum()
    
    workers = per[per['pwtyp'] != 0]
    unknown_workers = workers[workers['pwtaz'] == -1]
    
    workers_per_county = workers.groupby('hcounty').sum()['psexpfac']
    unknown_workers_per_county = unknown_workers.groupby('hcounty').sum()['psexpfac']
    unknown_worker_share_by_county[run] = unknown_workers_per_county / workers_per_county

    #work_at_home = workers[workers['hpcl'] == workers['pwpcl']]
    work_at_home = workers[workers['pwautime'] == 0]
    print(work_at_home['psexpfac'].sum() / workers['psexpfac'].sum())

    #stop
    #print('{0}:\t{1}, {2}, {3}, {4}'.format(run, per['psexpfac'].sum(), workers, emp, 1 - emp/workers))

outfile = os.path.join(BASE_PATH, 'workersByTAZ.csv')
#students_by_taz.fillna(0).to_csv(outfile)
#Popen(outfile, shell = True)

print(unknown_worker_share_by_county)