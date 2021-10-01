import os
import csv
import numpy as np
#import pandas as pd

#base_path = r'T:\TIM_3.1\190712_FullTest\scenario\Output'
base_path = r'D:/TIM3/SurveyData'
#per_file = os.path.join(base_path, '_person_2.dat')
#trip_file = os.path.join(base_path, '_trip_2.dat')
per_file = os.path.join(base_path, 'dvrpc_precx5.dat')
trip_file = os.path.join(base_path, 'dvrpc_tripx5.dat')

per2pass = {}
f = open(per_file, 'r')
reader = csv.DictReader(f, delimiter = ' ')
for row in reader:
    per2pass[row['ï»¿hhno'] + '-' + row['pno']] = bool(int(row['ptpass']))
f.close()

pass_costs = []
pass_weights = []
nopass_costs = []
nopass_weights = []

f = open(trip_file, 'r')
reader = csv.DictReader(f, delimiter = ' ')
for row in reader:
    if row['mode'] == '6':
        if per2pass[row['ï»¿hhno'] + '-' + row['pno']]:
            pass_costs.append(float(row['travcost']))
            pass_weights.append(float(row['trexpfac']))
        else:
            nopass_costs.append(float(row['travcost']))
            nopass_weights.append(float(row['trexpfac']))

pass_avg = np.average(pass_costs, weights = pass_weights)
nopass_avg = np.average(nopass_costs, weights = nopass_weights)

print('Pass:    {}'.format(pass_avg))
print('No Pass: {}'.format(nopass_avg))