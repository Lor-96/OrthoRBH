def checkhit(data):

    d={}
    with open(data, 'r') as gen:
        for l in gen:
            if not l.startswith('#'):
                line=l.split()
                if not line[0] in d.keys():
                    d.setdefault(line[0], [line])
                    s=next(gen).split()
                    if not s[0].startswith('#'):
                        if s[0] in d.keys():
                            d[s[0]].append(s)
                        elif s[0] not in d.keys():
                            d.setdefault(s[0],[s])
             
        for k,v in  d.items():
            if not len(v)==2:
                if len(v) == 1:
                    v.append(float(v[0][11])/float(v[0][11]))
            else:
                if not len(v)== 3:
                    v.append((float(v[0][11]) - float(v[1][11]))/float(v[0][11]))

        d2={}
        for k,v in d.items():
            d2.setdefault(tuple(v[0][0:2]), v[0:])
        
        return d2

def table(diz):
    text=[]
    for k,v in diz.items():
        if  len(v)== 3:
            text.append(str([k,v[0][1],v[1][1],v[2]]))
        elif len(v)==2:
            text.append(str([k,v[0][1],v[0][1],v[1]]))
    data=[]
    for line in text:
        data.append(line.split())
    l=[]
    for line in data:
        l.append([line[0].strip("[],('"),line[2].strip("[],('"),line[3].strip("[],('"), line[4].strip("[],('")])
    x=[]
    for line in l:
        x.append("\t".join(line))
    return x

path1='C:/Users/color/Desktop/orthodb/ODBcomparison/bestmel_vs_bestpse95/noiso/noiso_ODBMel_DB_vs_ODBPse.txt'
path2='C:/Users/color/Desktop/orthodb/ODBcomparison/bestmel_vs_bestpse95/noiso/noiso_ODBPse_DB_vs_ODBMel.txt'

data1=checkhit(path1)
data2=checkhit(path2)

file1=table(data1)
with open('PSEasq_vs_MELDB_table.txt','w') as t:
    for line in file1:
        t.write(line + '\n')
        
file2=table(data2)
with open('MELasq_vs_PSEDB_table.txt','w') as t:
    for line in file2:
        t.write(line + '\n')

file1=[line.split('\t') for line in file1]
file2=[line.split('\t') for line in file2]

def floatorint(string):
        if string.isdigit() == True :
            return int(string)
        elif string.isdigit() == False :
            return float(string)

dat1=[]
for line in file1:
    dat1.append([line[0],line[1],line[2],floatorint(line[3])])

dat2=[]
for line in file2:
    dat2.append([line[0],line[1],line[2],floatorint(line[3])])

del(data1,data2,file1,file2,line,t)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
colnames=['Query','1st_Hit','2nd_Hit','Bitscore_ratio']
df=pd.DataFrame(dat1,columns=colnames)
df2=pd.DataFrame(dat2,columns=colnames)
num_bins=30

n, bins, patches = plt.hist(df['Bitscore_ratio'], num_bins, facecolor='blue', alpha=0.5,rwidth=0.8)
plt.xlabel('Bitscore Ratio')
plt.ylabel('Frequency')
plt.title('Pseudoobscura as Query', loc='center')
plt.show()

n, bins, patches = plt.hist(df2['Bitscore_ratio'], num_bins, facecolor='blue', alpha=0.5,rwidth=0.8)
plt.xlabel('Bitscore Ratio')
plt.ylabel('Frequency')
plt.title('Melanogaster as Query', loc='center')
plt.show()
