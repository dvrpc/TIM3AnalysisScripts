import pandas
import numpy
import os
from subprocess import Popen

def fix_time(t):
    hr = t // 100
    min = t % 100
    return (60*hr + min) % 1440

def classify_time_period(t):
    #half = args[0]
    #if half == 1:
    #    t = args[2]
    #elif half == 2:
    #    t = args[1]
    if t < 360:
        return 'NT'
    elif t < 600:
        return 'AM'
    elif t < 900:
        return 'MD'
    elif t < 1140:
        return 'PM'
    else:
        return 'NT'

need_to_fix_time = False
input_path = os.path.join(Visum.GetPath(69), 'inputs')
output_path = os.path.join(Visum.GetPath(69), 'Output')
report_path = os.path.join(Visum.GetPath(69), 'Reporting')
hh_file = os.path.join(output_path, '_household_2.dat')
tour_file = os.path.join(output_path, '_tour_2.dat')
tables = {}
tables['household'] = pandas.read_csv(hh_file, '\t')
tables['tour'] = pandas.read_csv(tour_file, '\t')

if need_to_fix_time:
    tables['tour']['tlvorig'] = tables['tour']['tlvorig'].apply(fix_time)
    tables['tour']['tardest'] = tables['tour']['tardest'].apply(fix_time)
    tables['tour']['tlvdest'] = tables['tour']['tlvdest'].apply(fix_time)
    tables['tour']['tarorig'] = tables['tour']['tarorig'].apply(fix_time)

tables['tour']['depart_tod'] = tables['tour']['tardest'].apply(classify_time_period)
tables['tour']['return_tod'] = tables['tour']['tlvdest'].apply(classify_time_period)

tables['tour']['hhtaz'] = tables['tour']['hhno'].map(tables['household'].set_index('hhno')['hhtaz'])
dvrpc = tables['tour'].query('hhtaz < 50000')

tours_by_depart_tod = dvrpc[['depart_tod', 'tmodetp', 'toexpfac']].groupby(['depart_tod', 'tmodetp']).sum()['toexpfac'].reset_index().pivot('tmodetp', 'depart_tod', 'toexpfac')
tours_by_return_tod = dvrpc[['return_tod', 'tmodetp', 'toexpfac']].groupby(['return_tod', 'tmodetp']).sum()['toexpfac'].reset_index().pivot('tmodetp', 'return_tod', 'toexpfac')

depart_outfile = os.path.join(report_path, 'TourModeShareByTOD_Depart.csv')
return_outfile = os.path.join(report_path, 'TourModeShareByTOD_Return.csv')

try:
    tours_by_depart_tod.to_csv(depart_outfile)
    tours_by_return_tod.to_csv(return_outfile)
except Exeption:
    os.mkdir(report_path)
    tours_by_depart_tod.to_csv(depart_outfile)
    tours_by_return_tod.to_csv(return_outfile)