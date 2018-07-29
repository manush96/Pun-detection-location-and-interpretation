import xml
import xml.etree.ElementTree
import re
import pprint
file=open("homographic_location_gold.txt","r")
data=file.read()

data=data.split("\n")

print(len(data))

e = xml.etree.ElementTree.parse("subtask2-homographic-test.xml").getroot()

sentences={}

for atype in e.findall('text'):
    words=[]
    sentences[atype.get('id')]=[]
    for i in atype.getchildren():

        words.append(i.text)
    temp=[]
    for j in range(len(words)-1):
        if words[j]=="'":
            temp.append(words[j-1]+words[j]+words[j+1])
    sentences[atype.get('id')]=words

print(sentences["hom_24"])
location_results_expected={}
for i in data:
    i=i.split()
    pos=re.sub('hom_[0-9]*_','',i[1])
    print(i[0],pos)
    location_results_expected[i[0]]=sentences[i[0]][int(pos)-1]

print(location_results_expected)


file=open("pun_words.txt","w")
for i in location_results_expected.keys():
    file.write(i+"  "+location_results_expected[i])
    file.write("\n")

file4=open("result4.txt")

output=eval(file4.read())
t={}


for i in output.keys():
    if i<1421:
        t[i]=output[i]
    if i>=1421 and t<1571:
        t[i+1]=output[i]
    else:
        t[i+2]=output[i]
output=t


file=open("s_out.txt","w")
for i in output.keys():
    file.write(str(i)+":"+str(output[i]))
    file.write("\n")
t={}
for i in output.keys():
    t["hom_"+str(i)]=output[i]

output=t

t={}

count=0
print(t)
file7=open("tester.txt","w")
file7.write(str(t))
true=0
false=0

for i in location_results_expected.keys():
    if i in output:
        if len(output[i][-1])!=0:
            if location_results_expected[i].lower() in output[i][-1]:
                true+=1
            else:
                false+=1
        else:
            count+=1
            false+=1

print(true)
print(false)
print(count)