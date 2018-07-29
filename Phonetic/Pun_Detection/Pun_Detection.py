
#All imports
from __future__ import print_function
import phrasefinder as pf
import pronouncing as pp
import Levenshtein
import nltk
import glob, os
from nltk.corpus import stopwords

#Function to get frequency of a ngram from large corpus
def main(query,resultdict):
	# Set up your query.

	#set the maximum number of phrases to return.
	options = pf.SearchOptions()
	options.topk = 1

	# Send the request.
	try:
		result = pf.search(pf.Corpus.AMERICAN_ENGLISH, query, options)
		if result.status != pf.Status.OK:
			resultdict[query] = 0
			return

		for phrase in result.phrases:
			if query in resultdict.keys():
				resultdict[query] = resultdict[query] + phrase.match_count
			else:
				resultdict[query] = phrase.match_count

		if query not in resultdict.keys():
			resultdict[query] = 0

	except Exception as error:
		resultdict[query] = 0
		return

#Function to get frequency of a ngram based query from large corpus
def new_main(query,resultdict):
	# Set up your query.

	#set the maximum number of phrases to return.
	options = pf.SearchOptions()
	options.topk = 30

	# Send the request.
	try:
		result = pf.search(pf.Corpus.AMERICAN_ENGLISH, query,options)
		if result.status != pf.Status.OK:
			return

		for phrase in result.phrases:
			skey = ""
			for token in phrase.tokens:
				skey = skey + token.text + " "
			resultdict[skey] = phrase.match_count

	except Exception as error:
		return

#Function for generating ngrams
def ngrams(data, n):
	#Creating a list to store n grams
	lst=list()

 	#Intially splitting file using spaces
	data = data.split()

	#Ordered List
	ordered_list= []

	#Making ngrams
	for i in range(len(data)-n+1):
		#Apending data in ordered_list
		ordered_list = ' '.join(data[i:i+n])

		#Apending data in normal list
		lst.append(ordered_list)
	#Returning list
	return lst

#Function for generating rhyming word of given word
def rhyme(word, level):

	#Using cmu dict of nltk
	entries = nltk.corpus.cmudict.entries()

	#Getting syllables of the given word
	syllables = [(wrd, syl) for wrd, syl in entries if wrd == word]
	rhymes = []

	#Finding rhymes of word
	for (wrd, syllable) in syllables:
		rhymes += [wrd for wrd, pron in entries if pron[-level:] == syllable[-level:]]
	return set(rhymes)

#Function to check whether two given word are rhyming of each other
def doTheyRhyme ( word1, word2 ):
	if not word1 in rhyme ( word2, 1 ):
		if Levenshtein.distance(word1,word2) < 3:
			return True
		else:
			return False
	else:
		return True

#Function to calculate Levenshtein Distance
def leven_distance(old_word, new_word):

	#1st Technique
	w_len_ch_old = len(old_word)
	w_len_ch_new = len(new_word)
	w_len_ch = min(w_len_ch_old ,w_len_ch_old)

	#distance
	dis_ch = Levenshtein.distance(old_word,new_word)
	ratio_ch =  (w_len_ch - dis_ch)/w_len_ch

	#2nd and 3rd Technique
	#Checking if phonetic representation exisist or not
	if(len(pp.phones_for_word(old_word)))>0 and len(pp.phones_for_word(new_word))>0:

		#2nd Technique
		#Getting phonetic representation
		old_word_phs = pp.phones_for_word(old_word)[0]
		new_word_phs = pp.phones_for_word(new_word)[0]

		w_len_phs_old = len(old_word_phs)
		w_len_phs_new = len(new_word_phs)

		w_len_phs = min(w_len_phs_old,w_len_phs_new)

		#distance
		dis_phs  = Levenshtein.distance(old_word_phs, new_word_phs)
		ratio_phs =  (w_len_phs - dis_phs)/w_len_phs

		#3rd Technique
		#Getting phonetic representation without spaces
		old_word_ph = old_word_phs.replace(" ","")
		new_word_ph = new_word_phs.replace(" ","")

		w_len_ph_old = len(old_word_ph)
		w_len_ph_new = len(new_word_ph)

		w_len_ph = min(w_len_ph_old,w_len_ph_new)

		#distance
		dis_ph  = Levenshtein.distance(old_word_ph, new_word_ph)
		ratio_ph =  (w_len_ph - dis_ph)/w_len_ph

	#Assigning a large value to get only true cases
	else:
		ratio_ph  = -1000
		ratio_phs = -1000

	#Returning max ratio from all three Technique
	ratio = max(ratio_ch, ratio_ph, ratio_phs)

	#Assigning smallest value to get only true cases
	if(ratio > 0.3):
		return ratio
	else:
		return 0.0001

