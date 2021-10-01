import numpy as np

#def split_line(line):
#    return line.split('\t')

#split_lines = np.vectorize(split_line)

class df:

    def __init__(self, data, columns):
        self.columns = columns
        self.data = data

    @classmethod
    def from_file(cls, fp, delimiter = '\t'):

        f = open(fp, 'r')
        raw_data = f.read()
        lines = raw_data.split('\n')
        header = lines[0].split(delimiter)
        
        M = len(lines)-1
        N = len(header)

        data = np.reshape(raw_data.replace('\n', delimiter).split(delimiter)[:-1], (M, N))[1:,:].astype(float)

        return cls(data, header)

    def __getitem__(self, key):
        return self.data[:, self.columns.index(key)]

