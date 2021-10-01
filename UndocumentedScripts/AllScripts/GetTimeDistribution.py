import pandas as pd
trip = pd.read_csv(r'D:\TIM3.1\CenterCityScreenlineCalibration\scenario\Output\_trip_2.dat', '\t')

def t2tod(t):
    if t < 360:
        return '0000'
    elif t < 600:
        return '0600'
    elif t < 900:
        return '1000'
    elif t < 1140:
        return '1500'
    else:
        return '1900'

def classify_time(args):
    deptm = args[0]
    arrtm = args[1]
    half = args[2]
    if half == 1:
        return t2tod(arrtm)
    else:
        return t2tod(deptm)

trip['args'] = list(zip(trip['deptm'], trip['arrtm'], trip['half']))
trip['tod'] = trip['args'].apply(classify_time)

print(trip.groupby('tod').sum()['trexpfac'])