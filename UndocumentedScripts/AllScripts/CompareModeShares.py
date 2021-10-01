import pandas as pd

before_file = r'D:\TIM3.1\CenterCityScreenlineCalibration\scenario\Output\iter0\_tour_2.dat'
after_file = r'D:\TIM3.1\CenterCityScreenlineCalibration\scenario\Output\_tour_2.dat'

data = {}
data['before'] = pd.read_csv(before_file, '\t').query('pdpurp == 1 and toexpfac == 1')
data['after'] = pd.read_csv(after_file, '\t').query('pdpurp == 1 and toexpfac == 1')

mode_share = {}
for i in data:
    mode_trips = data[i][['tmodetp', 'toexpfac']].groupby('tmodetp').sum()['toexpfac']
    mode_share[i] = mode_trips / mode_trips.sum()

mode_share = pd.DataFrame(mode_share)
print(mode_share)