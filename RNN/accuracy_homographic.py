file=open("out.txt")
results=eval(file.read())


file1=open("result.txt","r")
data=file1.read()
data=data.split("\n")

t=[]

for i in data:
    t.append(int(i))


true=0
false=0
ones=0

false_pos={}
false_neg=0

for i in range(2248):

    if t[i]==1 and results[i+1][0]>0:
        true+=1
    elif t[i]==0 and results[i+1][0]==0:
        true+=1
    else:
        false+=1
    if t[i]==1:
        ones+=1
    if t[i]==0 and results[i+1][0]>0:
        false_pos[i+1]=results[i+1]
    if t[i]==1 and results[i+1][0]==0:
        false_neg+=1



print(false_neg)
print(true,false,ones)
print(len(false_pos.keys()))
file=open("false_positives.txt","w")
for key,val in false_pos.items():
    file.write(str(key)+":"+str(val)+"\n")
