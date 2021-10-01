import os
import csv
import numpy as np

base_path = r'T:\TIM_3.1\190712_FullTest\scenario\Output'
#base_path = r'D:\TIM3\DaySimOutputs1%'
per_file = os.path.join(base_path, '_person_2.dat')
trip_file = os.path.join(base_path, '_trip_2.dat')

#Read person file to create dictionary mapping whether or not each person has a transit pass
per2pass = {}
f = open(per_file, 'r')
reader = csv.DictReader(f, delimiter = '\t')
for row in reader:
    per2pass[row['hhno'] + '-' + row['pno']] = bool(int(row['ptpass']))
f.close()

#Create lists 
pass_costs = []
pass_weights = []
nopass_costs = []
nopass_weights = []

f = open(trip_file, 'r')
reader = csv.DictReader(f, delimiter = '\t')
for row in reader:
    if row['mode'] == '6': #Only get information for transit trips
        has_transit_pass = per2pass[row['hhno'] + '-' + row['pno']]
        if has_transit_pass: #Check if trip-maker has transit pass
            pass_costs.append(float(row['travcost']))
            pass_weights.append(float(row['trexpfac']))
        else:
            nopass_costs.append(float(row['travcost']))
            nopass_weights.append(float(row['trexpfac']))

#Create lists of costs and weights for all transit trips
all_costs = nopass_costs + pass_costs
all_weights = nopass_weights + pass_weights

pass_costs = np.array(pass_costs)
pass_weights = np.array(pass_weights)
nopass_costs = np.array(nopass_costs)
nopass_weights = np.array(nopass_weights)
all_costs = np.array(all_costs)
all_weights = np.array(all_weights)

pass_no_cost    = ((pass_costs == 0) * pass_weights).sum()
pass_w_cost     = ((pass_costs != 0) * pass_weights).sum()
nopass_no_cost  = ((nopass_costs == 0) * nopass_weights).sum()
nopass_w_cost   = ((nopass_costs != 0) * nopass_weights).sum()

all_no_cost = pass_no_cost + nopass_no_cost
all_w_cost = pass_w_cost + nopass_w_cost

print('Tripmaker Has Transit Pass')
print('# With No Cost: ' + str(pass_no_cost))
print('# With Cost:    ' + str(pass_w_cost))
print('% With No Cost: ' + str(100 * pass_no_cost / (pass_no_cost + pass_w_cost)) + '%')
print('Average Cost:   ' + str(np.average(pass_costs, weights = pass_weights)))
print('\n')
print('Tripmaker Does Not Have Transit Pass')
print('# With No Cost: ' + str(nopass_no_cost))
print('# With Cost:    ' + str(nopass_w_cost))
print('% With No Cost  ' + str(100 * nopass_no_cost / (nopass_no_cost + nopass_w_cost)) + '%')
print('Average Cost:   ' + str(np.average(nopass_costs, weights = nopass_weights)))
print('\n')
print('All Transit Trips')
print('# With No Cost: ' + str(all_no_cost))
print('# With Cost:    ' + str(all_w_cost))
print('% With No Cost: ' + str(100 * all_no_cost / (all_no_cost + all_w_cost)) + '%')
print('Average Cost:   ' + str(np.average(all_costs, weights = all_weights)))