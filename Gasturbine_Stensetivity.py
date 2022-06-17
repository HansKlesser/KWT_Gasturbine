from tespy.networks import Network
from tespy.connections import Connection, Bus
from tespy.components import Sink, Source, DiabaticCombustionChamber, Compressor, Turbine

import numpy as np
import pandas as pd


fluid_list = ['N2', 'O2', 'Ar', 'CO2', 'H2O', 'CH4']

gt = Network(fluids=fluid_list, p_unit='bar', T_unit='C')

air = {'N2': 0.7551, 'O2': 0.2314, 'Ar': 0.0129, 'CO2': 0.0006, 'H2O': 0, 'CH4': 0}
fuel = {'N2': 0, 'O2': 0, 'Ar': 0, 'CO2': 0, 'H2O': 0, 'CH4': 1}

src_air = Source('air')
src_fuel = Source('fuel')
sink_exhaust = Sink('exhaust')

cmp_CC = DiabaticCombustionChamber('combustion chamber')
cmp_Compressor = Compressor('compressor')
cmp_Turbine = Turbine('turbine')

con_1 = Connection(src_air, 'out1', cmp_Compressor, 'in1', label='air')
con_2 = Connection(cmp_Compressor, 'out1', cmp_CC, 'in1', label='comp_air')
con_3 = Connection(src_fuel, 'out1', cmp_CC, 'in2', label ='fuel')
con_4 = Connection(cmp_CC, 'out1', cmp_Turbine, 'in1', label='cc outlet')
con_5 = Connection(cmp_Turbine, 'out1', sink_exhaust, 'in1', label='exhaust')

gt.add_conns(con_1, con_2, con_3, con_4, con_5)

# Parameter Data for Components
cmp_CC.set_attr(eta=0.98, pr=0.95)
cmp_Compressor.set_attr(eta_s=0.85, pr=20)
cmp_Turbine.set_attr(eta_s=0.9)

# flow parameters
con_1.set_attr(p=1.013, T=25, fluid=air)
con_3.set_attr(p=20, T=25, fluid=fuel)
con_4.set_attr(T=1200)
con_5.set_attr(p=1.013)

# busses for energy flow
work_net = Bus('work net')
fuel_energy = Bus('fuel energy')

work_net.add_comps(
    {'comp': cmp_Compressor, 'base': 'bus', 'char': 1},
    {'comp': cmp_Turbine, 'char': 1}
)

fuel_energy.add_comps(
    {'comp': cmp_CC, 'base': 'bus', 'char': 1}
)

gt.add_busses(work_net, fuel_energy)

# Parameter of Busses
work_net.set_attr(P=-150e6)

gt.solve('design')

gt.print_results()

# save to file
gt.save('results-design/')

# create parameter and results data
pr_range = np.array([5, 10, 15, 20, 25, 30])
inletT_range = np.array([900, 1000, 1100, 1200, 1300, 1400])
df_eta = pd.DataFrame(columns=pr_range)
df_swk = pd.DataFrame(columns=pr_range)

for i in inletT_range:
    eta = []
    swk = []
    for j in pr_range:
        # Update Parameter
        cmp_Compressor.set_attr(pr=j)
        con_4.set_attr(T=i)
        con_3.set_attr(p=1.013*j+1e-9)

        print('Inlet Temperature =', i)
        print('Pressure Ratio Compressor =', j)

        # solve case
        gt.solve(mode='design', init_path='results-design/')
        eta.append(abs(work_net.P.val/fuel_energy.P.val)*100)
        swk.append(abs(work_net.P.val*1e-3)/con_1.m.val)
    df_eta.loc[i] = eta
    df_swk.loc[i] = swk
    df_eta.to_csv('eta.csv')
    df_swk.to_csv('swk.csv')