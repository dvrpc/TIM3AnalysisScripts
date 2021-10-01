from calibration_util import *

tables = {}
fps = [r'B:\model_development\TIM_3.1_OriginalCoefficients\scenario\Output\_trip_2.dat',
       r'B:\model_development\TIM_3.1\_trip_2.dat']
names = ['original', 'updated']

readers = []
for i in range(len(fps)):
    readers.append(TableReader(tables, fps[i], names[i], '\t'))
    readers.start()

for reader in readers:
    reader.join()

subway_taz_file = r'D:\ref\SubwayTAZs.txt'
