import numpy as np
import pandas as pd
import VisumPy.helpers as h

bins = np.arange(181)
ivt = h.GetMatrix(Visum, 302)
ei = h.GetMatrix(Visum, 141)
ei_long = h.GetMatrix(Visum, 142)

ei_hist = np.histogram(ivt, bins, weights = ei)[0]
ei_long_hist = np.histogram(ivt, bins, weights = ei_long)[0]

outdata = pd.DataFrame({'EI': ei_hist, 'EI_LONG': ei_long_hist})
outdata.to_csv(r'D:\TIM3\EI_Histogram.csv')
