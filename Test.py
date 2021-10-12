import os
import pandas as pd
import numpy as np
from datetime import date
from dateutil.relativedelta import relativedelta

#SETTING THE OUTPUT RESULT FRAME
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

#CREATE A BLANK DATAFRAME
df_blank_lower = pd.DataFrame(columns=['Date_x', 'Index Category_x', 'Sub Category_x', 'Region_x', 'Change'])

#SELECT THE DIRECTORY/PATH
directory = r'C:\Users\pratik.mudholkar\OneDrive - Drilling Info\Desktop\Open Insights Index\Tasks\7 Oct-2021\Pratik QC code'
os.chdir(directory)


#READ BOTH THE EXPORT FILES PRESENT IN THE DIRECTORY
old_file = pd.read_csv("Export File_Parquet_Jul2021.csv", usecols=('Date', 'Index Category', 'Sub Category', 'Region', 'Plow', 'Index', 'Phigh', 'UID'))
old = pd.DataFrame(old_file)
new_file = pd.read_csv("Export File_Parquet_Aug2021.csv", usecols=('Date', 'Index Category', 'Sub Category', 'Region', 'Plow', 'Index', 'Phigh', 'UID'))
new = pd.DataFrame(new_file)


#MERGE BOTH EXPORT FILES USING A COMMON ID 'UID' COLUMN
merged = old_file.merge(new_file, how='inner', on='UID')
merged.to_csv("merged.csv", index=False)


#CALCULATE %DIFERRENCE/CHANGE IN INDEX -----FORMULA[((OLD INDEX - NEW INDEX) / OLD INDEX) * 100]
merged['Change'] = (merged['Index_x'] - merged['Index_y'])*100/merged['Index_x']
#print(merged['Change'])
merged.to_csv("merged.csv", index=False)

#SET THE THRESHOLD

#USER INPUTS
input1 = input("Enter the number of months:")
input2 = input("Enter the threshold value for all the months before that month, which lies" + " " + input1 + " " + "months behind the current month:")
input3 = input("Enter the threshold value for all the months after that month, which lies" + " " + input1 + " " + "months behind the current month:")

#CONDITIONAL LOOPS
today = date.today()
#print(today)
currentdate = today.strftime("%m/%d/%Y")
#print(currentdate)


#PRINT SET OF ROWS BASED ON INPUT1 = 12 MONTHS IN MERGED.CSV

mergedfile = pd.read_csv(r"C:\Users\pratik.mudholkar\OneDrive - Drilling Info\Desktop\Open Insights Index\Tasks\7 Oct-2021\Pratik QC code\merged.csv", usecols=('Date_x', 'Index Category_x', 'Sub Category_x', 'Region_x', 'Change'))
merged_date_change = mergedfile.loc[:, ['Date_x', 'Change']]
mergedfiledf = pd.DataFrame(mergedfile)
df_merge = mergedfiledf.loc[:, ['Date_x', 'Index Category_x', 'Sub Category_x', 'Region_x', 'Change']]
#print(df_merge)


if input1 == "12":
    twelve_months = today + relativedelta(months=-12)
    twelve_months_strf_ym = twelve_months.strftime("%Y%m")
    twelve_months_strf_ymd = twelve_months.strftime("%Y%m%d")
    #print("twelve_months_strf_ym:", twelve_months_strf_ym)
    twelve_months_strf_y = twelve_months.strftime("%Y")

# CONDITIONS BASED ON INPUT 1
    for date in df_merge['Date_x']:
        #print(date)
        date_ = date.split('-')
        date_year_month = date_[2] + date_[0]
        date_year_month_day = date_[2] + date_[0] + date_[1]
        #print("date_year_month:",date_year_month)
        date_year = date_[2]



        j = 0

        if date_year < twelve_months_strf_y or date_year_month < twelve_months_strf_ym or date_year_month_day < twelve_months_strf_ymd:

            df_blank_lower = df_blank_lower.append(mergedfile.loc[j, :])
        j += 1


        check_condition_less_true = df_merge[(df_merge['Change'] > int(input2)) | (merged['Change'] < (-1 * int(input2)))]
        # print("check_condition_less_true", check_condition_less_true)

        check_condition_more_true = df_merge[(df_merge['Change'] > int(input3)) | (merged['Change'] < (-1 * int(input3)))]
        # print("check_condition_more_true", check_condition_more_true)

        if check_condition_less_true == True and check_condition_more_true == True:
            print(df_blank_lower)




        #while str(year[2]) > str(twelve_months_strf_Y):
            #print("dates which lie ahead" + " " + str(twelve_months) + " " + "are" + " " + str(year[2]))



