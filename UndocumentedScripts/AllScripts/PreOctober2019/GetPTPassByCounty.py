import os
import numpy as np
import pandas as pd

#Define input and output files
base_path = r'Y:\TIM_3.1\DVRPC_ABM_VISUM18patch\scenario\Output'
#base_path = r'D:/TIM3/SurveyData'
hh_file = os.path.join(base_path, '_household_2.dat')
per_file = os.path.join(base_path, '_person_2.dat')
#hh_file = os.path.join(base_path, 'dvrpc_hrecx4.dat')
#per_file = os.path.join(base_path, 'dvrpc_precx5.dat')
taz_file = os.path.join(base_path, 'taz2county.csv')
outfile = os.path.join(base_path, 'TransitPassShareByCounty.csv')

delimiter = '\t' #Household file delimiter

#Create dictionary to map TAZ to CPA
taz2cpa = {}
f = open(taz_file, 'r')
lines = f.read().split('\n')
f.close()

for line in lines[1:-1]:
    taz_cpa_pair = line.split(',')
    taz2cpa[taz_cpa_pair[0]] = (taz_cpa_pair[1])

#Create list of CPAs and series to add up number of transit pass owners and overall population
#cpa_list = list(set(taz2cpa.values()))
#cpa_list.sort()
cpa_list = ['Philadelphia', 'Delaware', 'Chester', 'Montgomery', 'Bucks', 'Mercer', 'Burlington', 'Camden', 'Gloucester', 'Rest of PA', 'Rest of NJ', 'Rest of Outer Counties']

cpa_pass = pd.Series((np.zeros_like(cpa_list, float)), index = cpa_list)
cpa_pop = pd.Series((np.zeros_like(cpa_list, float)), index = cpa_list)

#Create dictionary to map household number to TAZ
hh2taz = {}
f = open(hh_file, 'r')
lines = f.read().split('\n')
f.close()
#Identify indices for needed values
header = lines[0].split(delimiter)
hhno = header.index('hhno')
hhtaz = header.index('hhtaz')

for line in lines[1:-1]:
    hh = line.split(delimiter)
    hh2taz[hh[hhno]] = hh[hhtaz]

delimiter = '\t' #Person file delimiter

#Open person file
f = open(per_file, 'r')
lines = f.read().split('\n')
f.close()

#Identify indices for needed values
header = lines[0].split(delimiter)
hhno = header.index('hhno')
ptpass = header.index('ptpass')
psexpfac = header.index('psexpfac')

ke = 0

for line in lines[1:-1]:
    per = line.split(delimiter)
    #try:
    cpa = taz2cpa[hh2taz[per[hhno]]]
    cpa_pass[cpa] += (float(per[ptpass])*float(per[psexpfac])) #Add if person owns transit pass
    cpa_pop[cpa] += float(per[psexpfac]) #Add to total population
    #except KeyError:
    #    ke += 1
    #    continue

ownership_by_cpa = cpa_pass / cpa_pop
ownership_by_cpa.to_csv(outfile)

print('Done with {} KeyErrors'.format(ke))