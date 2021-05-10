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

dict1=gtfprotid('genomic_melanogaster.gtf')

dict2=gtfprotid('genomic_pseudobscura.gtf')




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
                if get_key(nextline[1]) !=  get_key(line[1]):
                    d.setdefault(line[0], [line[0:], nextline, ((float(line[11]) - float(nextline[11]))/ float(line[11]) ) ])
                    break
                i+=1
                nextline = mylist[(idx + i) % len(mylist)]
                
        elif line[0] in d.keys():
            continue

    d2={}
    for k,v in d.items():
        d2.setdefault(tuple(v[0][0:2]), v[0:])

    return d2


outdict=checkhit('Dmel_vs_Dpse.txt',dict2)
outdict=checkhit('Dpse_vs_Dmel.txt',dict1)
   
