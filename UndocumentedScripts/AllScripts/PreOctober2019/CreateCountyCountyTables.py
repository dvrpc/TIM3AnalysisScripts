import os
from collections import OrderedDict

def csv2dict(csv_file):
    '''
    Reads the first 2 columns of a csv file into a dictionary where the keys are the entries in the first column and the values are the entries in the second

    Parameters
    ----------
    csv_file (str):
        Filepath of csv file to be read into dictionary

    Returns
    -------
    out_dict (dict):
        Dictionary read from first two columns of csv file
    '''
    out_dict = {}
    first_line = True
    
    f = open(csv_file)
    for line in f:
        if first_line:
            first_line = False
            continue
        else:
            data = line.replace('\n', '').split(',')
            out_dict[data[0]] = data[1]

    f.close()
    return out_dict
        
wd = os.path.split(__file__)[0]
taz2county_file = os.path.join(wd, 'taz2county.csv')
taz2county = csv2dict(taz2county_file)

def init_od_dict(locations):
    '''
    Initializes an origin-destination dictionary based on a list of locations

    Parameters
    ----------
    locations (list):
        List of locations (strings)

    Returns
    -------
    od_dict (dict):
        Dictionary where the input locations are the keys and the values are sub-dictionaries where the locations are the keys and zeros are the values
    '''
    #Create empty origin-destination dictionary
    od_dict = OrderedDict()
    for oloc in locations:
        od_dict[oloc] = OrderedDict()
        for dloc in locations:
            od_dict[oloc][dloc] = 0.0
    return od_dict

def write_table(name, od_dict, fp):
    '''
    Writes table to specified filepath

    Parameters
    ----------
    name (str):
        Table name
    od_dict (dict):
        Dictionary where the keys are origins, and the values are sub-dictionaries where the keys are destinations, and the values are the number in the origin-destination pair
    fp (str):
        Filepath to write to
    '''
    locations = list(od_dict.keys()) #Extract locations from dictionary
    lines = [','.join([name] + locations)] #Write first line as the header
    for oloc in locations: #For each origin location, write the number of trips to each destination location
        line = [oloc]
        for dloc in locations:
            line.append(str(od_dict[oloc][dloc]))
        lines.append(','.join(line))
    with open(fp, 'w') as f:
        f.write('\n'.join(lines))
        f.close()
    print('{} origin-destination table written to file'.format(name))

