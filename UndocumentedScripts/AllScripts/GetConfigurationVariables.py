#import sys
import os

print('Running the script')

def find(folder, text):

    outdata = []
    log = []

    print('Looking for ' + str(text) + ' in ' + str(folder))
    log.append('Looking for ' + str(text) + ' in ' + str(folder))

    for f in os.listdir(folder):
        fp = os.path.join(folder, f)
        
        try:
            newdata = find(fp, text)
            outdata += newdata
            #log += newlog
        except WindowsError:
            infile = open(fp, 'r')
            lines = infile.read().split('\n')
            ##print(data)
            #if text in data:
            #    print('\nFOUND\n')
            #    log.append('\nFOUND\n')
            #    outdata.append(fp)
            for line in lines:
                if text in line:
                    data = line.split(text)[1]
                    i = 0
                    for ch in data:
                        if not ch.isalnum():
                            break
                        i += 1
                    variable = data[:i]
                    outdata.append(variable)
            infile.close()

    return list(set(outdata))#, log

wd = r'D:\DaySimClones\2021-07-16\DaySim'
text = 'Global.Configuration.'

outdata = find(wd, text)

outfile = r'D:\TIM3\ConfigVariables.txt'
with open(outfile, 'w') as f:
    f.write('\n'.join(outdata))
    f.close()

print('Done')