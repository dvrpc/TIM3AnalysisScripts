import pandas as pd

survey = pd.read_csv(r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_tour_2.dat', '\t')
daysim = pd.read_csv(r'D:\TIM3.1\CalibrationAugust2021\scenario\Output\2108071831\_tour_2.dat', '\t')#.query('toexpfac == 1')

print('Total Work Tours Originating in New Jersey')
qry1 = '(pdpurp == 1 and ((totaz >= 18000 and totaz < 50000) or (totaz >= 53000 and totaz < 58000)))'
print('Survey: {}'.format(survey.query(qry1)['toexpfac'].sum()))
print('DaySim: {}'.format(daysim.query(qry1)['toexpfac'].sum()))

print('\nDrive-Transit Tours')
qry2 = '(pdpurp == 1 and tmodetp == 7)'
print('Survey: {}'.format(survey.query(qry2)['toexpfac'].sum()))
print('DaySim: {}'.format(daysim.query(qry2)['toexpfac'].sum()))

print('\nBoth')
qry3 = qry1 + ' and ' + qry2
print('Survey: {}'.format(survey.query(qry3)['toexpfac'].sum()))
print('DaySim: {}'.format(daysim.query(qry3)['toexpfac'].sum()))