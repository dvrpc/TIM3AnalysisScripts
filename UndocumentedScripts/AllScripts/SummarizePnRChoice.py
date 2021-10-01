import pandas as pd
import os

#Read in files
base_path = r'\\yoshi\modeling\TIM_3.1\DVRPC_ABM_Github\scenario\Output\Min Imp_SP_SA'
tours = pd.read_csv(os.path.join(base_path, '_tour_2.dat'), '\t')
trips = pd.read_csv(os.path.join(base_path, '_trip_2.dat'), '\t')

#Merge tour and trip files
tourtrip = tours.merge(trips, on = ['hhno', 'pno', 'day', 'tour'])

#Filter for transit trips (mode = 6) on PnR tours (tmodetp = 7) and group by origin stop area
pnr_otaz_counts = tourtrip[['tmodetp', 'mode', 'otaz']].query('tmodetp == 7 and mode == 6').groupby('otaz').count()

#Write out file
pnr_otaz_counts.to_csv(os.path.join(base_path, r'pnr_otaz_counts_3March.csv'))

print('Done')