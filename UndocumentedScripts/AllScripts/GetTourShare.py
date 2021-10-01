import pandas as pd

tour_file = r'D:\TIM3.1\CalibrationApril2021\scenario\Output\0423\_tour_2.dat'
tour = pd.read_csv(tour_file, '\t')

print(tour.groupby('tmodetp').sum()['toexpfac'])