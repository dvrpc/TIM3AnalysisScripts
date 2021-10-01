import pandas as pd

fp1 = r'Y:\TIM_3.1\DVRPC_ABM_VISUM18patch\Tools\CreateParcelBase\DVRPC_parcelbase.dat' #Old file
fp2 = r'T:\TIM_3.1\190802_FullTest\Tools\CreateParcelBase\DVRPC_parcelbase_2010.dat' #New file

df1 = pd.read_csv(fp1, delimiter = ' ')
df2 = pd.read_csv(fp2, delimiter = ',')

print((df1 != df2).sum())