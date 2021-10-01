import os
import csv
import numpy as np

base_path = r'T:\TIM_3.1\190712_FullTest\scenario\Output'
#base_path = r'D:\TIM3\SurveyData'
district_file = os.path.join(base_path, 'taz2district.csv')
trip_file = os.path.join(base_path, '_trip_2.dat')
#trip_file = os.path.join(base_path, 'dvrpc_tripx5.dat')
outfile = os.path.join(base_path, 'FreeTransitFlow.csv')

counties = ['Philadelphia', 'Delaware', 'Chester', 'Montgomery', 'Bucks',
            'Mercer', 'Burlington', 'Camden', 'Gloucester',
            'Extended PA', 'Extended NJ', 'Extended MD/DE']
county_flow = np.zeros(2*[len(counties)], float)

district2index = {'5':  0,
                  '3':  1,
                  '2':  2,
                  '4':  3,
                  '1':  4,
                  '9':  5,
                  '6':  6,
                  '7':  7,
                  '8':  8,
                  '10': 9,
                  '11': 10,
                  '12': 11}

taz2district = {}
f = open(district_file, 'r')
reader = csv.DictReader(f, delimiter = ',')
for row in reader:
    taz2district[row['TAZ']] = row['DISTRICT']
f.close()

f = open(trip_file, 'r')
reader = csv.DictReader(f, delimiter = '\t')
for row in reader:
    if row['mode'] != '6' or float(row['travcost']) > 0:
        continue
    if row['otaz'] == '0' or row['dtaz'] == '0':
        continue
    o = district2index[taz2district[row['otaz']]]
    d = district2index[taz2district[row['dtaz']]]
    county_flow[o, d] += float(row['trexpfac'])

lines = [',' + ','.join(counties)]
for i in range(len(counties)):
    new_line = [counties[i] + ',' + ','.join(county_flow[i, :].astype(str))]
    lines += new_line

f = open(outfile, 'w')
f.write('\n'.join(lines))
f.close()

print('Done')