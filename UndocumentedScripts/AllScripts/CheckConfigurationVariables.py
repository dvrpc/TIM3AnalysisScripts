config_var_file = r'D:\TIM3\ConfigVariables.txt'
with open(config_var_file, 'r') as f:
    vars = f.read().split('\n')
    f.close()

config_file = r'D:\TIM3.1\CalibrationJune2021\scenario\dvrpc_apply_2015_tnc.properties'
with open(config_file, 'r') as f:
    lines = f.read().split('\n')
    f.close()

for line in lines:
    if len(line) == 0 or line[0] == '#':
        continue
    var = line.replace(' ', '').split('=')[0]
    if var not in vars:
        print(var)

print('\nDone')