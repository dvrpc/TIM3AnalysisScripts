import pandas
import numpy

base_path = Visum.GetPath(69)
trip_file = os.path.join(base_path, 'Output', '_trip_2.dat')
sp_file = os.path.join(base_path, 'working', 'park_and_ride_shadow_prices.txt')

trip = pd.read_csv(trip_file, '\t')
sp = pd.read_csv(sp_file, '\t')

