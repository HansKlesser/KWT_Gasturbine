from tespy.networks import Network
from tespy.connections import Connection
from tespy.components import Sink, Source, DiabaticCombustionChamber, Compressor


fluid_list = ['N2', 'O2', 'Ar', 'CO2', 'H2O', 'CH4']

gt = Network(fluids=fluid_list, p_unit='bar', T_unit='C')

air = {'N2': 0.7551, 'O2': 0.2314, 'Ar': 0.0129, 'CO2': 0.0006, 'H2O': 0, 'CH4': 0}
fuel = {'N2': 0, 'O2': 0, 'Ar': 0, 'CO2': 0, 'H2O': 0, 'CH4': 1}

src_air = Source('air')
src_fuel = Source('fuel')
sink_exhaust = Sink('exhaust')

cmp_CC = DiabaticCombustionChamber('combustion chamber')
cmp_Compressor = Compressor('compressor')

con_1 = Connection(src_air, 'out1', cmp_Compressor, 'in1', label='air')
con_2 = Connection(cmp_Compressor, 'out1', cmp_CC, 'in1', label='comp_air')
con_3 = Connection(src_fuel, 'out1', cmp_CC, 'in2', label ='fuel')
con_4 = Connection(cmp_CC, 'out1', sink_exhaust, 'in1', label='exhaust')

gt.add_conns(con_1, con_2, con_3, con_4)


cmp_CC.set_attr(eta=0.98, pr=0.95)

cmp_Compressor.set_attr(eta_s=0.85, pr=10)
con_1.set_attr(p=1.013, T=25, fluid=air)
con_3.set_attr(p=20, T=25, fluid=fuel, m=1)
con_4.set_attr(T=1000)

gt.solve('design')

gt.print_results()