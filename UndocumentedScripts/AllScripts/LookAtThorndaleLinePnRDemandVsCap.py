from __future__ import division
import pandas as pd
import os

infile = r'D:\TIM3\PnRDemandVsCAP.csv'
data = pd.read_csv(infile)

pnr_zones = [90045, 90088, 90101, 90095, 90165, 90163, 90148, 90109, 90029, 90009, 90155, 90151, 90020, 90077, 90167, 90156, 90170, 90136, 90002, 90001, 90132, 90048]

thorndale = data.query('Zone in @pnr_zones')

print(thorndale.sum(0))