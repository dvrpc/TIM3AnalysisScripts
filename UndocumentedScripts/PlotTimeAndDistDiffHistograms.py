import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

base_path = r'D:\TIM3'
files = {'NonPnR': 'NonPnRTripsWithVISUMSkims.csv',
         'PnR': 'PnRTripsWithVISUMSkimsReclassifyZones.csv'}

for f in files:
    print(f)
    df = pd.read_csv(os.path.join(base_path, files[f])).query('skimdist >= 3')

    #raise Exception

    plt.hist(df['timediff'], edgecolor = 'k')
    plt.title(f + ': Time Difference')
    plt.savefig(r'D:\TIM3\{}TimeDiffNotBlend.png'.format(f))
    plt.clf()

    plt.hist(df['distdiff'], edgecolor = 'k')
    plt.title(f + ': Distance Difference')
    plt.savefig(r'D:\TIM3\{}DistDiffNotBlend.png'.format(f))
    plt.clf()

    try:
        
        df = df.query('otaz != dtaz and mode != 6 and mode >= 3')

        plt.scatter(df['skimtime'], df['timediff'], color = 'k', s = 1, alpha = 0.5)
        plt.grid(True)
        plt.xlabel('Skim Time')
        plt.ylabel('Time Difference')
        plt.title(f + ' Auto Leg Trips')
        plt.savefig(r'D:\TIM3\{}InterzonalAutoSkimTimeVSTimeDiffNoBlend.png'.format(f))
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
        plt.savefig(r'D:\TIM3\{}InterzonalAutoSkimdDistVSDistDiffNoBlend.png'.format(f))
        plt.clf()

    except ValueError:
        pass

print('Done')