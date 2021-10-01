import numpy as np
import csv
import os

def classify_time(time):
    if int(time) < 6*60:
        return '0000'
    elif int(time) < 10*60:
        return '0600'
    elif int(time) < 15*60:
        return '1000'
    elif int(time) < 19*60:
        return '1500'
    else:
        return '1900'
classify_time = np.vectorize(classify_time)

trip_file = r'T:\TIM_3.1\190802_FullTest\scenario\Output\_trip_2.dat'
#trip_file = r'D:\TIM3\DaySimOutputs1%\_trip_2.dat'

trip_data = []
f = open(trip_file)
reader = csv.DictReader(f, delimiter = '\t')
columns = reader.fieldnames
for row in reader:
    if row['mode'] not in ['3', '4', '5']: #Not an auto trip
        continue
    trip_data.append([row['mode'], row['otaz'], row['dtaz'], row['deptm'], row['travdist'], row['trexpfac']])
f.close()

trip_data = np.array(trip_data)
trip_tod = classify_time(trip_data[:, 3])

N = trip_data.shape[0]

zones = Visum.Net.Zones.GetMultipleAttributes(['No']).astype(str)
dis = {'0000': np.array(Visum.Net.ODMatrices.ItemByKey(401).GetValues()),
       '0600': np.array(Visum.Net.ODMatrices.ItemByKey(402).GetValues()),
       '1000': np.array(Visum.Net.ODMatrices.ItemByKey(403).GetValues()),
       '1500': np.array(Visum.Net.ODMatrices.ItemByKey(404).GetValues()),
       '1900': np.array(Visum.Net.ODMatrices.ItemByKey(405).GetValues())}
#od = {'0000': np.array(Visum.Net.ODMatrices.ItemByKey(101).GetValues()),
#      '0600': np.array(Visum.Net.ODMatrices.ItemByKey(102).GetValues()),
#      '1000': np.array(Visum.Net.ODMatrices.ItemByKey(103).GetValues()),
#      '1500': np.array(Visum.Net.ODMatrices.ItemByKey(104).GetValues()),
#      '1900': np.array(Visum.Net.ODMatrices.ItemByKey(105).GetValues())}

outlabels = ['MODE', 'OTAZ', 'DTAZ', 'TOD', 'DAYSIMDIST', 'VISUMDIST', 'DISTDIFF', 'TREXPFAC']
outdata = np.empty((N, len(outlabels)), str)
for i in range(N):
    mode = trip_data[i][0]
    otaz = trip_data[i][1]
    dtaz = trip_data[i][2]
    tod = trip_tod[i]
    daysimdist = trip_data[i][4]
    visumdist = str(dis[tod][zones.index(otaz), zones.index(dtaz)])
    trexpfac = trip_data[i][5]
    outdata[i, :] = [mode, otaz, dtaz, tod, daysimdist, visumdist, '', trexpfac]

outdata[:, 6] = (outdata[:, 5].copy().astype(float) - outdata[:, 4].copy().astype(float)).astype(str)

outfile = r'T:\TIM_3.1\190802_FullTest\AutoTripDists.csv'
f = open(outfile, 'w')
f.write(','.join(outlabels) + '\n')
f.write('\n'.join([','.join(outdata[i]) for i in range(N)]))
f.close()

print('Go')