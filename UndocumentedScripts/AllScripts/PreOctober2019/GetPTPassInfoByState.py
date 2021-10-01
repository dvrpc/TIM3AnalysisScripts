import os
import csv
import numpy as np

base_path = r'T:\TIM_3.1\190712_FullTest\scenario\Output'
#base_path = r'D:\TIM3\DaySimOutputs1%'
per_file = os.path.join(base_path, '_person_2.dat')
trip_file = os.path.join(base_path, '_trip_2.dat')
district_file = os.path.join(base_path, 'taz2district.csv')

district2state = {'1': 'PA',
                  '2': 'PA',
                  '3': 'PA',
                  '4': 'PA',
                  '5': 'PA',
                  '6': 'NJ',
                  '7': 'NJ',
                  '8': 'NJ',
                  '9': 'NJ',
                  '10': 'EXT',
                  '11': 'EXT',
                  '12': 'EXT'}

taz2district = {}
f = open(district_file, 'r')
reader = csv.DictReader(f, delimiter = ',')
for row in reader:
    taz2district[row['TAZ']] = row['DISTRICT']
f.close()

#Read person file to create dictionary mapping whether or not each person has a transit pass
per2pass = {}
f = open(per_file, 'r')
reader = csv.DictReader(f, delimiter = '\t')
for row in reader:
    per2pass[row['hhno'] + '-' + row['pno']] = bool(int(row['ptpass']))
f.close()

#Create lists 
pass_costs = {'PA': [], 'NJ': []}
pass_weights = {'PA': [], 'NJ': []}
nopass_costs = {'PA': [], 'NJ': []}
nopass_weights = {'PA': [], 'NJ': []}
all_costs = {}
all_weights = {}

f = open(trip_file, 'r')
reader = csv.DictReader(f, delimiter = '\t')
for row in reader:
    state = district2state[taz2district[row['otaz']]]
    if state not in pass_costs.keys():
        continue
    if row['mode'] == '6': #Only get information for transit trips
        has_transit_pass = per2pass[row['hhno'] + '-' + row['pno']]
        if has_transit_pass: #Check if trip-maker has transit pass
            pass_costs[state].append(float(row['travcost']))
            pass_weights[state].append(float(row['trexpfac']))
        else:
            nopass_costs[state].append(float(row['travcost']))
            nopass_weights[state].append(float(row['trexpfac']))
            
pass_no_cost = {}
pass_w_cost = {}
nopass_no_cost = {}
nopass_w_cost = {}
all_no_cost = {}
all_w_cost = {}

for state in ['PA', 'NJ']:
#Create lists of costs and weights for all transit trips
    all_costs[state] = nopass_costs[state] + pass_costs[state]
    all_weights[state] = nopass_weights[state] + pass_weights[state]

    pass_costs[state] = np.array(pass_costs[state])
    pass_weights[state] = np.array(pass_weights[state])
    nopass_costs[state] = np.array(nopass_costs[state])
    nopass_weights[state] = np.array(nopass_weights[state])
    all_costs[state] = np.array(all_costs[state])
    all_weights[state] = np.array(all_weights[state])

    pass_no_cost[state]    = ((pass_costs[state] == 0) * pass_weights[state]).sum()
    pass_w_cost[state]     = ((pass_costs[state] != 0) * pass_weights[state]).sum()
    nopass_no_cost[state]  = ((nopass_costs[state] == 0) * nopass_weights[state]).sum()
    nopass_w_cost[state]   = ((nopass_costs[state] != 0) * nopass_weights[state]).sum()

    all_no_cost[state] = pass_no_cost[state] + nopass_no_cost[state]
    all_w_cost[state] = pass_w_cost[state] + nopass_w_cost[state]

    print('\n\n' + state + '\n')

    print('Tripmaker Has Transit Pass')
    print('# With No Cost: ' + str(pass_no_cost[state]))
    print('# With Cost:    ' + str(pass_w_cost[state]))
    print('% With No Cost: ' + str(100 * pass_no_cost[state] / (pass_no_cost[state] + pass_w_cost[state])) + '%')
    print('Average Cost:   ' + str(np.average(pass_costs[state], weights = pass_weights[state])))
    print('\n')
    print('Tripmaker Does Not Have Transit Pass')
    print('# With No Cost: ' + str(nopass_no_cost[state]))
    print('# With Cost:    ' + str(nopass_w_cost[state]))
    print('% With No Cost  ' + str(100 * nopass_no_cost[state] / (nopass_no_cost[state] + nopass_w_cost[state])) + '%')
    print('Average Cost:   ' + str(np.average(nopass_costs[state], weights = nopass_weights[state])))
    print('\n')
    print('All Transit Trips')
    print('# With No Cost: ' + str(all_no_cost[state]))
    print('# With Cost:    ' + str(all_w_cost[state]))
    print('% With No Cost: ' + str(100 * all_no_cost[state] / (all_no_cost[state] + all_w_cost[state])) + '%')
    print('Average Cost:   ' + str(np.average(all_costs[state], weights = all_weights[state])))