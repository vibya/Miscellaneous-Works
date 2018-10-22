'''
This module reads an input file(txt) file and prints the following analysis:
 Approximate Word Count
 Approximate Sentence Count
 Average Letter Count
 Average Sentence Length
'''

import os
import re
import nltk
from nltk import sent_tokenize, word_tokenize
words =[]
letterCount = 0
sentences = []

#Prompt the user to provide the file name
inputFilename = input("Please provide the file name:")
txtfilepath = os.path.join(inputFilename)

def main():
        global letterCount, sentences
        with open(txtfilepath,encoding = 'utf-8') as inputFile:
                sentences = sent_tokenize(inputFile.read())

                #extract the words from each sentence
                for sentence in sentences:
                        pattern = re.compile(r"\w*('|->)?\w*[^-,\s\.()\W]")
                        matches = pattern.finditer(sentence)
                        for match in matches:
                                words.append(match.group())
                #count the letters in each word
                for word in words:
                        letterCount+=len(word)
        printAnalysis()
        #not generating any output file because #FollowTheInstructions #DidnotAsk-DonotDoit

def printAnalysis():
        print('-----------------')
        print('Paragraph Analysis')
        print('-----------------')
        print('Approximate Word Count: '+str(len(words)))
        print('Approximate Sentence Count: '+str(len(sentences)))
        print('Average Letter Count: '+str(letterCount/len(words)))
        print('Average Sentence Length: '+str(len(words)/len(sentences)))

if __name__ == "__main__":
    """Program to analyze a given text file 
    """
    main()
