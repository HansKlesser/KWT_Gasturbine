# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read files
df_eta = pd.read_csv('eta.csv', header=0, index_col=0)
df_swk = pd.read_csv('swk.csv', header=0, index_col=0)

# print for controll
print(df_swk)
print(df_eta)

fig, swk_eta = plt.subplots()

swk_eta.plot(df_swk['5'],df_eta['5'], label='p_r = constant', color='blue')
swk_eta.plot(df_swk['10'],df_eta['10'], color='blue')
swk_eta.plot(df_swk['15'],df_eta['15'], color='blue')
swk_eta.plot(df_swk['20'],df_eta['20'], color='blue')
swk_eta.plot(df_swk['25'],df_eta['25'], color='blue')
swk_eta.plot(df_swk['30'],df_eta['30'], color='blue')

swk_eta.set(xlabel='Spezifische Arbeit [kJ/kg]', ylabel='Wirkungsgrad [%]',
       title='Parameteranalyse')

for i in range(5):
    swk_eta.plot(df_swk.iloc[i], df_eta.iloc[i], color='red')

swk_eta.plot(df_swk.iloc[5], df_eta.iloc[5], color='red', label='T_inlet = constant')

plt.legend()
plt.show()




