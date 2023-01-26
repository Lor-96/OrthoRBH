class Rbh:

    def __init__(self,object):
        if type(object) == str:
            self.path=object
        elif type (object) == dict:
            self.name=object.keys()
            self.val=object.values()
            self.elements=object.items()

    def readrbhpath(self):
        d={}
        with open(self.path,'r') as file:
            for line in file:
                if line.startswith('#'):
                    ind=line
                    key=line.strip('#ID:')
                    d.setdefault(key,[ind])
                if line.startswith('>'):
                    d[key].append(line)
        d={k:''.join(v) for k,v in d.items()}

        return d

    def getblastlines(self):
        from software.library.functions import floatorint
        d1={}
        d2={}
        for k,v in self.elements:
            query=None
            hit2=None
            rep2=None
            lines=v.split('\n')
            for line in lines:
                query = k.strip()
                if query != None:    
                    if line.startswith('>1st:\t'):
                        hit1=line.strip('>1st:\t')
                    if line.startswith('>2nd:\t'):
                        hit2=line.strip('>2nd:\t')
                    if line.startswith('>Reciprocal 1:\t'):
                        rep1=line.strip('>Reciprocal 1:\t')
                    if line.startswith('>Reciprocal 2:\t'):
                        rep2=line.strip('>Reciprocal 2:\t')
                        if hit1 != None and rep1 != None:
                            if hit2 != None:
                                if rep2 != None:
                                    val1=[hit1.split('\t'),hit2.split('\t')]
                                    val2=[rep1.split('\t'),rep2.split('\t')]
                                    d1.setdefault(query,val1)
                                    d2.setdefault(query,val2)
                                elif rep2 == None:
                                    val1=[hit1.split('\t'),hit2.split('\t')]
                                    val2=[rep1.split('\t')]
                                    d1.setdefault(query,val1)
                                    d2.setdefault(query,val2)
                            elif hit2 == None:
                                if rep2 != None:
                                    val1=[hit1.split('\t')]
                                    val2=[rep1.split('\t'),rep2.split('\t')]
                                    d1.setdefault(query,val1)
                                    d2.setdefault(query,val2)
                                elif rep2 == None:
                                    val1=[hit1.split('\t')]
                                    val2=[rep1.split('\t')]
                                    d1.setdefault(query,val1)
                                    d2.setdefault(query,val2)
        
        def preparedataframe(dictionary):
            import pandas as pd
            d={}
            for k,v in dictionary.items():
                if len(v) == 2:
                    b1 = floatorint(v[0][11].strip())
                    b2 = floatorint(v[1][11].strip())
                    bt = (b1 - b2)/b1
                    p=floatorint(v[0][2])
                    d.setdefault(k,[p,bt])
                if len(v) == 1:
                    b1 = floatorint(v[0][11].strip())
                    bt = b1/b1
                    p = floatorint(v[0][2])
                    d.setdefault(k,[p,bt])
            df= pd.DataFrame(d.values(),index = d.keys() ,columns= ['Percentage','Bitscore'])
            return df

        df1=preparedataframe(d1)
        df2=preparedataframe(d2)

        return df1,df2

    def print_rbh(self):
        import os
        from software.library.functions import unique_file
        line=[]
        for v in self.val:
            line.append(v)
        filename=unique_file('exalign_RBH.txt')
        with open(filename,'w') as text:
            text.write('\n\n'.join(line))
        text.close()