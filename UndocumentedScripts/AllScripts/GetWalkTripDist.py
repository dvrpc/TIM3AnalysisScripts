import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

#infile = r'B:\model_development\TIM_3.1_Testing\scenario\Output\0528\_trip_2.dat'
infile = r'D:\TIM3.1\VersionWithSurveyData\scenario\Output\_trip_2.dat'
print('Reading Tour File')
tour = pd.read_csv(infile.replace('trip', 'tour'), '\t')
print('Reading Trip File')
trip = pd.read_csv(infile, '\t')
tourtrip = tour.merge(trip, on = ['hhno', 'pno', 'day', 'tour'])
#if walk['travdist'].max() > 2:
#    print('Walk trips over 2 miles!')
step = 0.05
max_dist = 2
bins = np.linspace(0, max_dist, int(max_dist*(1/step) + 1))
starts = bins[:-1]
ends = bins[1:]

plots = {'All Walk Trips': 'mode == 1',
         'Work Tours': 'mode == 1 and pdpurp == 1 and parent == 0',
         'School Tours': 'mode == 1 and pdpurp == 2 and parent == 0',
         'Escort Tours': 'mode == 1 and pdpurp == 3 and parent == 0',
         'Other HB Tours': 'mode == 1 and pdpurp > 3 and parent == 0',
         'Work-Based Tours': 'mode == 1 and parent == 1'}

outdata = pd.DataFrame()
outdata['Start'] = starts
outdata['End'] = ends

outpath = r'D:\TIM3\WalkDistsSurvey'

for plot_name in plots:
    print(plot_name)
    walk = tourtrip.query(plots[plot_name])
    plt.figure(figsize = (12, 6.75))
    plt.hist(walk['travdist'], bins, weights = walk['trexpfac'], facecolor = 'b', edgecolor = 'k')
    plt.grid(True)
    plt.xlabel('Distance (Miles)')
    plt.ylabel('# Trips')
    plt.title(plot_name)
    plt.savefig(os.path.join(outpath, 'WalkDistribution100_{}.png'.format(plot_name.replace(' ', '').replace('-', ''))))
    plt.clf()
    (hist, b) = np.histogram(walk['travdist'], bins, weights = walk['trexpfac'])
    outdata[plot_name] = hist

outdata.to_csv(os.path.join(outpath, 'WalkDistributions.csv'))
print('Done')