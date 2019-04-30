#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 11:19:59 2019

@author: gabriel
"""
import pandas as pd
import numpy as np
import math
from scipy.stats import linregress as linreg


def slope(data_x, data_y):
    """
    Return the slope of the given set of data
    """
    slope_, intercept, r_value, p_value, std_err = linreg(data_x, data_y)
    return slope_


tube_lenght = 13.5  # leght of the tube
h = 6.62607004e-34  # planck constant
m_e = 9.10938356e-31  # electron mass
e = 1.60217662e-19  # electron charge

raw_data = pd.read_csv('data1.txt', sep='\t')

radios_medios = np.array([(raw_data['R1']+raw_data['R2'])/2,
                          (raw_data['r1']+raw_data['r2'])/2])

energy = [e*V*1e3 for V in raw_data['kV']]
sqrt_energy_inverse = [1/math.sqrt(eV) for eV in energy]
sin_theta1 = [math.sin(math.atan(r/tube_lenght)) for r in radios_medios[0]]
sin_theta2 = [math.sin(math.atan(r/tube_lenght)) for r in radios_medios[1]]

data = pd.DataFrame({'1/sqrt(eV)': sqrt_energy_inverse,
                     'sin(theta1)': sin_theta1,
                     'sin(theta2)': sin_theta2})

slopes = [slope(data['1/sqrt(eV)'], data['sin(theta1)']),
          slope(data['1/sqrt(eV)'], data['sin(theta2)'])]


interplanar_distance = np.array([h/(2*mm*math.sqrt(2*m_e)) for mm in slopes])
print(interplanar_distance)
