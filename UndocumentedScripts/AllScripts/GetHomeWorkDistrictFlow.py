import pandas as pd
import os

def classify_district(taz):
    if taz < 200:
        return 'Center City'
    elif taz < 4000:
        return 'Outer Philadelphia'
    elif taz < 18000:
        return 'Suburban PA'
    elif taz < 50000:
        return 'Suburban NJ'
    elif taz < 53000:
        return 'Extended PA'
    elif taz < 58000:
        return 'Extended NJ'
    elif taz < 60000:
        return 'Extended DE/MD'
    else:
        return 'External'

def aggregate_flows(hhfile, perfile, hhsep = '\t', persep = '\t'):

    hh = pd.read_csv(hhfile, hhsep)
    per = pd.read_csv(perfile, persep)
    hhper = hh.merge(per, on = 'hhno')
    workers = hhper[hhper['pwtaz'] > 0]

    workers['hdist'] = workers['hhtaz'].apply(classify_district)
    workers['wdist'] = workers['pwtaz'].apply(classify_district)

    return workers[['hdist', 'wdist', 'psexpfac']].groupby(['hdist', 'wdist']).sum()['psexpfac'].reset_index().pivot('hdist', 'wdist', 'psexpfac')

hh_survey = r'M:\Modeling\Model_Development\TIM3.1\Template_Github\DVRPC_ABM\scenario\DaySimSummaries\data\dvrpc_hrecx4.dat'
per_survey = r'M:\Modeling\Model_Development\TIM3.1\Template_Github\DVRPC_ABM\scenario\DaySimSummaries\data\dvrpc_precx5.dat'
hh_base = r'D:\TIM3.1\191217_DistToTransit0\scenario\Output\_household_2.dat'
per_base = r'D:\TIM3.1\191217_DistToTransit0\scenario\Output\_person_2.dat'
hh_test = r'D:\TIM3.1\191230_OfficeBufferInWorkLoc\scenario\Output\_household_2.dat'
per_test = r'D:\TIM3.1\191230_OfficeBufferInWorkLoc\scenario\Output\_person_2.dat'

outfile = r'D:\TIM3.1\DistrictFlows191231_RAW.xlsx'

flows = {}
print('Survey')
flows['survey'] = aggregate_flows(hh_survey, per_survey, ',', ' ')
print('Base')
flows['base'] = aggregate_flows(hh_base, per_base)
print('Test')
flows['test'] = aggregate_flows(hh_test, per_test)

print('Writing Output')
writer = pd.ExcelWriter(outfile)
for dataset in flows:
    flows[dataset].to_excel(writer, dataset)
writer.close()
print('Done')