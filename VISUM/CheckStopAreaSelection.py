'''
This script looks at DaySim's chosen stop areas for a transit trip and replicates the calculation based on the skims in VISUM
'''
from __future__ import division
import pandas as pd
import numpy as np
from numpy import inf
import os
from Util import WriteToTrace

#Set file locations
base_path = os.path.join(os.path.split(os.path.split(__file__)[0])[0], 'scenario')
trip_file = os.path.join(base_path, 'Output', 'SA_NoWalkSA', '_trip_2.dat') #Must be a trip file where the stop areas are written for transit trips
hh_file = trip_file.replace('trip', 'household')
tour_file = trip_file.replace('trip', 'tour')
maz2sa_file = os.path.join(base_path, 'microzonetostopareadistance.dat')
outfile = os.path.join(base_path, 'TransitTripsWithBestSAs.csv')

skim_base = {'0000': 'PuTSkim_0.00-6.00',
             '0600': 'PuTSkim_6.00-10.00',
             '1000': 'PuTSkim_10.00-15.00',
             '1500': 'PuTSkim_15.00-19.00',
             '1900': 'PuTSkim_19.00-0.00'}

tods = list(skim_base.keys())

skim_extension = {'Fare': '.FAR',
                  'IVT': '.IVT',
                  'BRT IVT': '.IVTT(BRT)',
                  #'Bus IVT': '.IVTT(Bus)',
                  'LRT IVT': '.IVTT(LRT)',
                  'PATCO IVT': '.IVTT(Pat)',
                  'RR IVT': '.IVTT(RR)',
                  'Sub IVT': '.IVTT(Sub)',
                  #'Trl IVT': '.IVTT(Trl)',
                  'BRD': '.BRD',
                  'OWTA': '.OWTA',
                  #'SFQ': '.SFQ',
                  'TWT': '.TWT.WKT'}
                  #'WKT': '.WKT'}

skim_list = list(skim_extension.keys())

StopAreas = np.array(Visum.Net.StopAreas.GetMultiAttValues("No"))[:,1]

skim_weights = {'Fare': 3,
                'IVT': 1,
                'BRT IVT': -0.05,
                #'Bus IVT': 0,
                'LRT IVT': -0.15,
                'PATCO IVT': -0.2,
                'RR IVT': -0.35,
                'Sub IVT': -0.2,
                #'Trl IVT': 0,
                'BRD': 5,
                'OWTA': 2.5,
                'TWT': 2.5,
                'WKT': 1}

walk_minutes_per_mile = 20
ovt_weight = 1
BaseCostCoefficientIncomeLevel = 30000
BaseCostCoefficientPerMonetaryUnit = -0.15


### Utility Functions ###

def read_skim(time, skim):
    '''
    Reads a stop area skim for a specified time period into a pandas data frame

    Parameters
    ----------
    time (str): The length-4 string representing the time period for the skim
    skim (str): The skim name. Must be a key of the global varialbe `skim_extention`

    Returns
    -------
    transit_skim (pandas.DataFrame): A data frame where the index and columns are the list of stop areas and the values are the values of the stop area skim
    '''
    global base_path, StopAreas, skim_base, skim_extension
    try:
        Visum.Net.AddMatrix(10000, objectTypeRef=4, MatrixType=4)
    except Exception:
        pass
    mat = Visum.Net.Matrices.ItemByKey(10000)
    mat.Init()
    mat.Open(os.path.join(base_path, skim_base[time] + skim_extension[skim]), ReadAdditive=True)
    if skim == 'NTR':
        return pd.DataFrame(np.array(mat.GetValuesFloat()) + 1, index = StopAreas, columns = StopAreas)
    else:
        return pd.DataFrame(np.array(mat.GetValuesFloat()), index = StopAreas, columns = StopAreas)

def classify_time(time):
    '''
    Classifies a time period based on a time in minutes after midnight

    Parameters
    ----------
    time (int): Time in minutes after midnight

    Returns
    -------
    time_period (str): A length-4 string representing the time period that the input time falls into
    '''
    if time < 360:
        return '0000'
    elif time < 600:
        return '0600'
    elif time < 900:
        return '1000'
    elif time < 1140:
        return '1500'
    else:
        return '1900'

