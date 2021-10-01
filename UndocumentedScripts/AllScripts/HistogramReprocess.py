'''
JJF 1 October 2020

The EI turnpike reports need to be run within the TOD versions files since the paths aren't loaded into the daily version.
This script renames them to reflect the TIM 2 TOD periods and adds the 0000 and 1900 periods into a single night period.
'''
import os
import pandas as pd

def rename_file(src, dst):
    src = src.replace('TravelTime', 'Distance')
    dst = dst.replace('TravelTime', 'Distance')
    successfully_completed = False
    while not successfully_completed:
        try:
            os.rename(src, dst)
            successfully_completed = True
        except WindowsError:
            os.remove(dst)

base_path = r'D:\TIM3.1\EITruckCalibrationOctober2020\scenario'
#rename_file(os.path.join(base_path, 'Report_HistsogramTravelTime_0600.csv'), os.path.join(base_path, 'Report_HistsogramTravelTime_AM.csv'))
#rename_file(os.path.join(base_path, 'Report_HistsogramTravelTime_1000.csv'), os.path.join(base_path, 'Report_HistsogramTravelTime_MD.csv'))
#rename_file(os.path.join(base_path, 'Report_HistsogramTravelTime_1500.csv'), os.path.join(base_path, 'Report_HistsogramTravelTime_PM.csv'))

data_0000 = pd.read_csv(os.path.join(base_path, 'Report_HistogramDistance_0000.csv'), index_col = 0)
data_1900 = pd.read_csv(os.path.join(base_path, 'Report_HistogramDistance_1900.csv'), index_col = 0)
data_NT = data_0000 + data_1900
data_NT.to_csv(os.path.join(base_path, 'Report_HistogramDistance_NT.csv'))

#Removing extra files
os.remove(os.path.join(base_path, 'Report_HistogramDistance_0000.csv'))
os.remove(os.path.join(base_path, 'Report_HistogramDistance_1900.csv'))