import pandas as pd
import numpy as np
import os
import statsmodels.api as sm
from statsmodels.genmod import families

def Log3(var1, var2, var3):
    if min(var1, var2, var3) < 1e-40:
        return 0
    else:
        total = var1 + var2 + var3
        return -(var1/total*np.log(var1/total) + var2/total*np.log(var2/total) + var3/total*np.log(var3/total))/np.log(4)
Log3 = np.vectorize(Log3)

base_path = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output'
hh_file = os.path.join(base_path, '_household_2.dat')
pday_file = os.path.join(base_path, '_person_day_2.dat')

hh = pd.read_csv(hh_file, '\t')
pday = pd.read_csv(pday_file, '\t')
pday['hhparcel'] = pday['hhno'].map(hh.set_index('hhno')['hhparcel'])

parcel_file = r'D:\TIM3.1\ImpedanceCalculationTest\Template_Internal\scenario\inputs\parcels_buffered.dat'
parcel = pd.read_csv(parcel_file, ' ')

parcel['MixedUse3Index2'] = Log3(parcel['hh_2'], parcel['empret_2'], parcel['empsvc_2'])
parcel['IntersectionDensity'] = 0.5*parcel['nodes3_2'] + parcel['nodes4_2'] - parcel['nodes1_2']

pday['MixedUse3Index2'] = pday['hhparcel'].map(parcel.set_index('parcelid')['MixedUse3Index2'])
pday['IntersectionDensity'] =  pday['hhparcel'].map(parcel.set_index('parcelid')['IntersectionDensity'])
pday['t1'] = (pday['wktours'] > 0).astype(int)
pday['t2'] = (pday['sctours'] > 0).astype(int)
pday['t3'] = (pday['estours'] > 0).astype(int)
pday['t4'] = (pday['pbtours'] > 0).astype(int)
pday['t5'] = (pday['shtours'] > 0).astype(int)
pday['t6'] = (pday['mltours'] > 0).astype(int)
pday['t7'] = (pday['sotours'] > 0).astype(int)

X = pd.DataFrame({'Intercept': np.ones_like(pday.index), 'Mixed': pday['MixedUse3Index2'], 'Intersection': pday['IntersectionDensity']})
for p in range(1, 8):
    print('\n')
    print(p)
    res = sm.GLM(pday['t{}'.format(p)], X, family = families.Binomial()).fit()
    print(res.summary())

#parcel.to_csv(r'D:\TIM3\ParcelWithIntersectionDensity.csv')
print('Go')