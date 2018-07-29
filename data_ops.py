from __future__ import unicode_literals

import xml.etree.ElementTree
import re

def expand_cont(sentence):
    global contractions
    words = sentence.split(" ")
    temp = []
    for i in words:
        if i in contractions:
            temp.append(contractions[i])
        else:
            temp.append(i)

    return " ".join(temp)

file=open("s.xml")
e = xml.etree.ElementTree.parse('s.xml').getroot()

lis=[]
for atype in e.findall('text'):
    words=[]
    print(atype.get('id'))
    s=atype.get('id')
    s=s.replace("hom_","")
    lis.append(int(s)-1)


result=[]
for i in range(2250):
    if i in lis:
        result.append(1)
    else:
        result.append(0)

file=open("result.txt","w")
for i in result:
    file.write(str(i)+"\n")

file=open("lables.txt","w")
file.write(str(result))

