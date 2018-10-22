'''
This module reads an input file (csv) containing monthly revenue records and
outputs(txt) the following analysis:
-Total Months
-Total Revenue 
-Average Revenue Change
-Identify the month with Greatest Increase in Revenue
-Identify the month with Greatest Decrease in Revenue
'''
import os
import csv
import argparse

parser = argparse.ArgumentParser(description='Present the Financial Analysis of a provided budget file')
parser.add_argument('Input_file',   help='''Provide the input file name 
                                            including the relative path if not in current directory''')
parser.add_argument('Output_file',  help='''Provide the output file name
                                            including the relative path if not in current directory''')
arguments = parser.parse_args()

#Housekeeping
count           = 0
revenue         = 0
difference      = 0
storedRevenue   = 0
increase        = 0
decrease        = 0
incmonth        = " "
decmonth        = " "
averages        = []

def main(Input_file, Output_file):
    """Read the input file and calculate the total months and revenue
    along with monthly revenue differences and identify the months with
    the greatest change.
    """
    header      = input("Does your file have a header? (y)es or (n)o:")
    csvpath     = os.path.join(Input_file)
    with open(csvpath,newline="") as csvfile:
        csvreader = csv.reader(csvfile,delimiter= ",")

        #skip the header if present
        if header == 'y':                                             
            next(csvreader)                                             

        for row in csvreader:
            calcTotalRevenue(int(row[1]))
            monthlyRevenueChange(int(row[1]))
            setGreatestchanges(row[0])

        printAnalysis()
        writeAnalysis(Output_file)

def calcTotalRevenue(monthRevenue):
    """Calculate total months and revenue

    Args:
        monthRevenue(number): Monthly Revenue
    """
    global count,revenue
    count+= 1
    revenue = revenue + monthRevenue

def monthlyRevenueChange(monthRevenue):
    """Calculate monthly revenue difference and store them in a list    

    Args:
        monthRevenue(number): Monthly Revenue
    """
    global storedRevenue, difference
    global averages
    if count == 1:
        storedRevenue = monthRevenue
    if count > 1:
        averages.append(monthRevenue - storedRevenue)                
        difference  = averages[-1]
        storedRevenue = monthRevenue

def setGreatestchanges(month):
    """Identify the month with the greatest change by comparing every month difference

    Args:
        month(string): Month
    """
    global increase, decrease, incmonth, decmonth
    #greatest monthly increase
    if increase < difference:                                    
        increase  = difference
        incmonth  = month
    #greatest monthly decrease
    if decrease > difference:                                     
        decrease  = difference
        decmonth  = month

def avgRevenueChange():
    """Calculate the average revenue change by dividing the total revenue difference
    with the number of differences

    Args:
        None

    Returns:
        averageRevenuechange(number) : average of all the revenue differences
    """
    revenueDifferences = 0
    
    for x in averages:
        revenueDifferences += x  
    averageRevenuechange = revenueDifferences/len(averages)
    return averageRevenuechange

def printAnalysis():
    print("----------------------------")                        
    print("Financial Analysis")
    print("----------------------------")
    print("Total Months: "+str(count))
    print("Total Revenue: $"+str(revenue))        
    print("Average Revenue Change: $"+str(avgRevenueChange()))    
    print("Greatest Increase in Revenue: "+ incmonth + " ($"+ str(increase)+")")
    print("Greatest Decrease in Revenue: "+ decmonth + " ($"+ str(decrease)+")")

def writeAnalysis(output_file):
    output_path = os.path.join(output_file)
    with open(output_path, 'w') as txtfile:
        txtfile.write("Financial Analysis")
        txtfile.write("\n----------------------------")
        txtfile.write("\nTotal Months: "+str(count))
        txtfile.write("\nTotal Revenue: $"+str(revenue))
        txtfile.write("\nAverage Revenue Change: $"+str(avgRevenueChange()))
        txtfile.write("\nGreatest Increase in Revenue: "+ incmonth + " ($"+ str(increase)+")")
        txtfile.write("\nGreatest Decrease in Revenue: "+ decmonth + " ($"+ str(decrease)+")")

if __name__ == "__main__":
    """Program to calculate the total revenue, months,
    average change and greatest change in revenue based on the input file
    """
    main(arguments.Input_file, arguments.Output_file)
    