#### MAIN SCRIPT ####

WriteToTrace(Visum, 'Reading MAZ to SA skim')
maz2sa = pd.read_csv(maz2sa_file, ' ')
maz2sa['WalkTime'] = maz2sa['distance'] / 5280 * walk_minutes_per_mile
maz2sa['maz-sa'] = list(zip(maz2sa['zoneid'], maz2sa['stopareaid']))
get_walk_time = maz2sa.set_index('maz-sa')['WalkTime'] #Used to get walk time from maz-stop area pair

WriteToTrace(Visum, 'Reading household file to get household incomes')
hh2inc = pd.read_csv(hh_file, '\t').set_index('hhno')['hhincome']

WriteToTrace(Visum, 'Reading tour file to get tour purposes')
tour = pd.read_csv(tour_file, '\t')
tour['tourid'] = list(zip(tour['hhno'], tour['pno'], tour['tour']))
tour2purp = tour.set_index('tourid')['pdpurp']

WriteToTrace(Visum, 'Reading trip file and removing non-walk to transit trips')
trip = pd.read_csv(trip_file, '\t').query('mode == 6 and opurp != 10 and dpurp != 10')
trip['hhincome'] = trip['hhno'].map(hh2inc)
trip['tourid'] = list(zip(trip['hhno'], trip['pno'], trip['tour']))
trip['pdpurp'] = trip['tourid'].map(tour2purp)
trip['reftm'] = (trip['half'] == 1)*trip['arrtm'] + (trip['half'] == 2)*trip['deptm']
trip['tod'] = trip['reftm'].apply(classify_time)

WriteToTrace(Visum, 'Calculating Tour Cost Coefficients')
trip['incomePower'] = 0.5*np.ones_like(trip.index)
trip[trip['pdpurp'] == 1]['incomePower'] *= 1.2
trip['incomeMultiple'] = trip['hhincome'] / BaseCostCoefficientIncomeLevel
trip['tourCostCoefficient'] = BaseCostCoefficientPerMonetaryUnit / np.power(trip['incomeMultiple'], trip['incomePower'])

WriteToTrace(Visum, 'Calculating Tour Time Coefficients')
purp2coeff = {}
for i in range(10):
    if i == 1:
        purp2coeff[i] = -0.02
    else:
        purp2coeff[i] = -0.01
trip['tourTimeCoefficient'] = trip['pdpurp'].map(purp2coeff)

trip['odpair'] = list(zip(trip['opcl'], trip['dpcl'], trip['tod'], trip['tourCostCoefficient'], trip['tourTimeCoefficient']))

trip = trip.query('tod == "0600"')

N = len(StopAreas)

WriteToTrace(Visum, 'Reading Skims')
TransitSkims = {}
Fares = {}
separated_skims = {}
for tod in tods:
    if tod != '0600':
        continue
    WriteToTrace(Visum, 'Reading TOD ' + tod)
    tod_skim = pd.DataFrame(np.zeros((N, N), float), index = StopAreas, columns = StopAreas)
    separated_skims[tod] = {}
    for skim in skim_list:
        WriteToTrace(Visum, 'Reading ' + skim)
        if skim == 'Fare':
            Fares[tod] = read_skim(tod, skim)
        else:
            skim_values = read_skim(tod, skim)
            separated_skims[tod][skim] = skim_values
            tod_skim += (skim_weights[skim] * skim_values)
    TransitSkims[tod] = tod_skim
WriteToTrace(Visum, 'Skims Read')

