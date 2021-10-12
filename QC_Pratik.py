#Load both input files
#merge data from both the input files into a single file using col- UID
#calculate %change for col- Index from the merged data file
#Check significant %change using below method
  #-Give user inputs
  #- user input 1 - no of months
     #- 12th month behind current date
     #- 6th month behind current date
  #- user input 2 - threshold (low)
     #-for all dates before 12th month behind current date
     #-for all dates before 6th month behind current date
  #- user input 3 - threshold (high)
     #-for all dates after 12th month behind current date
     #-for all dates after 6th month behind current date
#If threshold is crossed for a particular row or n number of rows, create a new sheet and write a result values from col-B, C, D


import os
import pandas as pd
import numpy as np
from datetime import date

today = date.today()
d4 = today.strftime("%m/%d/%Y")
print(d4)
#CREATE A BLANK DATAFRAME
frames = []

#SELECT THE DIRECTORY/PATH
s = r'C:\Users\pratik.mudholkar\OneDrive - Drilling Info\Desktop\Open Insights Index\Tasks\7 Oct-2021\Pratik QC code'
os.chdir(s)

#READ BOTH THE EXPORT FILES PRESENT IN THE DIRECTORY
old_file = pd.read_csv("Export File_Parquet_Jul2021.csv", usecols=('Date', 'Index Category', 'Sub Category', 'Region', 'Plow', 'Index', 'Phigh', 'UID'))
old = pd.DataFrame(old_file)
#print(old)
new_file = pd.read_csv("Export File_Parquet_Aug2021.csv", usecols=('Date', 'Index Category', 'Sub Category', 'Region', 'Plow', 'Index', 'Phigh', 'UID'))
new = pd.DataFrame(new_file)
#print(new)

merged = old_file.merge(new_file, how='inner', on='UID')
#merged = old_file + new_file
#print(merged)
merged.to_csv("merged.csv", index=False)

#SET THE THRESHOLD
input1 = input("Enter the number of months:")
input2 = input("Enter the threshold value for all the months starting" + " " + input1 + " " + "months behind the current month:")
input3 = input("Enter the threshold value for all the months starting" + " " + input1 + " " + "months ahead of the current month:")
#chng_pct = 10

merged['Change'] = (merged['Index_x'] - merged['Index_y'])*100/merged['Index_x']
#print(merged['Change'])
#check = merged[(merged['Change'] > chng_pct) | (merged['Change'] < (-1 * chng_pct))]
check = merged[(merged['Change'] > int(input2)) | (merged['Change'] < (-1 * int(input2)))]
print(check)
check = check[['Date_x', 'Index Category_x', 'Sub Category_x', 'Region_x', 'Plow_x', 'Index_x', 'Phigh_x', 'UID', 'Plow_y', 'Index_y', 'Phigh_y', 'Change']]
check1 = check.copy()
check.set_index('Date_x', inplace=True)
#merged.to_csv("merged.csv", index=False)

check.to_csv('Comparison.csv')
check1 = check1[['Index Category_x', 'Sub Category_x', 'Region_x']]
check1.drop_duplicates(subset=['Index Category_x', 'Sub Category_x', 'Region_x'], keep='first', inplace=True)
check1.set_index('Index Category_x', inplace=True)
check1.to_csv('indices to be checked.csv')

