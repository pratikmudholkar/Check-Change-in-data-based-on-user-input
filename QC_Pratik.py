# ------ WORK FLOW -------

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


# IMPORT MODULES
import os
import sys
import pandas as pd
from datetime import date
from time import process_time
from dateutil.relativedelta import relativedelta


# INITIATING THE ENTIRE CODE RUN PROCESS TIME
coderun_start = process_time()


# SETTING THE OUTPUT RESULT FRAME
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


# ADD DATETIME FUNCTION TO GET THE CURRENT DATE
today = date.today()
currentdate = today.strftime("%m/%d/%Y")
QC_File_final_filename = today.strftime("%b-%Y")


# SELECT THE DIRECTORY/PATH
s = r'C:\Users\pratik.mudholkar\OneDrive - Drilling Info\Desktop\Open Insights Index\Tasks\7 Oct-2021\Pratik QC code'
os.chdir(s)




# READ BOTH THE EXPORT FILES PRESENT IN THE DIRECTORY
old_file = pd.read_csv("Export File_Parquet_Jul2021.csv", usecols=('Date', 'Index Category', 'Sub Category', 'Region', 'Plow', 'Index', 'Phigh', 'UID'))
old = pd.DataFrame(old_file)
new_file = pd.read_csv("Export File_Parquet_Aug2021.csv", usecols=('Date', 'Index Category', 'Sub Category', 'Region', 'Plow', 'Index', 'Phigh', 'UID'))
new = pd.DataFrame(new_file)


# MERGE BOTH EXPORT FILES USING A COMMON ID 'UID' COLUMN
merged = old_file.merge(new_file, how='inner', on='UID')
merged.to_csv("merged.csv", index=False)   #Column_name_x = old columns & Column_name_y = new columns


# REARRANGING COLUMNS
mergedupdate = list(merged.columns)

#Date_x,        Index Category_x,  Sub Category_x,    Region_x,        Plow_x,           Index_x,        Phigh_x,           UID,            Date_Y,     Index Category_Y, Sub Category_y,      Region_y,           Plow_y,          Index_y,           Phigh_y
mergedupdate[0], mergedupdate[1], mergedupdate[2], mergedupdate[3], mergedupdate[4], mergedupdate[5], mergedupdate[6], mergedupdate[7], mergedupdate[8], mergedupdate[9], mergedupdate[10], mergedupdate[11], mergedupdate[12], mergedupdate[13], mergedupdate[14] = \
    mergedupdate[8], mergedupdate[9], mergedupdate[10], mergedupdate[11], mergedupdate[5], mergedupdate[13], mergedupdate[0], mergedupdate[1], mergedupdate[2], mergedupdate[3], mergedupdate[4], mergedupdate[6], mergedupdate[7], mergedupdate[12], mergedupdate[14]
        #Date_Y,     Index Category_Y, Sub Category_y,      Region_y,        Index_x,           Index_y,

merged = merged[mergedupdate]
merged.to_csv("merged.csv", index=False)


#CREATING FINAL_QC FILE - PHASE 1
QC_File = merged.drop(["Date_x", "Index Category_x", "Sub Category_x", "Region_x", "Plow_x", "Phigh_x", "Plow_y", "Phigh_y"], axis=1)
QC_File.to_csv("QC_File.csv", index=False)

#FINAL QC FILE - PHASE 2
#CALCULATE %DIFERRENCE/CHANGE IN INDEX -----FORMULA[((OLD INDEX - NEW INDEX) / OLD INDEX) * 100]
QC_File['Change'] = (QC_File['Index_x'] - QC_File['Index_y'])*100/QC_File['Index_x']
#print(QC_File['Change'])
QC_File.to_csv("QC_File.csv", index=False)

#REARRANGING COLUMNS
QC_File_update = list(QC_File.columns)
print(QC_File_update)
QC_File_update[6], QC_File_update[7] = QC_File_update[7], QC_File_update[6]
QC_File = QC_File[QC_File_update]
QC_File.to_csv("QC_File.csv", index=False)


