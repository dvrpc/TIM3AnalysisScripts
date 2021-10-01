import csv
import os

base_path = r'T:\TIM_3.1\TestInitialSteps_190324\scenario\Output'
district_file = os.path.join(os.path.split(base_path)[0], 'DaySimSummaries', 'data', 'county_districts.csv')
infile = os.path.join(base_path, '_tour_2.dat')
outfile = os.path.join(base_path, 'tour_county_flows_mode_purpose.csv')

