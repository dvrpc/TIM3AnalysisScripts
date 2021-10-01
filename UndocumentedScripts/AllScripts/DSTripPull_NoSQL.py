import os
import pandas as pd
import numpy as np

class TripSet:

    def __init__(self, mode, start, end, fac):

        self.mode = mode
        self.start = start
        self.end = end
        self.fac = fac

    def get(self, trips):
        return self.fac*(trips[(trips['mode'] == self.mode) & (trips['deptm'] >= self.start) & (trips['deptm'] <= self.end)][['otaz', 'dtaz', 'trexpfac']].groupby(['otaz', 'dtaz']).sum()['trexpfac'].reset_index().pivot('otaz', 'dtaz', 'trexpfac')).fillna(0)


zones = np.array(Visum.Net.Zones.GetMultiAttValues("No"))[:, 1]
N = len(zones)
    
def set_mat(no, trips, mtxs):
    Visum.Log(20480, 'Setting Matrix %d'%(no))
    global N, zones
    mat = pd.DataFrame(np.zeros((N, N)), zones, zones)
    for mtx in mtxs:
        mat += mtx.get(trips)
    Visum.Net.Matrices.ItemByKey(no).SetValues(mat.values)
    Visum.Log(20480, 'Matrix %d Set'%(no))

inpdir = Visum.GetPath(69)
tripfile = os.path.join(inpdir, 'Output', '_trip_2.dat')
Visum.Log(20480, 'Reading Trip File')
trip = pd.read_csv(tripfile, '\t')

ea = (0, 359)
am = (360, 599)
md = (600, 899)
pm = (900, 1139)
nt = (1140, 1439)

set_mat(101, trips, [TripSet(3, ea[0], ea[1], 1), TripSet(4, ea[0], ea[1], 0.5), TripSet(5, ea[0], ea[1], 0.3)])
set_mat(102, trips, [TripSet(3, am[0], am[1], 1), TripSet(4, am[0], am[1], 0.5), TripSet(5, am[0], am[1], 0.3)])
set_mat(103, trips, [TripSet(3, md[0], md[1], 1), TripSet(4, md[0], md[1], 0.5), TripSet(5, md[0], md[1], 0.3)])
set_mat(104, trips, [TripSet(3, pm[0], pm[1], 1), TripSet(4, pm[0], pm[1], 0.5), TripSet(5, pm[0], pm[1], 0.3)])
set_mat(105, trips, [TripSet(3, nt[0], nt[1], 1), TripSet(4, nt[0], nt[1], 0.5), TripSet(5, nt[0], nt[1], 0.3)])

set_mat(201, trips, [TripSet(6, ea[0], ea[1], 1)])
set_mat(202, trips, [TripSet(6, am[0], am[1], 1)])
set_mat(203, trips, [TripSet(6, md[0], md[1], 1)])
set_mat(204, trips, [TripSet(6, pm[0], pm[1], 1)])
set_mat(205, trips, [TripSet(6, nt[0], nt[1], 1)])

set_mat(221, trips, [TripSet(2, ea[0], ea[1], 1)])
set_mat(222, trips, [TripSet(2, am[0], am[1], 1)])
set_mat(223, trips, [TripSet(2, md[0], md[1], 1)])
set_mat(224, trips, [TripSet(2, pm[0], pm[1], 1)])
set_mat(225, trips, [TripSet(2, nt[0], nt[1], 1)])

set_mat(231, trips, [TripSet(1, ea[0], ea[1], 1)])
set_mat(232, trips, [TripSet(1, am[0], am[1], 1)])
set_mat(233, trips, [TripSet(1, md[0], md[1], 1)])
set_mat(234, trips, [TripSet(1, pm[0], pm[1], 1)])
set_mat(235, trips, [TripSet(1, nt[0], nt[1], 1)])