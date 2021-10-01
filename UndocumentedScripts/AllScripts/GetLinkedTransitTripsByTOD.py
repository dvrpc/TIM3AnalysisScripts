import pandas as pd

fp = r'T:\TIM_3.1\DVRPC_ABM_Testing\scenario\output\_trip_2.dat'
trip = pd.read_csv(fp, '\t')

def classify_time(args):
    if args[0] == 1:
        t = args[2]
    elif args[0] == 2:
        t = args[1]
    else:
        raise AssertionError, 'Tour half not 1 or 2'
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

