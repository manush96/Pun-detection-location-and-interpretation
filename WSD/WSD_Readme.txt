Things to import to run the program

from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize
import sys
from pywsd.lesk import simple_lesk



stanford_pos_dir = '/Users/shaivalpatel/Downloads/stanford-postagger-full-2018-02-27/'

Change the above directory to the folder of stanfordpostagger that we are providing  in the zip file.

from pywsd.lesk import simple_lesk

The whole program is written in python 2.7 using pycharm


result.txt has the results of each sentence in the data set.Where it is a key value pair and each key is the sentence number in the data and value is a list of number of flags raised and the words with conflicting senses.
If the flag value is greater than 0 than pun has been detected

sent.txt has the has the dataset


Dict.txt has the frequency of all the words in the dataset

result4.txt has the location of the pun in the sentence where some words has a list of words with conflicting senses but the last word in the list is word which comes by the intuition of the baseline model for pun detection.


Inter.py has the code for pun interpretation 

Import the following for inter.py

from pywsd.lesk import simple_lesk
import sys

raw_Sents2.txt has the data for pun interpretation and pun_words.txt is the list of pun words which will be given as input

Subtask_2_evaluation.py has the code that we used to evaluate the results of pun location

homographic_location_gold.txt has the original location of the puns in the data

subtask2-homographic-test.xml has the data in the form of xml
