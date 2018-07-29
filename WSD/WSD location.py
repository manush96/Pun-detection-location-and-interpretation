from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize
import sys
from nltk.corpus import stopwords

reload(sys)
sys.setdefaultencoding('UTF8')

#configuring POSTagger
stanford_pos_dir = '/Users/shaivalpatel/Downloads/stanford-postagger-full-2018-02-27/'
eng_model_filename = stanford_pos_dir + 'models/english-left3words-distsim.tagger'
my_path_to_jar = stanford_pos_dir + 'stanford-postagger.jar'

st = StanfordPOSTagger(model_filename=eng_model_filename, path_to_jar=my_path_to_jar)

import nltk

dict = open('dict.txt','r')

dict=dict.read()

newdict = eval(dict)
print newdict
s= open('sent.txt','r')
s=s.read()
data = eval(s)
from pywsd.lesk import simple_lesk
f= open('raw_sent2.txt','r')
f1 = open('result7.txt', 'w')

dict={}

ndata = f.read()
ndata = ndata.split('\n')
results={}
num=1
for sents in data:


    sentences = [sents]
    print(sentences)





    #ngram generator
    def generate_ngrams(n, data):
        data = data.split(" ")
        n_grams = []
        for i in range(len(data) - n + 1):
            k = 0
            str = ""
            while k < n:
                str += data[i + k] + " "
                k += 1
            str = str.rstrip()
            n_grams.append(str)
        return n_grams
    #assigning context window according to the sentence length
    if len(sentences[0].split())>10:

            trigrams = generate_ngrams(5, sentences[0])
    elif len(sentences[0].split())>8 and len(sentences[0].split())<=10:
        trigrams = generate_ngrams(4, sentences[0])
    elif len(sentences[0].split())<=8:
        print 1
        trigrams = generate_ngrams(3, sentences[0])


    #getting POS tags for the words
    def get_pos_tags(data):
        words = word_tokenize(data)
        pos_dict = st.tag(words)
        encoded = [[s.encode('utf8') for s in t] for t in pos_dict]

        return encoded


    dict = {}

    context = sentences[0].split()
    from nltk.corpus import wordnet

    #converting Stanford POS tags to wornet tags
    def get_wordnet_pos(treebank_tag):

        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return ''


    for i in get_pos_tags(sentences[0]):
        try:

            dict[i[0]] = simple_lesk(sentences[0], i[0], get_wordnet_pos(i[1]))



        except IndexError:
            print sentences[0]
            dict[i[0]] = simple_lesk(sentences[0], i[0])

            continue

    flag = 0
    s=[]
    for i in trigrams:

        for j in get_pos_tags(i):
            try:
                #getting word sense for words and checking if there is a conflict, if there is we raise a flag
                if simple_lesk(i, j[0], get_wordnet_pos(j[1])) != dict[j[0]] and newdictj[0]<10:
                    flag += 1
                    s.append(j[0])

            except IndexError:
                    continue

    print(flag,s)

    results[sentences[0]]=[flag,s]


    j=num
    f1 = open('result7.txt', 'a')
    print j, sentences[0]
    f1.write(str(j)+":"+str(results[sentences[0]])+"\n")


    num+=1






