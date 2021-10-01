from dsa_util import *

print('Reading files')
tables = []
tables.append(DSTable('hh0',    r'Y:\TIM_3.1\TIM31_HigherTransitCoefficients\scenario\Output\_household_2.dat', '\t'))
tables.append(DSTable('ps0',    r'Y:\TIM_3.1\TIM31_HigherTransitCoefficients\scenario\Output\_person_2.dat',    '\t'))
tables.append(DSTable('to0',    r'Y:\TIM_3.1\TIM31_HigherTransitCoefficients\scenario\Output\_tour_2.dat',      '\t'))
tables.append(DSTable('hh3',    r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\_household_2.dat',                '\t'))
tables.append(DSTable('ps3',    r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\_person_2.dat',                   '\t'))
tables.append(DSTable('to3',    r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\_tour_2.dat',                     '\t'))
tables.append(DSTable('hh20',   r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\20Iters\_household_2.dat',        '\t'))
tables.append(DSTable('ps20',   r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\20Iters\_person_2.dat',           '\t'))
tables.append(DSTable('to20',   r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\20Iters\_tour_2.dat',             '\t'))
tables = ReadTables(tables)

district_file = r'D:\ref\taz2flowdistrict.csv'
taz2district = pd.read_csv(district_file, index_col = 0)['FLOW_DISTRICT']

outfile = r'D:\TIM3\ShadowPricingHomeWorkFlows_Raw.xlsx'

order = ['Center City', 'Outer Philadelphia', 'Suburban PA', 'Suburban NJ', 'Extended PA', 'Extended NJ', 'Extended DE/MD']

def get_home_work_flow(hh, ps):
    global taz2district
    hhwk = hh[['hhno', 'hhtaz']].merge(ps[['hhno', 'pwtaz', 'psexpfac']]).query('pwtaz > 0')
    hhwk['hdistrict'] = hhwk['hhtaz'].map(taz2district)
    hhwk['wdistrict'] = hhwk['pwtaz'].map(taz2district)
    return hhwk.groupby(['hdistrict', 'wdistrict']).sum()['psexpfac'].reset_index().pivot('hdistrict', 'wdistrict', 'psexpfac').fillna(0)

print('Processing Files')
output = {}
for iter in ['0', '3', '20']:
    output[iter] = get_home_work_flow(tables['hh%s'%(iter)], tables['ps%s'%(iter)]).loc[order, order]

print('Writing File')
writer = pd.ExcelWriter(outfile)
for iter in output:
    output[iter].to_excel(writer, iter)
writer.close()

print(tables['to0'].query('pdpurp == 1')['toexpfac'].sum())
print(tables['to3'].query('pdpurp == 1')['toexpfac'].sum())
print(tables['to20'].query('pdpurp == 1')['toexpfac'].sum())

print('Go')