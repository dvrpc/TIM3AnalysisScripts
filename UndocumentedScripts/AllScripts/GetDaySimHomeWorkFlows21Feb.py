from dsa_util import *

print('Reading files')
tables = []
tables.append(DSTable('hh-nosp',    r'Y:\TIM_3.1\TIM31_HigherTransitCoefficients\scenario\Output\_household_2.dat',     '\t'))
tables.append(DSTable('ps-nosp',    r'Y:\TIM_3.1\TIM31_HigherTransitCoefficients\scenario\Output\_person_2.dat',        '\t'))
tables.append(DSTable('to-nosp',    r'Y:\TIM_3.1\TIM31_HigherTransitCoefficients\scenario\Output\_tour_2.dat',          '\t'))
tables.append(DSTable('hh-long',    r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\3Iters\_household_2.dat',             '\t'))
tables.append(DSTable('ps-long',    r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\3Iters\_person_2.dat',                '\t'))
tables.append(DSTable('to-long',    r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\3Iters\_tour_2.dat',                  '\t'))
tables.append(DSTable('hh-short',   r'T:\TIM_3.1\200220_FewerFarAwayWorkplaceChoices\scenario\Output\_household_2.dat', '\t'))
tables.append(DSTable('ps-short',   r'T:\TIM_3.1\200220_FewerFarAwayWorkplaceChoices\scenario\Output\_person_2.dat',    '\t'))
tables.append(DSTable('to-short',   r'T:\TIM_3.1\200220_FewerFarAwayWorkplaceChoices\scenario\Output\_tour_2.dat',      '\t'))
tables = ReadTables(tables)

district_file = r'D:\ref\taz2flowdistrict.csv'
taz2district = pd.read_csv(district_file, index_col = 0)['FLOW_DISTRICT']

outfile = r'D:\TIM3\ShadowPricingHomeWorkFlows_200221_Raw.xlsx'

order = ['Center City', 'Outer Philadelphia', 'Suburban PA', 'Suburban NJ', 'Extended PA', 'Extended NJ', 'Extended DE/MD']

def get_home_work_flow(hh, ps):
    global taz2district
    hhwk = hh[['hhno', 'hhtaz']].merge(ps[['hhno', 'pwtaz', 'psexpfac']]).query('pwtaz > 0')
    hhwk['hdistrict'] = hhwk['hhtaz'].map(taz2district)
    hhwk['wdistrict'] = hhwk['pwtaz'].map(taz2district)
    return hhwk.groupby(['hdistrict', 'wdistrict']).sum()['psexpfac'].reset_index().pivot('hdistrict', 'wdistrict', 'psexpfac').fillna(0)

print('Processing Files')
output = {}
for iter in ['nosp', 'long', 'short']:
    output[iter] = get_home_work_flow(tables['hh-%s'%(iter)], tables['ps-%s'%(iter)]).loc[order, order]

print('Writing File')
writer = pd.ExcelWriter(outfile)
for iter in output:
    output[iter].to_excel(writer, iter)
writer.close()

print(tables['to-nosp'].query('pdpurp == 1')['toexpfac'].sum())
print(tables['to-long'].query('pdpurp == 1')['toexpfac'].sum())
print(tables['to-short'].query('pdpurp == 1')['toexpfac'].sum())

print('Go')