import pandas as pd
import numpy as np
from subprocess import Popen

def negate(input):
    '''
    Not statement converted to a function so it can be an input to pandas.Series.apply()
    '''
    return not input

infile = r'D:\TIM3\TransitTripsWithBestSAs_191231.csv'
outfile = r'D:\TIM3\StopAreaChoiceSummary_191231_NoPnR.xlsx'
sa2mode_file = r'D:\ref\sa2mode.csv'

print('Reading Files')
sa2mode = pd.read_csv(sa2mode_file, index_col = 0)['MODE']
trip = pd.read_csv(infile, index_col = 0)

trip = trip.query('opurp != 10 and dpurp != 10')

print('Creating Fields')
#Checking if stop areas match
trip['o_match'] = trip['otaz'] == trip['osa']
trip['d_match'] = trip['dtaz'] == trip['dsa']
trip['od_match'] = trip['o_match'] & trip['d_match']
trip['od_mismatch'] = (trip['o_match'] | trip['d_match']).apply(negate)

#Identifying stop area mode
trip['omode_ds'] = trip['otaz'].map(sa2mode)
trip['dmode_ds'] = trip['dtaz'].map(sa2mode)
trip['omode_python'] = trip['osa'].map(sa2mode)
trip['dmode_python'] = trip['dsa'].map(sa2mode)

#Checking if stop area modes match
trip['omode_match'] = trip['omode_ds'] == trip['omode_python']
trip['dmode_match'] = trip['dmode_ds'] == trip['dmode_python']
trip['odmode_match'] = trip['omode_match'] & trip['dmode_match']
trip['odmode_mismatch'] = (trip['omode_match'] | trip['dmode_match']).apply(negate)

#Checking if subway stop areas chosen
trip['osub_ds'] = trip['omode_ds'] == 'Sub'
trip['dsub_ds'] = trip['dmode_ds'] == 'Sub'
trip['odsub_ds'] = trip['osub_ds'] & trip['dsub_ds']
trip['odnotsub_ds'] = (trip['osub_ds'] | trip['dsub_ds']).apply(negate)

trip['osub_python'] = trip['omode_python'] == 'Sub'
trip['dsub_python'] = trip['dmode_python'] == 'Sub'
trip['odsub_python'] = trip['osub_python'] & trip['dsub_python']
trip['odnotsub_python'] = (trip['osub_python'] | trip['dsub_python']).apply(negate)

#Checking if Patco stop areas chosen
trip['opat_ds'] = trip['omode_ds'] == 'Pat'
trip['dpat_ds'] = trip['dmode_ds'] == 'Pat'
trip['odpat_ds'] = trip['opat_ds'] & trip['dpat_ds']
trip['odnotpat_ds'] = (trip['opat_ds'] | trip['dpat_ds']).apply(negate)

trip['opat_python'] = trip['omode_python'] == 'Pat'
trip['dpat_python'] = trip['dmode_python'] == 'Pat'
trip['odpat_python'] = trip['opat_python'] & trip['dpat_python']
trip['odnotpat_python'] = (trip['opat_python'] | trip['dpat_python']).apply(negate)

print('Summarizing Data')
stop_matching = pd.DataFrame(np.empty((5, 1)), columns = ['#'],
                             index = ['Total Transit Trips',
                                      'Origin Stops Match',
                                      'Destination Stops Match',
                                      'Origin and Destination Stops Match',
                                      'Origin and Destination Stops Mismatch'])
stop_matching.loc['Total Transit Trips', '#'] = trip['trexpfac'].sum()
stop_matching.loc['Origin Stops Match', '#'] = trip[trip['o_match']]['trexpfac'].sum()
stop_matching.loc['Destination Stops Match', '#'] = trip[trip['d_match']]['trexpfac'].sum()
stop_matching.loc['Origin and Destination Stops Match', '#'] = trip[trip['od_match']]['trexpfac'].sum()
stop_matching.loc['Origin and Destination Stops Mismatch', '#'] = trip[trip['od_mismatch']]['trexpfac'].sum()
stop_matching['%'] = stop_matching['#'] / stop_matching.loc['Total Transit Trips', '#']

mode_matching = pd.DataFrame(np.empty((5, 1)), columns = ['#'],
                             index = ['Total Transit Trips',
                                      'Origin Modes Match',
                                      'Destination Modes Match',
                                      'Origin and Destination Modes Match',
                                      'Origin and Destination Modes Mismatch'])
