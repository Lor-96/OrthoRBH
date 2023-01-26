class exaligntab():
    def __init__(self,path):
        self.path=path

    def top1hitexalign(self):
        def floatorint(string):
            if string.isdigit() == True :
                return int(string)
            elif string.isdigit() == False :
                return float(string)

        with open(self.path, 'r') as file:
            for line in range(9):
                print(next(file))
            d={}
            for line in file:
                col=line.split('\t')
                query=col[0].split(' ')[0].strip()
                if not query in d.keys():
                    v=[query,floatorint(col[1].strip()), col[2].strip()] + list(map(floatorint,col[3:]))
                    d.setdefault(v[0],v)
        return d

    def getexalign_header_tab(self):
        with open(self.path,'r') as file:
            header=[next(file) for i in range(9)][8].split('\t')
            header=list(map(lambda x:x.strip('\n'), header))
        print(header)
        return header

    def pltexaligntop1(self,species):
        import pandas as pd
        import matplotlib.pyplot as plt
        from software.library.functions import unique_file 

        sp=self.top1hitexalign()
        colnames=self.getexalign_header_tab()
        df_sp=pd.DataFrame(sp.values(),columns=colnames)
        print('The number of hits in the dataframe is: '+str(len(df_sp)))
        df_sp=df_sp.loc[(df_sp['PVALUE'] < 0.001) & (df_sp['SCORE'] >= 0)]
        print('The number of hits selected is: '+str(len(df_sp)))

        def plot_exonmatch(dataframe,species=str):
            num_bins=30
            file_name=f'exon_match_frequency_{species}.png'
            filename=unique_file(f"{file_name}")
            title=f'Exon match percentage frequency {species}'
            plt.figure()
            plt.hist(dataframe['EX_M%'], num_bins, facecolor='red', alpha=0.5,rwidth=0.8)
            plt.xlabel('EX_M%')
            plt.ylabel('Frequency')
            plt.title(title, loc='center')
            plt.savefig(f"{filename}")

            return None

        def plot_exonscore(dataframe,species=str):
            num_bins=30
            file_name=f'score_match_distribution_{species}.png'
            filename=unique_file(f"{file_name}")
            title=f'Score match distribution {species}'
            plt.figure()
            plt.hist(dataframe['SCORE']/dataframe['QEXN'], num_bins, facecolor='blue', alpha=0.5,rwidth=0.8)
            plt.xlabel('Normalized SCORE')
            plt.ylabel('Frequency')
            plt.title(title, loc='center')
            plt.savefig(f"{filename}")

            return None

        plot_exonmatch(df_sp,species)
        plot_exonscore(df_sp,species)
        return None


    def exaligntop2(self,percentage):
        with open(self.path,'r') as file:
            import pandas as pd
    
            def floatorint(string):
                if string.isdigit() == True :
                    return int(string)
                elif string.isdigit() == False :
                    return float(string)
            lista=[]
            header=[next(file) for line in range(9)][8].split('\t')
            header=list(map(lambda x:x.strip('\n'), header))
            print(header)
            for line in file:
                col=line.split('\t')
                query=col[0].split(' ')[0].strip()
                subject=col[2].split(' ')[0].strip()
                v=[query,floatorint(col[1].strip()), subject] + list(map(floatorint,col[3:]))
                lista.append(v)
        df=pd.DataFrame(lista,columns=header) 
        df=df.loc[(df['PVALUE'] < 0.001) & (df['SCORE'] >= 0)]
        f=iter(df.values.tolist())
        d={}
        for line in f:
            if not line[0].strip() in d.keys():
                d.setdefault(line[0],[line])
                successive=next(f)
                if line[2].strip() == successive[2].strip():
                    while successive[2].strip() == v[2].strip():
                        successive=next(f)
                        if successive[0].strip() != v[0].strip():
                            break
                if successive[0].strip() in d.keys():
                    if not len(d[successive[0].strip()]) >1:
                        d[successive[0].strip()].append(successive)
                elif successive[0].strip() not in d.keys():
                    d.setdefault(successive[0],[successive])
        d1={k:v for k,v in d.items() if v[0][5] >= percentage}
        for k,v in  d1.items():
            if len(v) == 1:
                v.append(((v[0][12])/v[0][1])/(v[0][12]/v[0][1]))
            elif len(v)== 2:
                v.append(((v[0][12]/v[0][1]) - (v[1][12]/v[1][1]))/(v[0][12]/v[0][1]))
        d2={}
        for k,v in d1.items():
            k=v[0][0].strip() + '\t' + v[0][2].strip()
            d2.setdefault(k, v[0:])
        return d2

    def exalignrbh(self,tab2, percentage, threshold):
        from software.library.functions import unique_file
        sp1=self.exaligntop2(percentage)
        sp2=exaligntab(tab2).exaligntop2(percentage)
        file1={}
        for k,v in sp1.items():
            if threshold != 0:    
                if len(v)==3:
                    if v[2]>= threshold:
                        file1.setdefault(k,v)
                if len(v)==2:
                    if v[1]>= threshold:
                        file1.setdefault(k,v)
            elif threshold == 0:
                if len(v)==3:
                    if v[2]> threshold:
                        file1.setdefault(k,v)
                if len(v)==2:
                    if v[1]> threshold:
                        file1.setdefault(k,v)
    
        file2={}
        for k,v in sp2.items():
            if threshold != 0:
                if len(v)==3:
                    if v[2]>= threshold:
                        file2.setdefault(k,v)
                if len(v)== 2:
                    if v[1]>= threshold:
                        file2.setdefault(k,v)
            elif threshold == 0:
                if len(v)==3:
                    if v[2]> threshold:
                        file2.setdefault(k,v)
                if len(v)== 2:
                    if v[1]> threshold:
                        file2.setdefault(k,v)
        brh={}
        for k,v in file1.items():
            stg=k.split('\t')
            x=stg[1] + '\t' + stg[0]
            if x in file2.keys():
                t=file2.get(x)
                st=str(k).split("\t")
                key=st[0].strip()+ '\t' + st[1].strip()
                hashtag='#ID:' + key
                row='>1st:\t' + '\t'.join(map("{}".format,v[0][0:]))
                rep='>Reciprocal 1:\t' + '\t'.join(map("{}".format, t[0][0:]))
                if t[0][5]==v[0][5]:
                    perc='>Percentage:\t' + str(v[0][5])
                    if len(t)==3:
                        rep2='>Reciprocal 2:\t' + '\t'.join(map("{}".format,t[1][0:]))
                        if len(v)==3:
                            row2='>2nd:\t' + '\t'.join(map("{}".format,v[1][0:]))
                            if t[2] == v[2]:
                                ratio='>ScoreRatio:\t' + str(v[2])
                                value='\n'.join([hashtag,row,row2,rep,rep2,perc,ratio])
                                brh.setdefault(key,value)
                            if t[2] != v[2]:
                                MB=max(t[2],v[2])
                                Ratio='>ScoreRatio:\t'+str(MB)
                                value='\n'.join([hashtag,row,row2,rep,rep2,perc,Ratio])
                                brh.setdefault(key,value)
                        if len(v)==2:
                            if t[2] == v[1]:
                                ratio='>ScoreRatio:\t' + str(v[1])
                                value='\n'.join([hashtag,row,rep,rep2,perc,ratio])
                                brh.setdefault(key,value)
                            if t[2] != v[1]:
                                MB=max(t[2],v[1])
                                Ratio='>ScoreRatio:\t'+str(MB)
                                value='\n'.join([hashtag,row,rep,rep2,perc,Ratio])
                                brh.setdefault(key,value)
                    if len(t)==2:
                        if len(v)==3:
                            row2='>2nd:\t' + '\t'.join(map("{}".format,v[1][0:]))
                            if t[1] == v[2]:
                                ratio='>ScoreRatio:\t' + str(v[2])
                                value='\n'.join([hashtag,row,row2,rep,perc,ratio])
                                brh.setdefault(key,value)
                            if t[1] != v[2]:
                                MB=max(t[1],v[2])
                                Ratio='>ScoreRatio:\t'+str(MB)
                                value='\n'.join([hashtag,row,row2,rep,perc,Ratio])
                                brh.setdefault(key,value)
                        if len(v)==2:
                            if t[1] == v[1]:
                                ratio='>ScoreRatio:\t' + str(v[1])
                                value='\n'.join([hashtag,row,rep,perc,ratio])
                                brh.setdefault(key,value)
                            if t[1] != v[1]:
                                MB=max(t[1],v[1])
                                Ratio='>ScoreRatio:\t'+str(MB)
                                value='\n'.join([hashtag,row,rep,perc,Ratio])
                                brh.setdefault(key,value)
                if t[0][5]!=v[0][5]:
                    MP=max(t[0][5],v[0][5])
                    Perc='>Percentage:\t' + str(MP)
                    if len(t)==3:
                        rep2='>Reciprocal 2:\t' + '\t'.join(map("{}".format,t[1][0:]))
                        if len(v)==3:
                            row2='>2nd:\t' + '\t'.join(map("{}".format,v[1][0:]))
                            if t[2] == v[2]:
                                ratio='>ScoreRatio:\t' + str(v[2])
                                value='\n'.join([hashtag,row,row2,rep,rep2,Perc,ratio])
                                brh.setdefault(key,value)
                            if t[2] != v[2]:
                                MB=max(t[2],v[2])
                                Ratio='>ScoreRatio:\t'+str(MB)
                                value='\n'.join([hashtag,row,row2,rep,rep2,Perc,Ratio])
                                brh.setdefault(key,value)
                        if len(v)==2:
                            if t[2] == v[1]:
                                ratio='>ScoreRatio:\t' + str(v[1])
                                value='\n'.join([hashtag,row,rep,rep2,Perc,ratio])
                                brh.setdefault(key,value)
                            if t[2] != v[1]:
                                MB=max(t[2],v[1])
                                Ratio='>ScoreRatio:\t'+str(MB)
                                value='\n'.join([hashtag,row,rep,rep2,Perc,Ratio])
                                brh.setdefault(key,value)
                    if len(t)==2:
                        if len(v)==3:
                            row2='>2nd:\t' + '\t'.join(map("{}".format,v[1][0:]))
                            if t[1] == v[2]:
                                ratio='>ScoreRatio:\t' + str(v[2])
                                value='\n'.join([hashtag,row,row2,rep,Perc,ratio])
                                brh.setdefault(key,value)
                            if t[1] != v[2]:
                                MB=max(t[1],v[2])
                                Ratio='>ScoreRatio:\t'+str(MB)
                                value='\n'.join([hashtag,row,row2,rep,Perc,Ratio])
                                brh.setdefault(key,value)
                        if len(v)==2:
                            if t[1] == v[1]:
                                ratio='>ScoreRatio:\t' + str(v[1])
                                value='\n'.join([hashtag,row,rep,Perc,ratio])
                                brh.setdefault(key,value)
                            if t[1] !=v[1]:
                                MB=max(t[1],v[1])
                                Ratio='>ScoreRatio:\t'+str(MB)
                                value='\n'.join([hashtag,row,rep,Perc,Ratio])
                                brh.setdefault(key,value)

        print("The number of the Best Reciprocal Hit between the 2 species is: "+str(len(brh.keys())))
        
        return brh
    
class exaligndict_rbh(exaligntab):
    def __init__(self,pathordict):
        if type(pathordict)== dict:
            self.name=pathordict.keys()
            self.val=pathordict.values()
            self.elements=pathordict.items()
        if type(pathordict)==str:
            self.path=pathordict
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
            self.name=d.keys()
            self.val=d.values()
            self.elements=d.items()

    def brh_elements(self):
        import pandas as pd
        def floatorint(string):
            if not type(string)==str:
                if type(string)==float:
                    return string
                if type(string)==int:
                    return string
            elif type(string) == str:
                if string.isdigit() == True :
                    return int(string)
                if string.isdigit() == False :
                    return float(string)
        d={}
        for k,v in self.elements:
            lines=v.split('\n')
            for i in lines:
                if i.startswith('#ID:'):
                    key=i.strip('#ID:')
                if i.startswith('>Percentage:'):
                    p=floatorint(i.strip('>Percentage:\t'))
                if i.startswith('>ScoreRatio:'):
                    b=floatorint(i.strip('>ScoreRatio:\t'))
                    d.setdefault(key,[key,p,b])
        colnames=['Hit','Percentage','ScoreRatio']
        df=pd.DataFrame(d.values(),columns=colnames)

        return df