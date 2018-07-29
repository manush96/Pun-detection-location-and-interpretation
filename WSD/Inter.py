from pywsd.lesk import simple_lesk
import sys


reload(sys)
sys.setdefaultencoding("utf8")
file=open("pun_words.txt","r")

data=file.read()

data=data.split("\n")
sent_id={}
for i in data:
    i=i.split()
    print(i)
    sent_id[i[0]]=i[1]
file.close()
file=open("raw_sent2.txt","r")

data=file.read()

data=data.split("\n")
sent_dict={}
counter=1
for i in data:
    sent_dict["hom_"+str(counter)]=i
    counter+=1
print(len(sent_id))
print (len(sent_dict))
synsets={}
list=[]
for i in sent_id:
    print sent_dict[i],sent_id[i]
    synsets[sent_id[i]]=simple_lesk(sent_dict[i],sent_id[i])
    list.append((sent_id[i],simple_lesk(sent_dict[i],sent_id[i])))



file=open("interpretation.txt","w")
for i in list:
    file.write(str(i))
    file.write("\n")

print list