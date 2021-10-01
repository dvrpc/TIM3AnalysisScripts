import pandas as pd
import time

infile = r'D:\TIM3\microzonetostopareadistance.dat'
outfile = r'D:\TIM3\readwritetimes.txt'

t0 = time.time()
df = pd.read_csv(infile, ' ')
t1 = time.time()
df.to_csv(infile, ' ')
t2 = time.time()

read_time = t1 - t0
write_time = t2 - t1

lines = ['Read:  %f seconds'%(round(read_time, 2)),
         'Write: %f seconds'%(round(write_time, 2))]

f = open(outfile, 'w')
f.write('\n'.join(lines))
f.close()