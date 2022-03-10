#New function to check hits of BLAST to make BRH 

def checkhitODB(blast):
    with open(blast,'r') as data:
        d={}
        for l in data:
            if not l.startswith('#'):
                line=l.split()
                if not line[0] in d.keys():
                    s=next(data).split()
                    if s[0] == line[0]:
                        d.setdefault(line[0],[line,s])
                    else:
                        d.setdefault(line[0], [line])
    
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

#Result on the BLASTP for Pseudoobscura as DB vs Melanogaster 13491 hits and for Melanogaster as DB vs Pseudoobscura 13400 hits
