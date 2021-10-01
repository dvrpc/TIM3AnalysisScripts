import pandas as pd

infile = r'T:\TIM_3.1\191018_StraightLineDistAll\scenario\maz2sa_dist.dat'
outfile = infile.replace('.dat', '_sorted.dat')
debug_file = infile.replace('.dat', '_debug.xlsx')
sa2mode_file = r'D:\TIM3\sa2mode.csv'

max_for_mode = {'Rail': 1,
                'Pat':  2,
                'Sub':  2,
                'LRT':  2,
                'Trl':  3,
                'Bus':  3}

writer = pd.ExcelWriter(debug_file)
N = 65536

print('Reading File')
sa2mode = pd.read_csv(sa2mode_file, index_col = 0)['MODE']
#print(sa2mode)
df = pd.read_csv(infile, ' ')

print('Adding Mode')
df['mode'] = df['stopareaid'].map(sa2mode)
df.head(N).to_excel(writer, 'Added Mode')

print('Sorting by mode and distance')
df = df.sort_values(['zoneid', 'distance', 'mode'])
df.head(N).to_excel(writer, 'Sorted')

#mode_dummies = pd.get_dummies(df['mode'])
#df[mode_dummies.columns] = mode_dummies
#df.head(N).to_excel(writer, 'Added Dummies')

modes = df['mode'].value_counts().index
for mode in modes:
    print('Creating ' + mode + ' pivot')
    mode_df = df[df['mode'] == mode]
    pivot = mode_df.pivot('zoneid', 'stopareaid', 'distance')
    pivot.to_excel(writer, 'Pivot_' + mode)

print('Writing Debug File')
writer.close()