# else:
#     #IF INPUT1 = 6 MONTHS
#     six_months = today + relativedelta(months=-6)
#     print(str(six_months))
#     six_months_strf_MY = six_months.strftime("%m-%Y")
#     print(six_months_strf_MY)
#     six_months_strf_Y = six_months.strftime("%Y")
#     print(six_months_strf_Y)
#
#
# #PRINT SET OF ROWS BASED ON INPUT1 = 6 MONTHS
#     for date in merged['Date_x']:
#         year = date.split('-')
#         #print(year)
#         if str(year[2]) < str(six_months_strf_Y):
#             print("dates which lie behind" + " " + str(six_months) + " " + "are" + " " + str(year[2]))
#         if str(year[2]) > str(six_months_strf_Y):
#             print("dates which lie ahead" + " " + str(six_months) + " " + "are" + " " + str(year[2]))








#CHECK IF % CHANGE IS > OR < THAN THRESHOLD BASED ON BELOW GIVEN CONDITIONS

#CONDITION 1: IF DATE < 2020, USE LESSER THRESHOLD AND CHECK IF THE CALCULATED %CHANGE IS < OR > THAN THAT THRESHOLD

# for date in merged['Date_x']:
#     year = date.split('-')
#     #print(int(year[2]))
#     if int(year[2]) < 2020:
#         check = merged[(merged['Change'] > chng_pct[1]) | (merged['Change'] < (-1 * chng_pct[1]))]
#         print(check)
#         check = check[['Date_x', 'Index Category_x', 'Sub Category_x', 'Region_x', 'Plow_x', 'Index_x', 'Phigh_x', 'UID', 'Plow_y', 'Index_y', 'Phigh_y', 'Change']]
#         check1 = check.copy()
#         check.set_index('Date_x', inplace=True)
#         check.to_csv('Comparison.csv')
#
#     #CONDITION 2: IF DATE > OR = 2020, USE HIGHER THRESHOLD AND CHECK IF THE CALCULATED %CHANGE IS < OR > THAN THAT THRESHOLD
#     else: #int(year[2]) >= 2020:
#         check = merged[(merged['Change'] > chng_pct[2]) | (merged['Change'] < (-1 * chng_pct[2]))]
#         print(check)
#         check = check[['Date_x', 'Index Category_x', 'Sub Category_x', 'Region_x', 'Plow_x', 'Index_x', 'Phigh_x', 'UID', 'Plow_y', 'Index_y', 'Phigh_y', 'Change']]
#         check1 = check.copy()
#         check.set_index('Date_x', inplace=True)
#         check.to_csv('Comparison.csv')
#         break
#
#     #SAVE ALL THE CALCULATIONS
#     merged.to_csv("merged.csv", index=False)
#
#     #CREATE A QC SHEET
#     check1 = check1[['Index Category_x', 'Sub Category_x', 'Region_x']]
#     check1.drop_duplicates(subset=['Index Category_x', 'Sub Category_x', 'Region_x'], keep='first', inplace=True)
#     check1.set_index('Index Category_x', inplace=True)
#     check1.to_csv('indices to be checked.csv')
#     break

#merged.to_csv("merged.csv", index=False)
# #os.open("merged.csv")
# merged.to_csv("merged.csv", index=False)
# check.to_csv('Comparison.csv')
# check1 = check1[['Index Category_x', 'Sub Category_x', 'Region_x']]
# check1.drop_duplicates(subset=['Index Category_x', 'Sub Category_x', 'Region_x'], keep='first', inplace=True)
# check1.set_index('Index Category_x', inplace=True)
# check1.to_csv('indices to be checked.csv')