def create_county_county_tables(run, purpose):
    '''
    Creates county-county home to work flows based on:
        -cc_hhper_{purpose}.csv: Merge of household and person file (usual work location)
        -cc_tour_{purpose}.csv: Tour file (Work tour O-D)
        -cc_trip_{purpose}.csv: Trip file (Work trip O-D)

    Parameters
    ----------
    run (str):
        Full path of directory containing outputs from DaySim run
    purpose (str):
        Indicates whether to make the summaries based on work trips or school trips. Must be "work" or "school"
    '''
    #Create variable that is true if work trips are being summarized.
    if purpose == 'work':
        work = True
    elif purpose == 'school':
        work = False
    else: #If any purpose other than work or school is selected, raise a ValueError
        raise ValueError('Purpose must be "work" or "school"')
    
    #Define input files
    hh_file = os.path.join(run, '_household_2.dat')
    per_file = os.path.join(run, '_person_2.dat')
    tour_file = os.path.join(run, '_tour_2.dat')
    trip_file = os.path.join(run, '_trip_2.dat')
    global taz2county

    counties = ['Bucks',
                'Chester',
                'Delaware',
                'Montgomery',
                'Philadelphia',
                'Burlington',
                'Camden',
                'Gloucester',
                'Mercer',
                'Rest of PA',
                'Rest of NJ',
                'Rest of Outer Counties',
                'Outside'
                ]

    #Define output files
    hhper_output = os.path.join(run, 'cc_hhper_{}'.format(purpose))
    tour_output = os.path.join(run, 'cc_tour_{}'.format(purpose))
    trip_output = os.path.join(run, 'cc_trip_{}'.format(purpose))

    #Create dictionary to map household number to household TAZ
    hhno2htaz = {}
    h = open(hh_file)
    first_line = True
    for line in h:
        entry = line.replace('\n', '').split('\t')
        if first_line:
            hhno = entry.index('hhno')
            hhtaz = entry.index('hhtaz')
            first_line = False
        else:
            hhno2htaz[entry[hhno]] = entry[hhtaz]
    h.close()

    ke = 0
    #Extract usual work/school location from person file and write to file
    hhper = init_od_dict(counties)    
    p = open(per_file)
    first_line = True
    for line in p:
        entry = line.replace('\n', '').split('\t')
        if first_line:
            hhno = entry.index('hhno')
            pwtaz = entry.index('pwtaz')
            pstaz = entry.index('pstaz')
            pptyp = entry.index('pptyp')
            psexpfac = entry.index('psexpfac')
            first_line = False
        else:
            if work:
                if entry[pwtaz] in ['-1', '0']:
                    continue
            else:
                if entry[pstaz] in ['-1', '0']:# or entry[pptyp] not in ['6', '7']:
                    continue
            htaz = hhno2htaz[entry[hhno]]
            try:
                hcounty = taz2county[htaz]
            except KeyError:
                print(htaz)
                ke += 1
                continue
            if work:
                try:
                    wcounty = taz2county[entry[pwtaz]]
                except KeyError:
                    print(entry[pwtaz])
                    ke += 1
                    continue
                if entry[psexpfac] == 'NA':
                    continue
                hhper[hcounty][wcounty] += float(entry[psexpfac])
            else:
                try:
                    scounty = taz2county[entry[pstaz]]
                except KeyError:
                    print(entry[pstaz])
                    ke += 1
                    continue
                if entry[psexpfac] == 'NA':
                    continue
                hhper[hcounty][scounty] += float(entry[psexpfac])
    write_table('Usual {} Location'.format(purpose.capitalize()), hhper, os.path.join(run, 'cc_hhper_{}.csv'.format(purpose)))
    print(ke)

    #Extract tour origin/destination pairs
    tour = init_od_dict(counties)
    to = open(tour_file)
    first_line = True
    for line in to:
        entry = line.replace('\n', '').split('\t')
        if first_line:
            pdpurp = entry.index('pdpurp')
            totaz = entry.index('totaz')
            tdtaz = entry.index('tdtaz')
            toexpfac = entry.index('toexpfac')
            first_line = False
        else:
            if work:
                if entry[pdpurp] != '1':
                    continue
            else:
                if entry[pdpurp] != '2':
                    continue
            try:
                ocounty = taz2county[entry[totaz]]
                dcounty = taz2county[entry[tdtaz]]
                if entry[toexpfac] == 'NA':
                    continue
                tour[ocounty][dcounty] += float(entry[toexpfac])
            except KeyError:
                continue
    write_table('{} Tours'.format(purpose.capitalize()), tour, os.path.join(run, 'cc_tour_{}work.csv'.format(purpose)))

    #Extract trip origin/destination pairs
    trip = init_od_dict(counties)
    tr = open(trip_file)
    first_line = True
    for line in tr:
        entry = line.replace('\n', '').split('\t')
        if first_line:
            dpurp = entry.index('dpurp')
            otaz = entry.index('otaz')
            dtaz = entry.index('dtaz')
            trexpfac = entry.index('trexpfac')
            first_line = False
        else:
            if work:
                if entry[dpurp] != '1':
                    continue
            else:
                if entry[dpurp] != '2':
                    continue
            try:
                ocounty = taz2county[entry[otaz]]
                dcounty = taz2county[entry[dtaz]]
                if entry[trexpfac] != 'NA':
                    continue
                trip[ocounty][dcounty] += float(entry[trexpfac])
            except KeyError:
                continue
    write_table('{} Trips'.format(purpose.capitalize()), trip, os.path.join(run, 'cc_trip_{}h2w.csv'.format(purpose)))

if __name__ == '__main__':

    wd = os.path.split(__file__)[0]
    #runs = ['run0', 'run1a', 'run2a']
    runs = ['survey']
    for run in runs:
        rundir = os.path.join(wd, 'Runs', run)
        create_county_county_tables(rundir, 'work')
        #create_county_county_tables(rundir, 'school')
