
fp1 = r'M:\Modeling\Model_Development\TIM3.1\Template_Github\DVRPC_ABM\Scripts\MAZ_to_StopAreas_June_2_DVRPC.py'
fp2 = r'T:\TIM_3.1\190727_FullTest\Scripts\MAZ_to_StopAreas_June_2_DVRPC.py'

f1 = open(fp1, 'r')
lines1 = f1.read().split('\n')
f1.close()

f2 = open(fp2, 'r')
lines2 = f2.read().split('\n')
f2.close()

for i in range(min(len(lines1), len(lines2))):
    if lines1[i] != lines2[i]:
        print(i)