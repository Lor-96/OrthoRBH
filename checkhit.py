def gtfprotid(gtf):
    with open(gtf,'r') as file:
        file=file.readlines()
        data= [line.split('\t') for line in file if not line.startswith('#')]
        cds= list(filter(lambda i:i[2]== 'CDS', data))
        annlist= [[i[0], i[3], i[4], i[6], i[8].split(';')] for i in cds]
        filt=[]
        for i in annlist:
            for e in i[4]:
               if 'protein_id' in e:
                   filt.append([i[4][0].split(),i[4][1].split(),e.split()])
        filt=[[i[0][1].strip('"'), i[1][1].strip('"'), i[2][1].strip('"')] for i in filt]
        d={}
        for i in filt:
            d.setdefault(i[0],[]).append(i[2])
            
    return d

path=('C:\\Users\\color\\Desktop\\Practice\\Directory Melanogaster\\genomic_melanogaster.gtf')
dict1=gtfprotid(path)


path2=('C:\\Users\\color\\Desktop\\Practice\\Directory Pseudobscura\\genomic_pseudobscura.gtf')
dict2=gtfprotid(path2)

del(path,path2)


def checkhit(data, dictionary):
    file = open(data,'r')
    file= file.readlines()
    mylist=[line.split() for line in file if not line.startswith('#')]
    
    def get_key(val):
        for key, value in dictionary.items():
            for x in value:
                if val == x:
                    return key

    d={}
    for idx, line in enumerate(mylist):
        if not line[0] in d.keys():
            i=1
            nextline = mylist[(idx + i) % len(mylist)]
            while True:
                if nextline[0] == line[0]:
                    if get_key(nextline[1]) !=  get_key(line[1]):
                        d.setdefault(line[0], [line[0:], nextline, ((float(line[11]) - float(nextline[11]))/ float(line[11]) ) ])
                        break
                    i+=1
                    nextline = mylist[(idx + i) % len(mylist)]
                    
                elif nextline[0] != line[0]:
                    d.setdefault(line[0], [line[0:], ((float(line[11]) / float(line[11]) ) )])
                    break
                
        elif line[0] in d.keys():
                continue
                
        

    d2={}
    for k,v in d.items():
        d2.setdefault(tuple(v[0][0:2]), v[0:])

    return d2


outdict=checkhit('Dmel_vs_Dpse.txt',dict2)
outdict2=checkhit('Dpse_vs_Dmel.txt',dict1)

def table(diz):
    text=[]
    for k,v in diz.items():
        text.append(str([k,v[0][1],v[1][1],v[2]]))
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

file1=table(outdict)
with open('DmelDpse.txt','w') as t:
    for line in file1:
        t.write(line + '\n')
    
file2=table(outdict2)
with open('DpseDmel.txt','w') as t:
    for line in file2:
        t.write(line + '\n')
   