#Function to calculate score of two trigram
def score_function(new_trigram ,old_trigram ,old_word, new_word):
	#Calculating Levenshtein distance
	ratio = leven_distance(old_word, new_word)

	if(ratio > 0.3):
		trigram_freq_dict = dict()
		len_new_word = 10

		#Getting frequency of new and old trigram
		main(new_trigram ,trigram_freq_dict)
		main(old_trigram ,trigram_freq_dict)
		score = (trigram_freq_dict[new_trigram] - trigram_freq_dict[old_trigram]) - (1/(ratio ** len_new_word))
	else:
		score = -1

	return score

#Function to calculate score of two trigram
def score_pair(new_trigram ,old_trigram ,old_word, new_word, score_pair_dict):

	score_pair_dict.update({old_word+" "+new_word : score_function(new_trigram ,old_trigram ,old_word, new_word)})
	return score_pair_dict

#Function to detect whether given sentence is pun or not
def detect(query,count,output_dict):
	query= query.lower()
	if len (query.split()) > 3:
		trigrams = ngrams(query.lower(),4)
	else:
		trigrams = ngrams(query.lower(),3)

	score_pair_dict = dict()

	POS_Tag_Set =("NN","NNS","JJ","JJR","JJS","RBR","RB","RBS","VB","VBD","VBG","VBN","VBP","VBZ","CD")
	for trigram in trigrams:

		fdict = dict()
		main(trigram, fdict)
		if fdict[trigram] > 500:
			continue
		else:
			unigrams = ngrams(trigram,1)

			#Filtering unigrams
			unigram_pos_tags = nltk.pos_tag(unigrams)

			for unigram_tagged in unigram_pos_tags:
				if(unigram_tagged[1] not in POS_Tag_Set):
					unigrams.remove(unigram_tagged[0])

			for unigram in unigrams:
						#Considering every unigram and creating new key
						query_trigram  = trigram.replace(unigram , "?")
						replace_dict = dict()

						#Getting one word different trigram
						new_main(query_trigram, replace_dict)


						#Creating set out of the trigram used for searching
						new_keyset = set(query_trigram.split())

						#Checking we get atleast 1 replacable trigram
						if len(replace_dict.keys())>0:
							for new_trigram in replace_dict.keys():
								diffset = set()

								#Creating set out of the new trigram
								matchkeyset = set(new_trigram.lower().split())

								#Getting the word which is changed in the trigram
								diffset = diffset.union(new_keyset.symmetric_difference(matchkeyset))

								#Removing the query character
								if "?" in diffset:
									diffset.remove("?")

								#If old and new word are same then we have to remove it from list
								if unigram in diffset:
										diffset.remove(unigram)

								#Finally getting new word
								if len(diffset) > 0:
											new_word = list(diffset)[0]

											POS_Tag_Set =("NN","NNS","JJ","JJR","JJS","RBR","RB","RBS","VB","VBD","VBG","VBN","VBP","VBZ","CD")

											tag_new_word = nltk.pos_tag(new_word)

											if (tag_new_word[0][1] in POS_Tag_Set) and not (new_word in set(stopwords.words('english'))) and doTheyRhyme(unigram , new_word):
												#Calculating score of two trigrams
												score_pair_dict = score_pair(new_trigram ,trigram ,unigram, new_word, score_pair_dict)


	if len(score_pair_dict.keys()) > 0:

			#Find the max value
			pair = max(score_pair_dict, key=score_pair_dict.get)

			#For pun print 1 vice versa
			if score_pair_dict[pair] > 0:
					output_dict.update({"het_" + str(count) : str(1)})
					print(count)
			else:
					output_dict.update({"het_" + str(count) : str(0)})
					print(count)
	else:
			output_dict.update({"het_" + str(count) : str(0)})
			print(count)

test_data_path= input("Enter Path of Test Data :")
output_path= input("Enter Path of Output File:")
os.chdir(test_data_path)
#getting all .txt files
for file in glob.glob("*"):
	output_dict = dict()
	#opening .txt files one by one
	with open(file,"r",encoding="ISO-8859-1") as f:

		#reading files one by one
		lines=f.readlines()
		count = 49

		#Detecting the puns
		for line in lines:
				count = count + 1
				detect(line,count,output_dict)

				#Writing the output
				with open(output_path+"/Output.txt","w+") as fu:
					fu.write(str(output_dict))
