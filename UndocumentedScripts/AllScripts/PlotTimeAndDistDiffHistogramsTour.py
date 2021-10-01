import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

base_path = r'D:\TIM3'
files = {'NonPnR': 'NonPnRTripsWithVISUMSkims.csv',
         'PnR': 'PnRTripsWithVISUMSkims.csv'}

files = {'Tours': 'ToursWithVISUMSkimsAvg.csv'}

auto_modes = [3, 4, 5]
qry = 'totaz != tdtaz and totaz < 50000 and tdtaz < 50000 and tmodetp in @auto_modes'

for f in files:
    print(f)
    df = pd.read_csv(os.path.join(base_path, files[f])).query(qry)

    plt.hist(df['timediff'], edgecolor = 'k')
    plt.title(f + ': Time Difference')
    plt.savefig(r'D:\TIM3\{}TimeDiff.png'.format(f))
    plt.clf()

    plt.hist(df['distdiff'], edgecolor = 'k')
    plt.title(f + ': Distance Difference')
    plt.savefig(r'D:\TIM3\{}DistDiff.png'.format(f))
    plt.clf()



    try:
        df = df.query('totaz != tdtaz and totaz < 50000 and tdtaz < 50000 and tmodetp != 6 and tmodetp >= 3')

        plt.scatter(df['skimtime'], df['timediff'], color = 'k', s = 1, alpha = 0.5)
        plt.grid(True)
        plt.xlabel('Skim Time')
        plt.ylabel('Time Difference')
        plt.title(f + ' Auto Leg Trips')
        plt.savefig(r'D:\TIM3\{}AutoSkimTimeVSTimeDiff.png'.format(f))
        plt.clf()

        plt.scatter(df['skimdist'], df['distdiff'], color = 'k', s = 1, alpha = 0.5)
        mn = df['distdiff'].min()
        mx = df['distdiff'].max()
        plt.plot(2*[3], [mn, mx], color = 'r', linewidth = 0.5, linestyle = '--')
        plt.grid(True)
        plt.xlabel('Skim Distance')
        plt.ylabel('Distance Difference')
        plt.ylim(mn, mx)
        plt.title(f + ' Auto Leg Trips')
        plt.savefig(r'D:\TIM3\{}AutoSkimdDistVSDistDiff.png'.format(f))
        plt.clf()

    except ValueError:
        pass

print('Done')