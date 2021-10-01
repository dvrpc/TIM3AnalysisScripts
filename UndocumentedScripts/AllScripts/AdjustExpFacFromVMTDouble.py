import pandas as pd
import os

base_path = r'D:\TIM3.1\EITruckCalibrationOctober2020\scenario\Output'
hh_file = os.path.join(base_path, '_household_2.dat')
trip_file = os.path.join(base_path, '_trip_2.dat')

adj = {}
for i in range(4000): #Philadelphia
    adj[i] = 1.130148846
for i in range(4000, 6000): #Delaware
    adj[i] = 0.923675202
for i in range(6000, 10000): #Chester
    adj[i] = 0.853038738
for i in range(10000, 14000): #Montgomery
    adj[i] = 0.877406934
for i in range(14000, 18000): #Bucks
    adj[i] = 0.937017792
for i in range(18000, 20000): #Mercer
    adj[i] = 1.025413689
for i in range(20000, 22000): #Burlington
    adj[i] = 0.997328967
for i in range(22000, 24000): #Camden
    adj[i] = 1.155831177
for i in range(24000, 26000): #Gloucester
    adj[i] = 1.143730772
for i in range(26000, 100040): #Other
    adj[i] = 1

adj = pd.Series(adj)
adj2 = 1 + 2*(adj-1)

print('Reading')
hh = pd.read_csv(hh_file, '\t')
trip = pd.read_csv(trip_file, '\t')

print('Arithmetic')
trip['hhtaz'] = trip['hhno'].map(hh.set_index('hhno')['hhtaz'])
trip['adj'] = trip['hhtaz'].map(adj2)
trip['trexpfac'] *= trip['adj']

print('Writing')
trip.to_csv(trip_file, '\t', index = False)

print('Done')