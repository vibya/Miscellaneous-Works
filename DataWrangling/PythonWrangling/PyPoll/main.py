'''
This module reads voting records(csv) and outputs the following analysis (txt):
-Total votes
-List of candidates who received votes along with 
    -the number of votes received 
    -percentage of votes
-The winner
'''

import os
import csv

total_votes            = 0
candidates             = []
Votes_perCandidate     = []

#Prompt the user to provide the file names
inputFilename       = input("Please provide the input file name:")
header              = input("Does your input file have a header? (y)es or (n)o:")
outputFilename      = input("Please provide the output file name:")
csvpath             = os.path.join(inputFilename)

def main():
    """Read the input file and calculate the total votes, votes per candidate
    and the winner of the election.
    """
    with open(csvpath,newline="") as csvfile:
        csvreader = csv.reader(csvfile,delimiter= ",")
        if header == 'y':
            next(csvreader)
        for row in csvreader:
            #check the candidate name and accumulate votes
            calculate_Total_Votes(row[2])
        print_write_Analysis()

def calculate_Total_Votes(candidate_name):
    """Accumulate the votes per Candidate

    Args:
        candidate_name (string) : Name of the candidate who received the vote
    """
    global total_votes
    found = False
    total_votes= total_votes + 1
    for x in range(len(candidates)):
        if candidates[x] == candidate_name:                   
            Votes_perCandidate[x] += 1
            found = True
    if not(found):                                    
        candidates.append(candidate_name)
        Votes_perCandidate.append(1)

def print_write_Analysis():
    output_Filepath         = os.path.join(outputFilename)
    greatest_total          = 0

    with open(output_Filepath, 'w') as txtfile:                        
        print(" ")
        print("Election Results")
        print("-------------------------")
        print("Total Votes: "+str(total_votes))
        print("-------------------------")

        txtfile.write("Election Results")
        txtfile.write("\n-------------------------")
        txtfile.write("\nTotal Votes: "+str(total_votes))
        txtfile.write("\n-------------------------\n")
        
        for y in range(len(candidates)):
            print(candidates[y]+": "+str(round((Votes_perCandidate[y]/total_votes)*100,1))+"% ("+str(Votes_perCandidate[y])+")")
            txtfile.write(candidates[y]+": "+str(round((Votes_perCandidate[y]/total_votes)*100,1))+"% ("+str(Votes_perCandidate[y])+")\n")
            if greatest_total < Votes_perCandidate[y]:
                greatest_total = Votes_perCandidate[y]
                winner = candidates[y]

        print("-------------------------")
        print("Winner: "+winner)
        print("-------------------------")
        txtfile.write("-------------------------")
        txtfile.write("\nWinner: "+winner)
        txtfile.write("\n-------------------------")

if __name__ == "__main__":
    """Program to calculate the total votes and identify
    the winner based on the election data input file
    """
    main()

