#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 18:19:48 2019

@author: gabriel
"""
import pandas as pd
import numpy as np
from scipy.stats import linregress as linreg
# =============================================================================
# functions definitions
# =============================================================================


def ignore_interval(data, dict_before, dict_after, interval):
    """
    Filter data from the given dictionary of dataframes 'data',
    ignoring a given iterval of time and store the results
    in separated dictionaries of dataframes
    """
    names = list(data.keys())
    for i in range(1, 5):
        df = data[names[i-1]]
        dict_before[names[i-1]] = df[
                df['tiempo'] < interval[i-1][0]]
        df = None
    for i in range(1, 5):
        df = data[names[i-1]]
        dict_after[names[i-1]] = df[
                df['tiempo'] > interval[i-1][1]]
        df = None


def perfomr_linreg(dict_data, dict_output):
    """
    Gives the information of perfonmig linear regrassion over the data
    in the dictionary of dataframes, and store the results in a
    dictionary of tuples.
    The tuples content slope, intercept, r_value, p_value, std_err.
    """
    names = list(dict_data.keys())
    x = np.array([])
    y = np.array([])
    for name in names:
        x = dict_data[name].iloc[:, 0].values
        y = dict_data[name].iloc[:, 1].values
        slope, intercept, r_value, p_value, std_err = linreg(x, y)
        dict_output[name] = (slope, intercept, r_value, p_value, std_err)


def diff_intercept(before, after, final):
    """
    return the difference between the outputs of
    the liear regression tuples, beore and after the equilibrium
    the order of the tuple values is:
        slope, intercept, r_value, p_value, std_err
    """
    names = list(before.keys())
    for name in names:
        diff_set = ()
        for i in range(0, 5):
            diff = before[name][i] - after[name][i]
            diff_set = diff_set + (diff, )
        final[name] = diff_set        


# =============================================================================
# end of functions definitions
# =============================================================================

# =============================================================================
# importing data from *.txt files into a dictionary of DataFrames
# =============================================================================
masses = {}
for i in range(1, 5):
    filename = 'masa' + str(i) + '.txt'
    name = 'mass' + str(i)
    masses[name] = pd.read_csv(filename, sep='\t', skiprows=1)

# Converting mass to Kilograms
for name in list(masses.keys()):
    masses[name].iloc[:, 1] = masses[name].iloc[:, 1]/1000

# =============================================================================
# Throughout this interval, the system is out of equilibrium
# We don't care about this data
# =============================================================================

ignore_inter = np.array([[89, 179],
                         [80, 175],
                         [80, 175],
                         [80, 195]])

data_before_equilibrium = {}
data_after_equilibrium = {}
ignore_interval(masses,
                data_before_equilibrium,
                data_after_equilibrium,
                ignore_inter)


reg_before = {}
reg_after = {}
perfomr_linreg(data_before_equilibrium, reg_before)
perfomr_linreg(data_after_equilibrium, reg_after)

# slope, intercept, r_value, p_value, std_err
final_data = {}
names = list(masses.keys())


diff_intercept(reg_before,
               reg_after, final_data)

delta_m = {}
for name in names:
    delta_m[name] = final_data[name][1]


with open('delta_m.txt', 'w+') as file:
    print('# mass delta_m', file=file)
    for name in names:
        print(name + ' ' + '{:.3e}'.format(delta_m[name]), file=file)
