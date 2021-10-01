import csv
import time
import numpy

fp = r'T:\TIM_3.1\190712_FullTest\scenario\Output\_trip_2.dat'
#fp = r'D:\TIM3\DaySimOutputs1%\_trip_2.dat'

class df:
    def __init__(self, data, columns):
        self.data = data
        self.columns = columns

    @classmethod
    def from_file(cls, fp, delimiter):
       


        data = []
        f = open(fp, 'r')
        reader = csv.reader(f, delimiter = delimiter)
        for row in reader:
            data.append(row)

        columns = data[0]
        data = numpy.array(data[1:])

        return cls(data, columns)

    def __getitem__(self, key):
        ix = self.columns.index(key)
        return [row[ix] for row in self.data]


ts = time.time()
data = df.from_file(fp, '\t')
te = time.time()

print('{} seconds'.format(te - ts))