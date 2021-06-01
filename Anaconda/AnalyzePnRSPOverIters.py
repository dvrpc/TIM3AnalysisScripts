import pandas as pd
import numpy as np
import os

base_path = r'D:\TIM3.1\CalibrationJune2021\scenario\Output'
outfile = r'D:\TIM3\SPIterProgress0601_PSRCSettings.csv'
outfile_sp = r'D:\TIM3\PricesIter0601_PSRCSettings.csv'

#For this run, the outputs were copied to folders at the time that they finished
timestamps = ['2105281722',
              '2105281910',
              '2105282055',
              '2105282238',
              '2105290022',
              '2105290203',
              '2105290346',
              '2105290528',
              '2105290712',
              '2105290855',
              '2105291039',
              '2105291223',
              '2105291407']

mode_map = {3: 1, 4: 0.5, 5: 0.3} #Maps person trips to vehicle trips for auto modes
auto_modes = list(mode_map.keys()) #Gets a list of the auto modes

#Dictionaries to add a series to in each iteration. These will be converted to data frames at the end
pnr_loads = {}
sp_by_iter = {}

N = len(timestamps)
for i in range(N): #Iterate over every set of outputs in the timestamps
    print('Iter {}'.format(i+1))
    try:
        #Read in trip file
        trip_file = os.path.join(base_path, timestamps[i], '_trip_2.dat')
        trip = pd.read_csv(trip_file, '\t').query('dpurp == 10 and mode in @auto_modes') #Only use auto trips to PnR lot

        #Calculate number of vehicle trips based on mode and expansion factor, and group by destination PnR lot
        trip['veh_trips'] = trip['mode'].map(mode_map) * trip['trexpfac']
        pnr_loads['Iter {}'.format(i+1)] = trip[['dtaz', 'veh_trips']].groupby('dtaz').sum()['veh_trips']

        #Read in shadow price file
        sp_file = os.path.join(base_path, timestamps[i], 'park_and_ride_shadow_prices.txt')
        sp = pd.read_csv(sp_file, '\t', index_col = 0)

        #Initialize with empty data frame where the rows are the PnR lots and the columns are the minute of the day
        prices = pd.DataFrame(np.zeros((180, 1440)), index = range(1, 181))

        #Move shadow values from `sp` to `prices`
        for j in range(1440):
            if j < 10:
                prices[j] = sp['PRICE000' + str(j)]
            elif j < 100:
                prices[j] = sp['PRICE00' + str(j)]
            elif j < 1000:
                prices[j] = sp['PRICE0' + str(j)]
            else:
                prices[j] = sp['PRICE' + str(j)]

        #Add the highest penalty at each lot to `sp_by_iter`
        sp_by_iter['Iter {}'.format(i+1)] = pd.Series(-prices.min(1), prices.index)

    except IOError: #If files don't exist for the given timestamp, just move on to the next iteration
        continue


print('Writing')
pd.DataFrame(pnr_loads).fillna(0).to_csv(outfile)
pd.DataFrame(sp_by_iter).fillna(0).to_csv(outfile_sp)

print('Done')