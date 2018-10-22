This module reads an input file (csv) containing monthly revenue records and
outputs(txt) the following analysis:
-Total Months


-Total Revenue 


-Average Revenue Change


-Identify the month with Greatest Increase in Revenue


-Identify the month with Greatest Decrease in Revenue

# The script will prompt the user to indicate if the input file has a header

There are four input files - 

2 original input files


2 files with same data as input files but with no header


This is how the script has to be invoked as follows with 2 arguments

# $python main.py inputfile outputfile

inputfile --> is the filename.csv if its in the same directory as the script
or folder/filename.csv - depending on where the file is located relative to the current script location

outputfile --> is filename.txt if the file should be placed in the same directory as the script
or folder/filename.txt - if it has to be placed in a different folder relative to the current script location

eg: sample script execution with file names provided
# $python main.py budget_data_1.csv output1.txt
