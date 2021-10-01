import pandas
import numpy

base_path = Visum.GetPath(69)
person_file = os.path.join(base_path, 'Output', '_person_2.dat')
per = pandas.read_csv(person_file, '\t')

