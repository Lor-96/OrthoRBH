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

                







                

        
        









