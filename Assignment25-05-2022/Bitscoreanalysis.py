path1='C:/Users/color/Desktop/orthodb/ODBcomparison/bestmel_vs_bestpse95/noiso/noiso_ODBMel_DB_vs_ODBPse.txt'
path2='C:/Users/color/Desktop/orthodb/ODBcomparison/bestmel_vs_bestpse95/noiso/noiso_ODBPse_DB_vs_ODBMel.txt'

def takethefirstrow(blastp):
    d={}
    with open(blastp, 'r') as gen:
        for l in gen:
            if not l.startswith('#'):
                line=l.split()
                if not line[0] in d.keys():
                    d.setdefault(line[0],line)
    return d

org1= takethefirstrow(path1)
org2= takethefirstrow(path2)
                
def tableID(dictionary):
    def floatorint(string):
        if string.isdigit() == True :
            return int(string)
        elif string.isdigit() == False :
            return float(string)
    text=[]
    for k,v in dictionary.items():
        text.append([str(k),str(v[1]),floatorint(v[2])])
   
    return text

n1=tableID(org1)
n2=tableID(org2)

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
colnames=['Query','1st_Hit','% ID']
df1=pd.DataFrame(n1, columns=colnames)
df2=pd.DataFrame(n2, columns=colnames)
num_bins=30

n, bins, patches = plt.hist(df1['% ID'], num_bins, facecolor='red', alpha=0.5,rwidth=0.8)
plt.xlabel('% ID')
plt.ylabel('Frequency')
plt.title('Pseudoobscura as Query', loc='center')
plt.show()

num_bins=30

n, bins, patches = plt.hist(df2['% ID'], num_bins, facecolor='red', alpha=0.5,rwidth=0.8)
plt.xlabel('% ID')
plt.ylabel('Frequency')
plt.title('Melanogaster as Query', loc='center')
plt.show()
