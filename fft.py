import numpy as np 
import csv
import pandas as pd 

with open('slit_horizontal_exp5998.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))
    
csvfile = 'slit_horizontal_exp5998.csv'
df = pd.read_csv(csvfile)
my_array = df['Gray_Value']
my_array = my_array.to_numpy()
fft_array = np.fft.rfftn(my_array)
print(fft_array)