def get_best_sa_pair(od_pair, trace = False):
    '''
    Identifies the best origin and destination stop areas for given dorigin and destination MAZs and time of day by using the walk distances from the MAZs to the stop areas and the stop area skims

    Parameters
    ----------
    od_pair (tuple): Length-3 tuple with the origin MAZ (int), the destination MAZ (int), and the time period of the trip (str)

    Returns
    -------
    osa (int): Best origin stop area
    dsa (int): Best destination stop area
    pjt (int): Perceived journey time for the input origin MAZ to the best origin stop area to the best destination stop area to the input destination MAZ
    '''
    global maz2sa, TransitSkims, ovt_weight, Fares, separated_skims, base_path
    omaz = od_pair[0]
    dmaz = od_pair[1]
    tod = od_pair[2]
    tourCostCoefficient = od_pair[3]
    tourTimeCoefficient = od_pair[4]

    #Filter maz to stmazop area data for the origin and destination MAZs
    osa_info = maz2sa[maz2sa['zoneid'] == omaz]
    dsa_info = maz2sa[maz2sa['zoneid'] == dmaz]

    #Get arrays of stop areas accessible to origin and destination
    osas = osa_info['stopareaid'].values
    dsas = dsa_info['stopareaid'].values

    #Create OVT matrix where the number of rows is the number of stop areas accessible to the origin and the number of columns is the number of stop areas accessible to the destination
    access_times = osa_info[['WalkTime']].values
    egress_times = dsa_info[['WalkTime']].values.T
    ovt = np.log(np.dot(np.exp(access_times), np.exp(egress_times)))

    #Calculate transit utility
    utility = tourCostCoefficient*Fares[tod].loc[osas][dsas] + tourTimeCoefficient*(TransitSkims[tod].loc[osas][dsas] + ovt_weight*ovt)

    #Create perceived journey time matrix for every accessible stop area pair for the origin and destination MAZs and melt it into a single series
    utility = pd.melt((utility).reset_index(), id_vars = ['index'], value_vars = list(dsas))

    if trace: #Write out results for every accessible origin and destination stop areas for the od-pair
        WriteToTrace(Visum, 'Tracing from {0} to {1}'.format(omaz, dmaz))
        PathChoiceScaleFactor = 1.5

        ivt  = separated_skims[tod]['IVT'].loc[osas][dsas]
        owta = separated_skims[tod]['OWTA'].loc[osas][dsas]
        twt  = spearated_skims[tod]['TWT'].loc[osas][dsas]
        brd  = separated_skims[tod]['BRD'].loc[osas][dsas]

        path_specific_ivt = {}
        path_specific_ivt['BRT IVT']   = separated_skims[tod]['BRT IVT'].loc[osas][dsas]
        path_specific_ivt['LRT IVT']   = separated_skims[tod]['LRT IVT'].loc[osas][dsas]
        path_specific_ivt['PATCO IVT'] = separated_skims[tod]['PATCO IVT'].loc[osas][dsas]
        path_specific_ivt['RR IVT']    = separated_skims[tod]['RR IVT'].loc[osas][dsas]
        path_specific_ivt['Sub IVT']   = separated_skims[tod]['Sub IVT'].loc[osas][dsas]

        pathTypeSpecificTime = pd.DataFrame(np.zeros_like(ivt), osas, dsas)
        for mode_ivt in ['BRT IVT', 'LRT IVT', 'PATCO IVT', 'RR IVT', 'Sub IVT']:
            pathTypeSpecificTime += (skim_weights[mode_ivt]*path_specific_ivt[mode_ivt])

        tpt = ivt + owta
        tpc = Fares[tod].loc[osas][dsas]
        twt = ovt.copy()
        ttc = pd.DataFrame(tourTimeCoefficient*np.ones_like(twt), index = osas, columns = dsas)
        tcc = pd.DataFrame(tourCostCoefficient*np.ones_like(twt), index = osas, columns = dsas)

        fpu = PathChoiceScaleFactor*(0 + tcc*tpc + ttc*(skim_weights['IVT']*ivt + skim_weights['OWTA']*owta + skim_weights['TWT']*twt + skim_weights['BRD']*brd + pathTypeSpecificTime))
        tpu = fpu + PathChoiceScaleFactor*tcc*ovt_weight*twt

        O = len(osas)
        D = len(dsas)
        N = O*D
        trace_out = pd.DataFrame(index = range(N))
        trace_out['OMAZ'] = N*[omaz]
        trace_out['DMAZ'] = N*[dmaz]
        trace_out['OSA']  = np.repeat(osas, D)
        trace_out['DSA']  = O*list(dsas)
        trace_out['FPU']  = np.reshape(fpu.values, N)
        trace_out['TPT']  = np.reshape(tpt.values, N)
        trace_out['TWT']  = np.reshape(twt.values, N)
        trace_out['TPU']  = np.reshape(tpu.values, N)
        trace_out['TPT']  = np.reshape(tpt.values, N)
        trace_out['TTC']  = np.reshape(ttc.values, N)
        trace_out['TCC']  = np.reshape(tcc.values, N)
        trace_out['PTST'] = np.reshape(PathTypeSpecificTime.values, N)

        trace_outfile = os.path.join(base_path, 'TransitPathTrace{0}-{1}.csv'.format(omaz, dmaz))
        trace_out.to_csv(trace_outfile)
        WriteToTrace(Visum, 'Trace outfile written')

    #Identify the origin and stop area pairs with the lowest perceived journey time, and return the origin stop area, the destination stop area, and the perceived journey time
    best_trips = utility[utility['value'] == utility['value'].max()]
    n_trips = len(best_trips.index)
    if n_trips == 0:
        return (0,0, inf)
    else:
        return (best_trips.iloc[0]['index'], best_trips.iloc[0]['variable'], best_trips.iloc[0]['value'])

