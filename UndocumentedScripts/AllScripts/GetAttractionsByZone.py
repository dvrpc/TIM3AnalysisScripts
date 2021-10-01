import pandas as pd
import numpy as np
from subprocess import Popen

print('Reading')
fp = r'D:\TIM3.1\EITruckCalibrationNovember2020\scenario\Output\_trip_2.dat'
trip = pd.read_csv(fp, '\t')

def get_attr_taz(args):
    otaz = args[0]
    dtaz = args[1]
    opurp = args[2]
    dpurp = args[3]

    if opurp == 10 or dpurp == 10:
        return 0

    if dpurp == 0:
        return otaz
    else:
        return dtaz

print('Getting Attractions')
trip['args'] = list(zip(trip['otaz'], trip['dtaz'], trip['opurp'], trip['dpurp']))
trip['ataz'] = trip['args'].apply(get_attr_taz)

print('Grouping By Attractions')
attr_by_taz = trip[['ataz', 'trexpfac']].groupby('ataz').sum()['trexpfac']

print('Writing File')
outfile = r'D:\TIM3\AttrByTAZ.csv'
attr_by_taz.to_csv(outfile)
Popen(outfile, shell = True)