#CALCULATE %DIFERRENCE/CHANGE IN INDEX -----FORMULA[((OLD INDEX - NEW INDEX) / OLD INDEX) * 100]
merged['Change'] = (merged['Index_x'] - merged['Index_y'])*100/merged['Index_x']
#print(merged['Change'])
merged.to_csv("merged.csv", index=False)


# READ MERGED CSV FILE (OLD + NEW)
mergedfile = pd.read_csv(r"C:\Users\pratik.mudholkar\OneDrive - Drilling Info\Desktop\Open Insights Index\Tasks\7 Oct-2021\Pratik QC code\merged.csv", usecols=('Date_y', 'Index Category_y', 'Sub Category_y', 'Region_y', 'Change', 'UID'))


# MODIFIED A DATE COLUMN TO MEET THE CONDITIONS
mergedfile['Date_y'] = pd.to_datetime(mergedfile['Date_y']).dt.strftime('%m-%d-%Y')
mergedfiledf = pd.DataFrame(mergedfile)


# CREATE BLANK_DATAFAMES
df_blank_lower = pd.DataFrame(columns=['Date_y', 'Index Category_y', 'Sub Category_y', 'Region_y', 'Change', 'UID'])  #FOR %CHANGE CHECKS USING INPUTT1
df_blank_upper = pd.DataFrame(columns=['Date_y', 'Index Category_y', 'Sub Category_y', 'Region_y', 'Change', 'UID'])  #FOR %CHANGE CHECKS USING INPUTT2
QC_File = pd.DataFrame(columns=['Date', 'Index Category', 'Sub Category', 'Region', 'Index_old', 'Index_new', 'Change', 'QC Comments'])  #FINAL QC FILE


# USER INPUTS
input1 = input("Enter month:")
inputT1 = input("Lower Threshold value:")  #for data which lies below input 1
inputT2 = input("Upper Threshold value:")  #for data which lies above input 1

# EXECUTE THE CODE ONLY IF UPPER THRESHOLD > LOWER THRESHOLD
while True:
    if int(inputT2) > int(inputT1):
        print("We are calculating the result as per your inputs....")
        break
    else:
        print("Warning!!! inputT2 Threshold value should be always greater than inputT2 Threshold value")
        print("CODE CANNOT BE EXECUTED!")
        sys.exit()



# FILTERING DATA BASED ON INPUT 1

# n_months = today + relativedelta(months=-12) #IGNORE THIS LINE
n_months = today + relativedelta(months=-int(input1))
n_months_strf_y = n_months.strftime("%Y")
n_months_strf_ym = n_months.strftime("%Y%m")
n_months_strf_ymd = n_months.strftime("%Y%m%d")
n_months_new = n_months.strftime('%m-%d-%Y')
year, month, d = str(n_months_new).split('-')
datemonth_12_year = year




# CALCULATION OF ACTUAL DATES IN DATA
j = 0
for value in mergedfile['Date_y']:
    date_ = value.split('-')
    date_year_month = date_[2] + date_[0]
    date_year_month_day = date_[2] + date_[0] + date_[1]
    date_year = date_[2]
    if date_year < n_months_strf_y or date_year_month < n_months_strf_ym or date_year_month_day < n_months_strf_ymd:
        df_blank_lower = df_blank_lower.append(mergedfile.loc[j, :])
    else:
        df_blank_upper = df_blank_upper.append(mergedfile.loc[j, :])
    j += 1

df_blank_lower.to_csv(input1 + "_Months_Lower.csv", index=False)
print("DataFrame for data below" + " " + input1 + "months behind the current date" + " " + "has been created")
df_blank_upper.to_csv(input1 + "_Months_Upper.csv", index=False)
print("DataFrame for data above" + " " + input1 + "months behind the current date" + " " + "has been created")




# THRESHOLD LIMIT CHECK
print("Initiating Threshold limit check....")

# THRESHOLD LIMIT CHECK FOR LOWER DATA FILE  (Picking up exact value)
Result_Lower = []
for change in df_blank_lower['Change']:
    #check_low = change > int(inputT1)
    #check_high = change < int(inputT1)
    if abs(change) >= int(inputT1): #Threshold input1 = 5.504691345
        Result_Lower.append("Significant change")
    else:
        Result_Lower.append("No significant change")
