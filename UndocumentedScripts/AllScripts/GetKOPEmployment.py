import pandas as pd
import numpy as np

per_file = r'D:\TIM3.1\PhoenixvilleSensitivityTest\SP\scenario\Output\_person_2.dat'
per = pd.read_csv(per_file, '\t')

kop_tazs = [8019, 8026, 8028, 10209] + list(range(10211, 10216)) + list(range(10219, 10224))
work_in_kop = per.query('pwtaz in @kop_tazs')

print(work_in_kop['psexpfac'].sum())