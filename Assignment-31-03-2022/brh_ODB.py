melanogaster_as_q=#'PERCORSO_FILE'
pseudoobscura_as_q=#'PERCORSO_FILE'

conv_melasq=#'PERCORSO_FILE_ID_CONVERTED_TO_REFSEQ'
conv_pseasq=#'PERCORSO_FILE_ID_CONVERTED_TO_REFSEQ'

#In this part we take only the first hit in order to make a plot of the distribution of the percentage of identity of the blastp 
def firsthitpident(blastp):
    d={}
    with open(blastp) as file:
        for line in file:
            if not line.startswith('#'):
                x=line.split()
                if x[0] not in d.keys():
                    d.setdefault(x[0],x)
    
    def floatorint(string):
        if string.isdigit() == True :
            return int(string)
        elif string.isdigit() == False :
            return float(string)
    
    dros=[]
    for k in d.values():
        dros.append([k[0],k[1],floatorint(k[2])])
    return dros

dmel=firsthitpident(melanogaster_as_q)
dpse=firsthitpident(pseudoobscura_as_q)

mel={}
pse={}
for line in dmel:
    if line[2] >= 55:
        mel.setdefault(line[0],line)
for line in dpse:
    if line[2]>=55:
        pse.setdefault(line[0],line)

import pandas as pd
cols = 'qseqid sseqid pident'.strip().split(' ')
x=pd.DataFrame(dmel,columns=cols)
y=pd.DataFrame(dpse, columns=cols)

import matplotlib.pyplot as plt
plt.hist(x['pident'],bins=30, range=[0,100],rwidth=0.8, color='blue')
plt.hist(y['pident'], bins=30, range=[0,100], rwidth=0.8,color ='red')

#From here starts the process to find the Best Reciprocal Hits in the blastp

def blastp_2ndhitratio(blastp,perc):
    
    def floatorint(string):
        if string.isdigit() == True :
            return int(string)
        elif string.isdigit() == False :
            return float(string)
    
    with open(blastp) as gen:
        d={}
        for l in gen:
            if not l.startswith('#'):
                line=l.split()
                if not line[0] in d.keys():
                    if floatorint(line[2]) >= perc:
                        d.setdefault(line[0],[line])
                        s=next(gen).split()
                        if not s[0].startswith('#'):
                            if s[0] in d.keys():
                                d[s[0]].append(s)
                            elif s[0] not in d.keys():
                                if floatorint(s[2])>= perc:
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

reorderedmelq=blastp_2ndhitratio(melanogaster_as_q,55)
reorderedpseq=blastp_2ndhitratio(pseudoobscura_as_q,55)

redmelqconv=blastp_2ndhitratio(conv_melasq,55)
redpseqconv=blastp_2ndhitratio(conv_pseasq,55)

def getbrh(diz1,diz2,thrs):
    file1={}
    for k,v in diz1.items():
        if len(v)==3:
            if v[2]>thrs:
                file1.setdefault(k,v)
        elif len(v)==2:
            if v[1]>thrs:
                file1.setdefault(k,v)
    file2={}
    for k,v in diz2.items():
        if len(v)==3:
            if v[2]>thrs:
                file2.setdefault(k,v)
        elif len(v)==2:
            if v[1]>thrs:
                file2.setdefault(k,v)
    brh=[]
    for k in file1.keys():
        x=(k[1],k[0])
        if x in file2.keys():
            brh.append(k)
    brh2=[]
    for k in file2.keys():
        x=(k[1],k[0])
        if x in file1.keys():
            brh2.append(k)
    counter=0
    for k in brh:
        x=(k[1],k[0])
        for j in brh2:
            if x==j:
                counter+=1
    if counter==len(brh):
        return brh
    else:
        return print('ERROR')

bestrep=getbrh(reorderedmelq,reorderedpseq,0.7)
bestrepconv=getbrh(redmelqconv,redpseqconv,0.7)
