import os

wd = os.getcwd()
fp = os.path.join(wd, 'microzones.csv')
outfile_cnty = os.path.join(wd, 'MicrozoneCounty.csv')
outfile_dist = os.path.join(wd, 'MicrozoneDistrict.csv')

with open(fp) as f:
    lines = f.read().split('\n')
    f.close()

county_data = {}
district_data = {}

first_line = True
for line in lines:
    if line == '':
        continue
    entry = line.split(',')
    if first_line:
        emptot_p = entry.index('EMPTOT_P')
        emptot_1 = entry.index('EMPTOT_1')
        emptot_2 = entry.index('EMPTOT_2')
        stcnty = entry.index('STCNTY')
        district = entry.index('DISTRICT')
        first_line = False

    else:
        if entry[stcnty] not in county_data:
            county_data[entry[stcnty]] = [int(entry[emptot_p]),
                                          int(entry[emptot_1]),
                                          int(entry[emptot_2])]
        else:
            county_data[entry[stcnty]][0] += int(entry[emptot_p])
            county_data[entry[stcnty]][1] += int(entry[emptot_1])
            county_data[entry[stcnty]][2] += int(entry[emptot_2])

        if entry[district] not in district_data:
            district_data[entry[district]] = [int(entry[emptot_p]),
                                              int(entry[emptot_1]),
                                              int(entry[emptot_2])]

        else:
            district_data[entry[district]][0] += int(entry[emptot_p])
            district_data[entry[district]][1] += int(entry[emptot_1])
            district_data[entry[district]][2] += int(entry[emptot_2])

county_lines = ['STCNTY,EMPTOT_P,EMPTOT_1,EMPTOT_2']
district_lines = ['DISTRICT,EMPTOT_P,EMPTOT_1,EMPTOT_2']

for county in county_data:
    county_lines.append('{0},{1},{2},{3}'.format(county,
                                                 county_data[county][0],
                                                 county_data[county][1],
                                                 county_data[county][2]))


for district in district_data:
    district_lines.append('{0},{1},{2},{3}'.format(district,
                                                   district_data[district][0],
                                                   district_data[district][1],
                                                   district_data[district][2]))

with open(outfile_cnty, 'w') as f:
    f.write('\n'.join(county_lines))
    f.close()

with open(outfile_dist, 'w') as f:
    f.write('\n'.join(district_lines))
    f.close()
