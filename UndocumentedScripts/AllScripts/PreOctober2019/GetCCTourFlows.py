import pandas as pd
import os
import time
from collections import OrderedDict

def create_county_county_flows(records, county_list = None):
    '''
    Creates a county-county flow for the given trip records

    Parameters
    ----------
    records (pandas.DataFrame):
        Table of records. Must include the following fields ['tocounty' (str), 'tdcounty' (str), 'toexpfac' (numeric)]
    county_list (list):
        List of county names to specify the order

    Returns
    -------
    county_county_flow(pandas.DataFrame):
        Pivoted data frame adding up the expansion weights
    '''
    county_county_flow = records[['tocounty', 'tdcounty', 'toexpfac']].groupby(['tocounty', 'tdcounty']).sum().reset_index().pivot(index = 'tocounty', columns = 'tdcounty', values = 'toexpfac').fillna(0)
    if county_list:
        county_county_flow = county_county_flow[county_list].T[county_list].T
    return county_county_flow

time_start = time.time()

base_path = r'D:\Debugging'
runs = ['survey', 'run0', 'run1a', 'run2a']
run_flows = {}
for run in runs:
    tour_file = os.path.join(base_path, 'Runs', run, '_tour_2.dat')

    taz2county_file = os.path.join(base_path, 'taz2county.csv')
    taz2county = pd.read_csv(taz2county_file, index_col = 0)['County']

    outfile = os.path.join(base_path, 'Runs', run, 'CountyCountyTourFlows.xlsx')

    purpmap = {1: 'Work',
               2: 'School',
               3: 'Escort',
               4: 'Personal Business',
               5: 'Shop',
               6: 'Meal',
               7: 'Social'}

    counties = ['Bucks',
                'Chester',
                'Delaware',
                'Montgomery',
                'Philadelphia',
                'Burlington',
                'Camden',
                'Gloucester',
                'Mercer']
                #'Rest of PA',
                #'Rest of NJ',
                #'Rest of Outer Counties',
                #'Outside'
                #]

    tour_fields = ['totaz', 'tdtaz', 'pdpurp', 'toexpfac']

    rs = time.time()
    tour = pd.read_table(tour_file, usecols = tour_fields)
    re = time.time()
    print(re - rs)

    tour['tocounty'] = tour['totaz'].map(taz2county)
    tour['tdcounty'] = tour['tdtaz'].map(taz2county)

    flows = OrderedDict()
    flows['Total'] = create_county_county_flows(tour, counties)
    for p in range(1, 8):
        flows[purpmap[p]] = create_county_county_flows(tour[tour['pdpurp'] == p], counties)

    flows = pd.Panel(flows)
    flows.to_excel(outfile)

    if run == 'survey':
        survey = flows

    else:
        difference = flows.subtract(survey)
        difference.to_excel(outfile.replace('.xlsx', 'Difference.xlsx'))
        difference.divide(survey).to_excel(outfile.replace('.xlsx', 'PercentDifference.xlsx'))
    
    #run_flows[run] = flows

#run_flows = pd.Panel4D(run_flows)



time_end = time.time()
print(time_end - time_start)