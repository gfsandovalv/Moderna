import numpy as np
import scipy as sci
import pandas as pd
# import matplotlib.pyplot as plt
import math
data = pd.read_csv('data.dat', sep='\t')
# print(data)


def T(current, measured_volt):
    """
    Devuelve la temperatura en función de la resistencia 
    del detector de radiacion.
    La resistencia del detector se determina con el voltaje medido en el multímetro
    y la corriente suministrada al bombillo
    """
    m = 1e-3
    R = measured_volt*m/current
    R0 = 0.3
    alpha = 4.5e-3
    T0 = 291
    return (R/R0 - 1)/alpha + T0



current = data.iloc[:, 1].values #corriente dada al bombillo
voltage = data.iloc[:, 0].values #voltaje aplicado (energía de radiación)
radiation_volts = data.iloc[:, 2:].values # voltaje medido en el multímetro para diferentes distancias
power = np.array([I*V for I, V in zip(current, voltage)])
radiation_temp = np.array([T(current[i], radiation_volts[i, :])
                           for i in range(0, radiation_volts.shape[0] - 1)])

# =============================================================================
# temperaturas a partir del voltaje medido en el multimetro
# =============================================================================

data_ = np.array([])
for i, power in enumerate(power):
    temp = radiation_volts[i]
    temp = np.insert(temp, 0, power, axis=0)
    data_ = np.append(data_, temp, axis=None)


data_log = np.array([math.log1p(val) for val in data_])
data_log.shape = (8,6)
data_.shape = (8,6)
np.savetxt('temperaturas.dat', data_, fmt='%.3e', delimiter='\t', header='power\t\t\t measured distance')
np.savetxt('temp_log.dat', data_log, fmt='%.3e', delimiter='\t', header='log of : power\t\t\t measured voltage')

