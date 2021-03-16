import sys
import os
import logging
import numpy as np 
import csv
import pandas as pd 
from matplotlib import pyplot as plt

PIXEL_SIZE_IN_MM = 1.2 * pow(10,-3)
DATA_COLUMN_NAME = 'Gray_Value'


def plot_mtf( frequency_array, fft_array ):
    plt.title("Modulation transfer function")
    plt.xlabel("mm^-1")
    plt.ylabel("Normalized amplitude %")
    plt.xlim([0, 200])
    plt.ylim([0, 105])
    plt.plot(frequency_array, fft_array)
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

if __name__ == "__main__":
    if(len(sys.argv) == 1):
        logging.error("No file selected")
        logging.error("Correct usage: python3 fft.py filename")
        quit()
    filename = sys.argv[1]

    df = pd.read_csv(filename)
    raw_array = df[DATA_COLUMN_NAME]
    raw_array = raw_array.to_numpy()


    fft_array = generate_normalized_mtf_array(raw_array)
    frequency_array = generate_frequency_array(fft_array)
    plot_mtf(frequency_array, fft_array) 
