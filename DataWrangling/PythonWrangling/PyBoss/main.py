'''
This module reformats the input employee file(csv) and outputs a reformatted file
with the following conversions:
-Name split into First Name and Last Name
-DOB converted to MM/DD/YYYY format
-SSN showing only last 4 digits and first five masked with *
-State abbreviated to its two-letter code
'''

import datetime
import csv
import os
import argparse
import us_state_abbrev

parser = argparse.ArgumentParser(description='Reformat the given input file containing employee data')
parser.add_argument('Input_file',   help='''Provide the input file name 
                                            including the relative path if not in current directory''')
parser.add_argument('Output_file',  help='''Provide the output file name
                                            including the relative path if not in current directory''')
arguments = parser.parse_args()


reformatted_file_data = []

def main(Input_file, Output_file):
    """Reads the input file
    Reformats the data and writes in to an output file
    """
    readFile(Input_file)
    writeFile(Output_file)
    print(Input_file+"-> Input File processed. \n"+ Output_file +"-> Output File generated")

def readFile(inputFilepath):
    """Reads the input file and reformats as required

    Args:
        inputFilepath(string) : path where the input file is present
    """
    with open(inputFilepath) as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            empid   = row["Emp ID"]
            name    = row["Name"].split()
            fname   = name[0]
            lname   = name[1]
            dob     = datetime.datetime.strptime(row["DOB"],'%Y-%m-%d').strftime('%m/%d/%Y')
            ssn     = '***-**-'+(row["SSN"][7:11])
            state   = row["State"]
            reformatted_file_data.append(
                {
                "Emp ID": empid,
                "First Name": fname,
                "Last Name": lname,
                "DOB": dob,
                "SSN": ssn,
                "State":us_state_abbrev.us_state_abbrev[state]
                }
            )

def writeFile(outputFilepath):
    """Writes the reformatted data in to the output file

    Args:
        outputFilepath(string) : Path where the output file should be placed
    """
    with open(outputFilepath, "w") as csvfile:
        fieldnames = ["Emp ID", "First Name", "Last Name", "DOB", "SSN", "State"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        writer.writerows(reformatted_file_data)

if __name__ == "__main__":
    """Program to read the input file and generate a reformatted output file
    """
    main(arguments.Input_file, arguments.Output_file)