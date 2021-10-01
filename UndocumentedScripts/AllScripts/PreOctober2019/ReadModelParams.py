import pandas as pd

fp = r'M:\Modeling\Model_Development\TIM3.1\DVRPC_ModelEstimationSummaryTables_2010 data vs 2015 data.xlsx'

work_location = pd.read_excel(fp, 'WorkLocation')

print('Done')
