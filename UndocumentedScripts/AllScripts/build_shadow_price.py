import pandas as pd
import os

n_iter = 10
min_sd = 0.03

county_data_file = r'D:\TIM3\County_Data.csv'
county_data = pd.read_csv(county_data_file, index = 0)

taz2county_file = r'D:\ref\taz2fips.csv'
