import sys
import os
import logging
import numpy as np 
import csv
import pandas as pd 
from scipy.optimize import curve_fit 

from matplotlib import pyplot as plt

PIXEL_SIZE_IN_MM = 1.2 * pow(10,-3)
DATA_COLUMN_NAME = 'Gray_Value'
LABEL_POINT = 20 # cycle/mm

def find_point_location (frequency_array, x ):
    differential_array = []
    for i in range(len(frequency_array)):
        differential_array.append(abs(frequency_array[i]- x))
    min_dif = np.min(differential_array)
    return differential_array.index(min_dif)

def plot_mtf( frequency_array, fft_array, filename):
    plt.title(filename)
    plt.xlabel("mm^-1")
    plt.ylabel("Normalized amplitude %")
    plt.xlim([0, 200])
    plt.ylim([0, 105])
    plt.plot(frequency_array, fft_array)
    position = find_point_location (frequency_array, LABEL_POINT)
    x = frequency_array[position]
    y = fft_array[position]
    y = round(y, 2)
    value_string = str(y) + "%"
    plt.plot(x, y, 'ro')
    plt.annotate('20 cycle per mm', xy = (x, y), xytext = (x + 20, y + 3), arrowprops=dict(facecolor='black', shrink = 0.05),)
    plt.annotate(value_string, xy=(x, y), xytext= (x + 20, y - 3))
    filename = filename = filename[:len(filename) - 4] + "_mtf.png"
    plt.savefig(filename)
    plt.show()

def generate_frequency_array( raw_array ):
    f_array = []
    for i in range (0, len(raw_array)):
        element = (i/ PIXEL_SIZE_IN_MM) / len(raw_array)
        f_array.append(element)
    return f_array

def generate_normalized_mtf_array( raw_array ):
    fft_array = np.fft.rfft(raw_array)
    fft_modulus_array = []
    max_element = abs(np.max(fft_array))
    for element in fft_array:
        fft_modulus_array.append(abs(element)/max_element * 100)
    return fft_modulus_array

def save_data_to_csv_file ( frequency_array, fft_array, filename ):
    dict = {'frequency': frequency_array, 'mtf %': fft_array}
    df = pd.DataFrame(dict)
    filename = filename[:len(filename) - 4] + '_mtf.csv'
    df.to_csv(filename)

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        logging.error("No file selected")
        logging.error("Correct usage: python3 fft.py filename")
        quit()
    filename = sys.argv[1]

    df = pd.read_csv(filename)
    raw_array = df[DATA_COLUMN_NAME]
    raw_array = raw_array.to_numpy()

    fft_array = generate_normalized_mtf_array(raw_array)
    frequency_array = generate_frequency_array(fft_array)
    find_point_location(frequency_array, 20)
    save_data_to_csv_file (frequency_array, fft_array, filename)
    plot_mtf(frequency_array, fft_array, filename)