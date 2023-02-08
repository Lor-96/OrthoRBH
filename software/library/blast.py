class Blast:

        def __init__(self, path):
                self.path= path

        """
        The following functions allow us to read the blast output and ...
        """

        def top1hit(self,percentage):
                def floatorint(string):
                        if string.isdigit() == True:
                                return int(string)
                        if string.isdigit() == False:
                                return float(string)
                d={}
                with open(self.path, 'r') as file:
                        for line in file:
                                if not line.startswith('#'):
                                        columns= line.split('\t')
                                        if not columns[0].strip() in d.keys():
                                                value=[columns[0].strip(),columns[1].strip()] + list(map(floatorint,columns[2:]))
                                                d.setdefault(value[0],value)
                d={k:v for k,v in d.items() if v[2] >= percentage}
                return d

        def top2hit(self, percentage):
                def floatorint(string):
                        if string.isdigit() == True :
                                return int(string)
                        elif string.isdigit() == False :
                                return float(string)
                with open(self.path,'r') as file:
                        d={}
                        for line in file:
                                if not line.startswith('#'):
                                        columns=line.split('\t')
                                        if not columns[0].strip() in d.keys():
                                                v=[columns[0].strip(),columns[1].strip()] + list(map(floatorint,columns[2:]))
                                                d.setdefault(v[0],[v])
                                                successive=next(file).split('\t')
                                                if not successive[0].startswith('#'):
                                                    if v[1].strip() == successive[1].strip():
                                                        while successive[1].strip() == v[1].strip():
                                                            successive=next(file).split('\t')
                                                            if successive[0].strip().startswith('#'):
                                                                break
                                                if not successive[0].startswith('#'):
                                                        if successive[0].strip() in d.keys():
                                                                val=[successive[0].strip(),successive[1].strip()]+list(map(floatorint,successive[2:]))
                                                                d[val[0]].append(val)
                                                        elif successive[0].strip() not in d.keys():
                                                                val=[successive[0].strip(),successive[1].strip()]+list(map(floatorint,successive[2:]))
                                                                d.setdefault(val[0],[val])
                d1={k:v for k,v in d.items() if v[0][2] >= percentage}
                for k,v in  d1.items():
                        if len(v) == 1:
                                v.append(v[0][11]/v[0][11])
                        elif len(v)== 2:
                                v.append((v[0][11] - v[1][11])/v[0][11])
                d2={}
                for k,v in d1.items():
                        k=v[0][0].strip() + '\t' + v[0][1].strip()
                        d2.setdefault(k, v[0:])
                return d2
          
        def conversiontable(self,percentage):
                from functools import reduce
                def floatorint(string):
                        if string.isdigit() == True :
                                return int(string)
                        elif string.isdigit() == False :
                                return float(string)

                with open(self.path,'r') as gen:
                        d={}
                        count=0
                        for line in gen:
                                if line.startswith('# Query:'):
                                        query=line
                                if line.startswith('# BLAST processed'):
                                        end=line.strip('# BLAST processed ')
                                if line.startswith('# 0 hit'):
                                        count+=1
                                        print(query.strip('\n')+ ' has no hit in the BLAST file')
                                if not line.startswith('#'):
                                        l=line.split('\t')
                                        if not l[0].strip() in d.keys():
                                                v=[l[0],l[1]] + list(map(floatorint,l[2:]))
                                                d.setdefault(l[0].strip(),[v])
                        print('The total of the 0 hits in the BLAST is: '+str(count)+' out of '+end)
                        print('The total of the hits with more than 0 hit in the BLAST is: '+str(len(d.keys()))+' out of '+end)
    
                        d1={k:v[0] for k,v in d.items() if v[0][2] >= percentage}
                        print('The total of the first hit for all queries with a percentage = '+str(percentage)+'%  are: '+str(len(d1.keys())))
                        print(str(len(d.keys()) - len(d1.keys()))+' hits are lower than '+str(percentage)+'%')
    
                        d2={}
                        for k,v in d1.items():
                                d2.setdefault(v[1],[]).append(v)
                        print('Swapping the order of OrthoDB and RefSeq there are: '+str(len(d1.keys()) - len(d2.keys()))+' IDs of OrthoDB that are associated with more than one RefSeq ID')
                        print('The total of the RefSeq IDs associated to one OrthoDB ID or more is: '+str(len(d2.keys())))
    
                        conv={}
                        notconv={}
                        counter=0
                        for k,v in d2.items():
                                if len(v)==1:
                                        conv.setdefault(v[0][0],v)
                                elif len(v) > 1:
                                        result=reduce(lambda x, y: x if (x[11] > y[11]) else y, v)
                                        p=all(i[11] == v[0][11] for i in v)
                                        if p == True:
                                                result2= reduce(lambda x,y : x if (x[2]>y[2]) else y, v)
                                                q=all(i[2] == v[0][2] for i in v)
                                                if q == True:
                                                        notconv.setdefault(k,[]).append(v)
                                                else:
                                                        conv.setdefault(result2[0],[result2])
                                                        counter+=1
                                        else:
                                                conv.setdefault(result[0],[result])
                                                counter+=1
                        print('The total of the IDs that are convertable 1 to 1 are: '+str(len(conv)))
                        print('The total of the IDs that are not convertable 1 to 1 are: '+str(len(notconv)))
                        print('The IDs that were associated to more RefSeq IDs and now are assigned to only one are: '+str(counter))

                return conv,notconv