def get_transit_time(inputs):
    '''
    Obtains the transit time for a given time of day and origin and destination stop areas

    Parameters
    ----------
    inputs (tuple): Length-3 tuple with the time period (str), origin stop area (int), and destination stop area (int)

    Returns
    -------
    time (float): Perceived journey time from the origin stop area to the destination stop area during the given time period
    '''
    global TransitSkims
    tod = inputs[0]
    osa = inputs[1]
    dsa = inputs[2]
    return TransitSkims[tod].loc[osa, dsa]

def get_fare(inputs):
    '''
    Obtains the transit fare for a given time of day and origin and destination stop areas

    Parameters
    ----------
    inputs (tuple): Length-3 tuple with the time period (str), origin stop area (int), and destination stop area (int)

    Returns
    -------
    fare (float): Fare from the origin stop area to the destination stop area during the given time period
    '''
    global Fares
    tod = inputs[0]
    osa = inputs[1]
    dsa = inputs[2]
    return Fares[tod].loc[osa, dsa]

WriteToTrace(Visum, 'Finding Best Stop Areas')
trip['odsa'] = trip['odpair'].apply(get_best_sa_pair)
trip['osa'] = trip['odsa'].apply(lambda x: x[0])
trip['dsa'] = trip['odsa'].apply(lambda x: x[1])
trip['utility'] = trip['odsa'].apply(lambda x: x[2])

WriteToTrace(Visum, 'Calculating DaySim Utilities')
trip['omaz-osa'] = list(zip(trip['opcl'], trip['otaz']))
trip['dmaz-dsa'] = list(zip(trip['dpcl'], trip['dtaz']))
trip['tod-osa-dsa'] = list(zip(trip['tod'], trip['otaz'], trip['dtaz']))
trip['access_time'] = trip['omaz-osa'].map(get_walk_time)
trip['egress_time'] = trip['dmaz-dsa'].map(get_walk_time)
trip['transit_time'] = trip['tod-osa-dsa'].apply(get_transit_time)
trip['fare'] = trip['tod-osa-dsa'].apply(get_fare)
trip['utility_daysim'] = trip['tourTimeCoefficient']*(ovt_weight*trip['access_time'] + trip['transit_time'] + ovt_weight*trip['egress_time']) + trip['tourCostCoefficient']*trip['fare']
trip['utility_diff'] = trip['utility'] - trip['utility_daysim']

WriteToTrace(Visum, 'Writing Output File')
trip.to_csv(outfile)

candidates = trip[(trip['osa'] == 100416) & (trip['dsa'] < 300000) & (trip['otaz'] >= 300000) & (trip['dtaz'] >= 300000)]
check_inputs = candidates['odpair'].iloc[0]
get_best_sa_pair(check_inputs, True)

WriteToTrace(Visum, 'Done')