import VisumPy.helpers as h
import numpy as np

time = h.GetMatrix(Visum, 221)
toll = h.GetMatrix(Visum, 261)
trips = h.GetMatrix(Visum, 2000)
h.SetMulti(Visum.Net.Zones, 'TIME_FROM_NJTP', time[-2, :])
h.SetMulti(Visum.Net.Zones, 'TIME_TO_NJTP', time[:, -2])
h.SetMulti(Visum.Net.Zones, 'TOLL_FROM_NJTP', toll[-2, :])
h.SetMulti(Visum.Net.Zones, 'TOLL_TO_NJTP', toll[:, -2])
h.SetMulti(Visum.Net.Zones, 'TRIPS_FROM_NJTP', trips[-2, :])
h.SetMulti(Visum.Net.Zones, 'TRIPS_TO_NJTP', trips[:, -2])
