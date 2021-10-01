from dsa_util import *
import os
from subprocess import Popen
import time
import matplotlib.pyplot as plt

order = [42101, 42045, 42029, 42091, 42017, 34021, 34005, 34007, 34015, 42071, 42011, 42077, 42095,
         34041, 34019, 34035, 34023, 34025, 34029, 34001, 34009, 34011, 34033, 10003, 24015]

county_name_map = {42101: 'Philadelphia County, Pennsylvania (DVRPC)',
                   42045: 'Delaware County, Pennsylvania (DVRPC)',
                   42029: 'Chester County, Pennsylvania (DVRPC)',
                   42091: 'Montgomery County, Pennsylvania (DVRPC)',
                   42017: 'Bucks County, Pennsylvania (DVRPC)',
                   34021: 'Mercer County, New Jersey (DVRPC)',
                   34005: 'Burlington County, New Jersey (DVRPC)',
                   34007: 'Camden County, New Jersey (DVRPC)',
                   34015: 'Gloucester County, New Jersey (DVRPC)',
                   42071: 'Lancaster County, Pennsylvania (Extended)',
                   42011: 'Berks County, Pennsylvania (Extended)',
                   42077: 'Lehigh County, Pennsylvania (Extended)',
                   42095: 'Northampton County, Pennsylvania (Extended)',
                   34041: 'Warren County, New Jersey (Extended)',
                   34019: 'Hunterdon County, New Jersey (Extended)',
                   34035: 'Somerset County, New Jersey (Extended)',
                   34023: 'Middlsex County, New Jersey (Extended)',
                   34025: 'Monmouth County, New Jersey (Extended)',
                   34029: 'Ocean County, New Jersey (Extended)',
                   34001: 'Atlantic County, New Jersey (Extended)',
                   34009: 'Cape May County, New Jersey (Extended)',
                   34011: 'Cumberland County, New Jersey (Extended)',
                   34033: 'Salem County, New Jersey (Extended)',
                   10003: 'New Castle County, Delaware (Extended)',
                   24015: 'Cecil County, Maryland (Extended)'}

n_iters = ['00', '04', '08', '12', '16']

def get_county_flow(hh_file, per_file, taz2county):
    workers = hh_file.merge(per_file).query('pwtyp > 0')
    workers['hcounty'] = workers['hhtaz'].map(taz2county)
    workers['wcounty'] = workers['pwtaz'].map(taz2county)
    return workers[['hcounty', 'wcounty', 'psexpfac']].groupby(['hcounty', 'wcounty']).sum().reset_index().pivot('hcounty', 'wcounty', 'psexpfac').fillna(0)

def plot_progress(progress_df, county, target):
    global county_name_map, order
    name = county_name_map[county]

    x = np.arange(0, 17, 4)
    y = np.array(progress_df.loc[county])

    #p = np.polyfit(x, y, 2)
    #x_c = np.linspace(0, 16, 1001)
    #y_c = p[0]*np.power(x_c, 4) + p[1]*np.power(x_c, 3) + p[2]*np.power(x_c, 2) + p[3]*np.power(x_c, 1) + p[4]*np.power(x_c, 0)
    #y_c = p[0]*np.power(x_c, 2) + p[1]*x_c + p[2]

    mx = np.maximum(y, target)
    mn = np.minimum(y, target)

    plt.scatter(x, y, color = 'k', s = 10, label = 'Workers in County')
    plt.plot(x, y, color = 'k', linewidth = 1, label = 'Quadratic Fit')
    plt.plot([0, 16], 2*[target], color = 'k', linewidth = 1, linestyle = '--', label = 'Target (TAZ Data)')
    #plt.ylim(mn, 1.2*mx)
    plt.grid(True)
    plt.xlabel('Number of Shadow Pricing Iterations')
    plt.ylabel('Number of Workers')
    plt.title(name)

    #plt.legend(loc = 'upper right')

    plt.savefig(r'D:\TIM3\ShadowPricingEffect\plots\{}.png'.format(county))
    plt.clf()


t0 = time.time()
print('Reading Files')
tables = []
tables.append(DSTable('hh00', os.path.join(r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\NoShadowPrice\_household_2.dat'), '\t'))
tables.append(DSTable('ps00', os.path.join(r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\NoShadowPrice\_person_2.dat'),    '\t'))
tables.append(DSTable('hh04', os.path.join(r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\4Iters\_household_2.dat'),        '\t'))
tables.append(DSTable('ps04', os.path.join(r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\4Iters\_person_2.dat'),           '\t'))
tables.append(DSTable('hh08', os.path.join(r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\8Iters\_household_2.dat'),        '\t'))
tables.append(DSTable('ps08', os.path.join(r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\8Iters\_person_2.dat'),           '\t'))
tables.append(DSTable('hh12', os.path.join(r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\12Iters\_household_2.dat'),       '\t'))
tables.append(DSTable('ps12', os.path.join(r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\12Iters\_person_2.dat'),          '\t'))
tables.append(DSTable('hh16', os.path.join(r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\16Iters\_household_2.dat'),       '\t'))
tables.append(DSTable('ps16', os.path.join(r'Y:\TIM_3.1\DVRPC_ABM_Github\scenario\Output\16Iters\_person_2.dat'),          '\t'))
tables = ReadTables(tables)
t1 = time.time()
print(t1 - t0)

taz2fips_file = r'D:\ref\taz2fips.csv'
taz2county = pd.read_csv(taz2fips_file, index_col = 0)['STATE_COUNTY_ID']

target_file = r'D:\ref\EmpByCountyTAZ.csv'
targets = pd.read_csv(target_file, index_col = 0)['EMP']

t2 = time.time()
print(t2 - t1)

print('Getting County Flows')

county_flows = {}
for n_iter in n_iters:
    county_flows[n_iter] = get_county_flow(tables['hh' + n_iter], tables['ps' + n_iter], taz2county).loc[order, order]

t3 = time.time()
print(t3 - t2)

print('Writing County Flows')

writer = pd.ExcelWriter(r'D:\TIM3\ShadowPricingEffect\CountyFlows.xlsx')
for n_iter in n_iters:
    county_flows[n_iter].to_excel(writer, n_iter)
writer.close()

t4 = time.time()
print(t4 - t3)

print('Getting Workers by County')

workers_by_county = pd.DataFrame(index = order)
for n_iter in n_iters:
    workers_by_county[n_iter] = county_flows[n_iter].sum(0)

t5 = time.time()
print(t5 - t4)

print('Plotting Progress by County')
for county in order:
    print(county)
    plot_progress(workers_by_county, county, targets[county])

t6 = time.time()
print(t6 - t5)

print('Go')