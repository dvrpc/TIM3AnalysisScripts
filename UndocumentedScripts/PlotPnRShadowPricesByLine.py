import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#sp_file = r'Y:\TIM_3.1\DVRPC_ABM_Testing\scenario\working\park_and_ride_shadow_prices_max-30.txt'
#sp_file = r'Y:\TIM_3.1\TestPnRShadowPriceConvergence\scenario\Output\2105012311\park_and_ride_shadow_prices.txt'
sp_file_1 = r'D:\TIM3.1\TestPnRShadowPriceConvergence\scenario\Output\2105060712\park_and_ride_shadow_prices.txt'
sp_file_0 = r'D:\TIM3.1\TestPnRShadowPriceConvergence\scenario\Output\2105050712\park_and_ride_shadow_prices.txt'
pnr_file = r'D:\TIM3\PnRZones.csv'

outfile = r'D:\TIM3\PnRSPPlots5vs15\{0}_{1}.png'

sp1 = pd.read_csv(sp_file_1, '\t')
sp0 = pd.read_csv(sp_file_0, '\t')
pnr = pd.read_csv(pnr_file).set_index('NodeID')

def extract_info(name):
    words = name.split(' ')
    line = words[-2]
    station = ' '.join(words[:-2])
    return (line, station)

def get_prices(sp):
    prices = pd.DataFrame(np.zeros((180, 1440)), index = range(1, 181))
    for i in range(1440):
        if i < 10:
            prices[i] = sp['PRICE000' + str(i)]
        elif i < 100:
            prices[i] = sp['PRICE00' + str(i)]
        elif i < 1000:
            prices[i] = sp['PRICE0' + str(i)]
        else:
            prices[i] = sp['PRICE' + str(i)]
    return prices

prices0 = get_prices(sp0)
prices1 = get_prices(sp1)

pnr['Info'] = pnr['NAME'].apply(extract_info)
pnr['Line'] = pnr['Info'].apply(lambda x: x[0])
pnr['Station'] = pnr['Info'].apply(lambda x: x[1])

lines = list(pnr['Line'].value_counts().index)

def plot_tod_breaks():
    for h in [6, 10, 15, 19]:
        plt.plot([60*h, 60*h], [-60, 5], color = 'k', linestyle = '--')

for line in lines:
    pnr_lines = pnr.query('Line == @line')
    n_lots = pnr_lines.shape[0]
    max_plots = n_lots
    for p in range(max_plots):
        plt.figure(figsize = (16, 9))
        plot_tod_breaks()
        for i in pnr_lines.index[p:p+1]:
            plt.plot(prices0.loc[i], linewidth = 2, label = 'TimeSpread = 5')
            plt.plot(prices1.loc[i], linewidth = 2, label = 'TimeSpread = 15')
        plt.title(line + ': {}'.format(pnr_lines.loc[i, 'Station']))
        plt.legend(loc = 'lower right')
        plt.grid(True)
        plt.xlim(0, 1439)
        plt.xticks(range(0, 1440, 60), range(24))
        plt.ylim(-60, 5)
        plt.xlabel('Hour')
        plt.ylabel('Shadow Price')
        #plt.legend(loc = 'lower right')
        plt.savefig(outfile.format(line, pnr_lines.loc[i, 'Station'].replace('/', '-')))
        plt.clf()
        plt.close()

print('Go')