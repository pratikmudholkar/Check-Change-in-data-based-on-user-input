# Load both input files
# merge data from both the input files into a single file using col- UID
# calculate %change for col- Index from the merged data file
# Check significant %change using below method
# -Give user inputs
# - user input 1 - no of months
# - 12th month behind current date
# - 6th month behind current date
# - user input 2 - threshold (low)
# -for all dates before 12th month behind current date
# -for all dates before 6th month behind current date
# - user input 3 - threshold (high)
# -for all dates after 12th month behind current date
# -for all dates after 6th month behind current date
# If threshold is crossed for a particular row or n number of rows, create a new sheet and write a result values from col-B, C, D


import os
import pandas as pd
import numpy as np
from datetime import date
from dateutil.relativedelta import relativedelta

# SETTING THE OUTPUT RESULT FRAME
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

today = date.today()
# print(today.strftime("%m-%d-%Y"))
currentdate = today.strftime("%m/%d/%Y")
# print(currentdate)

mergedfile = pd.read_csv(r"C:\Users\pratik.mudholkar\OneDrive - Drilling Info\Desktop\Open Insights Index\Tasks\7 Oct-2021\Pratik QC code\merged.csv",usecols=('Date_x', 'Index Category_x', 'Sub Category_x', 'Region_x', 'Change'))
mergedfile['Date_x'] = pd.to_datetime(mergedfile['Date_x']).dt.strftime('%m-%d-%Y')
# print(mergedfile['Date_x'])
mergedfiledf = pd.DataFrame(mergedfile)

# BLANK_DATAFAME
df_blank_lower = pd.DataFrame(columns=['Date_x', 'Index Category_x', 'Sub Category_x', 'Region_x', 'Change'])
df_blank_upper = pd.DataFrame(columns=['Date_x', 'Index Category_x', 'Sub Category_x', 'Region_x', 'Change'])
QC_File = pd.DataFrame(columns=['Index Category_x', 'Sub Category_x', 'Region_x', 'QC Comments', 'Analyst Comments'])

input1 = input("Enter month:")
inputT1 = input("Threshold:") #for data which lies below input 1
inputT2 = input("Threshold:") #for data which lies above input 1


# CALCULATION FOR 12 MONTH BACK
# twelve_months = today + relativedelta(months=-12)
twelve_months = today + relativedelta(months=-int(input1))
print(twelve_months)
twelve_months_strf_y = twelve_months.strftime("%Y")
twelve_months_strf_ym = twelve_months.strftime("%Y%m")
twelve_months_strf_ymd = twelve_months.strftime("%Y%m%d")
twelve_months_new = twelve_months.strftime('%m-%d-%Y')
# print("Date twelve_months before" + " " + str(today) + " " + "is:", twelve_months_new)
year, month, d = str(twelve_months_new).split('-')
datemonth_12_year = year

# CALCULATION OF ACTUAL DATES IN DATA
j = 0
for value in mergedfile['Date_x']:
    # print(value)
    date_ = value.split('-')
    date_year_month = date_[2] + date_[0]
    date_year_month_day = date_[2] + date_[0] + date_[1]
    # print("date_year_month:",date_year_month)
    date_year = date_[2]
    if date_year < twelve_months_strf_y or date_year_month < twelve_months_strf_ym or date_year_month_day < twelve_months_strf_ymd:
        df_blank_lower = df_blank_lower.append(mergedfile.loc[j, :])
    else:
        df_blank_upper = df_blank_upper.append(mergedfile.loc[j, :])
    j += 1

# print(df_blank_lower)
df_blank_lower.to_csv("12_Months_Lower.csv", index=False)

df_blank_upper.to_csv("12_Months_Upper.csv", index=False)
# print(df_blank_lower['Change'])

#open_df_lower = pd.read_csv(r"C:\Users\pratik.mudholkar\PycharmProjects\Open Insights Index\12_Months_Lower.csv",
#                           usecols=('Date_x', 'Index Category_x', 'Sub Category_x', 'Region_x', 'Change'))
#df_lower = pd.DataFrame(open_df_lower)


# THRESHOLD LIMIT CHECK

# THRESHOLD LIMIT CHECK for lower dataframe (Picking up exact value)
for change in df_blank_lower['Change']:
    #check_low = change > int(inputT1)
    #check_high = change < int(inputT1)
    if float(inputT1) == change: #Threshold input1 = 5.504691345
        print("df_blank_lower: No significant change")
    else:
        print("df_blank_lower: significant change")

for change in df_blank_upper['Change']:
    if float(inputT2) == change: #Threshold input2 = 10.58766974
        print("df_blank_upper: No significant change")
    else:
        print("df_blank_upper: significant change")

#append
#1 add to the excel lower
#2 add to the excel upper

#Write a loop to check the distinct values against lower and upper for significant and no significant change



# else:
#     print("No significant change in prices")
#    # if check_12_lower != 0:
#    print(check_12_lower)
# check1 = check_12_lower.copy()
# check_12_lower.set_index('Date_x', inplace=True)
# # merged.to_csv("merged.csv", index=False)
#
# check_12_lower.to_csv('Comparison.csv')
# check1 = check1[['Index Category_x', 'Sub Category_x', 'Region_x']]
# check1.drop_duplicates(subset=['Index Category_x', 'Sub Category_x', 'Region_x'], keep='first', inplace=True)
# check1.set_index('Index Category_x', inplace=True)
# check1.to_csv('indices to be checked.csv')

# else:
#     print("Input not supported!")