mode_matching.loc['Total Transit Trips', '#'] = trip['trexpfac'].sum()
mode_matching.loc['Origin Modes Match', '#'] = trip[trip['omode_match']]['trexpfac'].sum()
mode_matching.loc['Destination Modes Match', '#'] = trip[trip['dmode_match']]['trexpfac'].sum()
mode_matching.loc['Origin and Destination Modes Match', '#'] = trip[trip['odmode_match']]['trexpfac'].sum()
mode_matching.loc['Origin and Destination Modes Mismatch', '#'] = trip[trip['odmode_mismatch']]['trexpfac'].sum()
mode_matching['%'] = mode_matching['#'] / mode_matching.loc['Total Transit Trips', '#']

def summarize_subway_choice(trip):
    output = pd.DataFrame(np.empty((3, 4)),
                          index = ['Subway Stops Chosen by Python Script',
                                   'Subway Stops Chosen by DaySim',
                                   'Subway Stops Chosen by Both'],
                          columns = ['Origin', 'Destination', 'Both', 'Neither'])
    output['Origin'] = [trip[trip['osub_python']]['trexpfac'].sum(),
                        trip[trip['osub_ds']]['trexpfac'].sum(),
                        trip[(trip['osub_python'] & trip['osub_ds'])]['trexpfac'].sum()]
    output['Destination'] = [trip[trip['dsub_python']]['trexpfac'].sum(),
                              trip[trip['dsub_ds']]['trexpfac'].sum(),
                              trip[(trip['dsub_python'] & trip['dsub_ds'])]['trexpfac'].sum()]
    output['Both'] = [trip[trip['odsub_python']]['trexpfac'].sum(),
                      trip[trip['odsub_ds']]['trexpfac'].sum(),
                      trip[(trip['odsub_python'] & trip['odsub_ds'])]['trexpfac'].sum()]
    output['Neither'] = [trip[trip['odnotsub_python']]['trexpfac'].sum(),
                         trip[trip['odnotsub_ds']]['trexpfac'].sum(),
                         trip[(trip['odnotsub_python'] & trip['odnotsub_ds'])]['trexpfac'].sum()]
    return output

def summarize_patco_choice(trip):
    output = pd.DataFrame(np.empty((3, 4)),
                          index = ['PATCO Stops Chosen by Python Script',
                                   'PATCO Stops Chosen by DaySim',
                                   'PATCO Stops Chosen by Both'],
                          columns = ['Origin', 'Destination', 'Both', 'Neither'])
    output['Origin'] = [trip[trip['opat_python']]['trexpfac'].sum(),
                        trip[trip['opat_ds']]['trexpfac'].sum(),
                        trip[(trip['opat_python'] & trip['opat_ds'])]['trexpfac'].sum()]
    output['Destination'] = [trip[trip['dpat_python']]['trexpfac'].sum(),
                              trip[trip['dpat_ds']]['trexpfac'].sum(),
                              trip[(trip['dpat_python'] & trip['dpat_ds'])]['trexpfac'].sum()]
    output['Both'] = [trip[trip['odpat_python']]['trexpfac'].sum(),
                      trip[trip['odpat_ds']]['trexpfac'].sum(),
                      trip[(trip['odpat_python'] & trip['odpat_ds'])]['trexpfac'].sum()]
    output['Neither'] = [trip[trip['odnotpat_python']]['trexpfac'].sum(),
                         trip[trip['odnotpat_ds']]['trexpfac'].sum(),
                         trip[(trip['odnotpat_python'] & trip['odnotpat_ds'])]['trexpfac'].sum()]
    return output

subway_choice_summary = summarize_subway_choice(trip)
am_subway_choice_summary = summarize_subway_choice(trip[trip['tod'] == 600])
patco_choice_summary = summarize_patco_choice(trip)
am_patco_choice_summary = summarize_patco_choice(trip[trip['tod'] == 600])

print('Writing Output')
try:
    writer = pd.ExcelWriter(outfile)
    stop_matching.to_excel(writer, 'Stop Matching')
    mode_matching.to_excel(writer, 'Mode Matching')
    subway_choice_summary.to_excel(writer, 'Subway Choice')
    am_subway_choice_summary.to_excel(writer, 'AM Subway Choice')
    patco_choice_summary.to_excel(writer, 'PATCO Choice')
    am_patco_choice_summary.to_excel(writer, 'AM PATCO Choice')
    writer.save()
except ImportError:
    stop_matching.to_csv(outfile.replace('.xlsx', '_StopMatching.csv'))
    mode_matching.to_csv(outfile.replace('.xlsx', '_ModeMatching.csv'))
    subway_choice_summary.to_csv(outfile.replace('.xlsx', '_SubwayChoice.csv'))
    am_subway_choice_summary.to_csv(outfile.replace('.xlsx', '_AMSubwayChoice.csv'))

print('Done')
Popen(outfile, shell = True)