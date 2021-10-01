import pandas as pd
from subprocess import Popen

fp = r'B:\model_development\TIM_3.1_Testing\scenario\Output\0506\_tour_2.dat'
tour = pd.read_csv(fp, '\t').query('totaz >= 50000 and totaz < 60000 and tdtaz < 50000')
dests_by_zone = tour[['tdtaz', 'toexpfac']].groupby('tdtaz').sum()
outfile = r'D:\TIM3\EIDestsbyZone.csv'
dests_by_zone.to_csv(outfile)
Popen(outfile, shell = True)