This is readme file for Pun Detection, Pun Location and Pun Generation By Context Normativeness and Phonetic Similarity

How to run:
1. Install Pythonv3.6.4
2. Run the implementation by entering command on your command line python by command -
   python filename
3.The program asks
a)Enter Path of Test Data :
b)Enter Path of Output File:

Path of Test Data is the path of folder where all the text files are stored which have puns to be detected
Path of Output File is the path of the folder where you want to store the output result

For running the programs you need all of these.
from __future__ import print_function
import phrasefinder as pf
import pronouncing as pp
import Levenshtein
import nltk
import glob, os
from nltk.corpus import stopwords

For the sake of convienience all the Task Contains Phrase Finder Api with it. So always run the files with the given files kept in same folder.
You need to install nltk and pronouncing libraries of python
You also need to install stopwords corpus from nltk and cmudict.
You also need to install Levenshtein Libraray of python.

We have given sample input and output of each task. Input is in data folder and output is in output folder.