df_blank_lower['Result'] = Result_Lower

#SAVE THE LOWER DATA FILES
df_blank_lower.to_csv(input1 + "_Months_Lower.csv", index=False)
print("Threshold limit check for lower data based on" + " " + inputT1 + "%" + " " + "has been completed")

# THRESHOLD LIMIT CHECK for upper dataframe (Picking up exact value)
Result_Upper = []
for change in df_blank_upper['Change']:
    if abs(change) >= int(inputT2): #Threshold input2 = 10.58766974
        Result_Upper.append("Significant change")
    else:
        Result_Upper.append("No significant change")
df_blank_upper['Result'] = Result_Upper

#SAVE THE UPPER DATA FILES
df_blank_upper.to_csv(input1 + "_Months_Upper.csv", index=False)
print("Threshold limit check for upper data based on" + " " + inputT2 + "%" + " " + "has been completed")




print("Combining lower data file and upper data file....")

#2 CODE SCRIPTS TO COMBINE 2 CSV FILES
print("Combining both check files")
Combined_Checks = pd.concat([df_blank_lower, df_blank_upper])
Combined_Checks.to_csv('Combined_Checks.csv', index=False)

#REARRANGING COLUMNS
Combined_Checks_update = list(Combined_Checks.columns)
Combined_Checks_update[5], Combined_Checks_update[6] = Combined_Checks_update[6], Combined_Checks_update[5]
Combined_Checks = Combined_Checks[Combined_Checks_update]
Combined_Checks.to_csv('Combined_Checks.csv', index=False)
print("Combined both lower and upper data file checks completed!!!")

# COMBINE BOTH CSV FILES
# OPTIONAL CODE
#STORE FILE NAMES IN A VARIABLE
# files = [input1 + '_Months_Lower.csv', input1 + '_Months_Upper.csv']
# combined = pd.DataFrame()
# for file in files:
#     df = pd.read_csv(file, skiprows=0)
#     combined = combined.append(df, index=False, ignore_index=False)
# combined.to_csv('Combined_Checks.csv')





# CREATING THE FINAL QC FILE
print("Generating final QC file....")

#MERGE BOTH QC FILE AND COMBINED CHECKS USING A COMMON ID 'UID' COLUMN
QC = pd.read_csv("QC_File.csv", usecols=('Date_y', 'Index Category_y', 'Sub Category_y', 'Region_y', 'Index_x', 'Index_y', 'Change', 'UID'))
QC_File = pd.DataFrame(QC)
checksfile = pd.read_csv("Combined_Checks.csv", usecols=('Date_y', 'Index Category_y', 'Sub Category_y', 'Region_y', 'Change', 'Result', 'UID'))
Combined_Checks = pd.DataFrame(checksfile)

#CREATING FINAL_QC FILE - PHASE 1
QC_File_final = QC_File.merge(Combined_Checks, on='UID', how='inner')
QC_File = QC_File_final.to_csv("QC" + " " + str(QC_File_final_filename) + ".csv", index=False)

#REMOVE DUPLICATE COLUMNS FROM FINAL QC FILE
openfile = pd.read_csv("QC" + " " + str(QC_File_final_filename) + ".csv", usecols=['Date_y_x', 'Index Category_y_x', 'Sub Category_y_x', 'Region_y_x', 'Index_x', 'Index_y', 'Change_y', 'Result'])
QCFile = pd.DataFrame(openfile)
print(QCFile)
finalfile = QCFile.to_csv("QC" + " " + str(QC_File_final_filename) + ".csv", index=False)
print("QC" + " " + str(QC_File_final_filename) + ".csv" + " " + "has been created")



# CALCULATE THE ENTIRE CODE RUN PROCESS TIME
coderun_stop = process_time()
print("Elapsed time:", coderun_stop, coderun_start)
print("Elapsed time during the whole program in seconds:", coderun_stop - coderun_start)




