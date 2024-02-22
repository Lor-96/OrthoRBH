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

    def pltexaligntop1(self,species, exonmatchp , scorematch):
        import pandas as pd
        import matplotlib.pyplot as plt
        from software.library.functions import unique_file 

        sp=self.top1hitexalign()
        colnames=self.getexalign_header_tab()
        df_sp=pd.DataFrame(sp.values(),columns=colnames)
        print('The number of hits in the dataframe is: '+str(len(df_sp)))
        df_sp=df_sp.loc[(df_sp['PVALUE'] <= 0.001) & (df_sp['SCORE'] >= 0)]
        print('The number of hits selected is: '+str(len(df_sp)))

        def plot_exonmatch(dataframe,species, exonmatchp = exonmatchp):
            num_bins=50
            file_name=f'exon_match_counts_{species}.png'
            filename=unique_file(f"{file_name}")
            title=f'Exon match percentage counts {species}'
            plt.figure(figsize=(10,10))
            plt.axvline((exonmatchp), color='red', linestyle='dashed', linewidth=1)
            plt.hist(dataframe['EX_M%'], num_bins, facecolor='indigo', alpha=0.5,rwidth=0.8)
            plt.xlabel('EX_M%')
            plt.ylabel('Counts')
            plt.title(title, loc='center')
            plt.savefig(f"{filename}")

            return None

        def plot_exonnormscore(dataframe,species, scorematch = scorematch):
            num_bins=50
            file_name=f'score_match_normalized_distribution_{species}.png'
            filename=unique_file(f"{file_name}")
            title=f'Score match distribution {species}'
            plt.figure(figsize=(10,10))
            plt.hist(dataframe['SCORE']/dataframe['QEXN'], num_bins, facecolor='deepskyblue', alpha=0.5,rwidth=0.8)
            plt.xlabel('Normalized SCORE')
            plt.ylabel('Counts')
            plt.title(title, loc='center')
            plt.savefig(f"{filename}")

            return None

        def plot_exonscore(dataframe,species, scorematch = scorematch):
            num_bins=50
            file_name=f'score_match_distribution_{species}.png'
            filename=unique_file(f"{file_name}")
            title=f'Score match distribution {species}'
            plt.figure(figsize=(10,10))
            plt.axvline((scorematch), color='red', linestyle='dashed', linewidth=1)
            plt.hist(dataframe['SCORE'], num_bins, facecolor='deepskyblue', alpha=0.5,rwidth=0.8)
            plt.xlabel('SCORE')
            plt.ylabel('Counts')
            plt.title(title, loc='center')
            plt.savefig(f"{filename}")

            return None
        
        plot_exonmatch(df_sp,species, exonmatchp=exonmatchp)
        plot_exonnormscore(df_sp,species, scorematch=scorematch)
        plot_exonscore(df_sp,species, scorematch=scorematch)
        
        return None

    def pltexaligntop1nofilt(self, pvalue, score, species):
        import pandas as pd
        import matplotlib.pyplot as plt
        import numpy as np
        from software.library.functions import unique_file, floatorint

        sp=self.top1hitexalign()
        colnames=self.getexalign_header_tab()
        df_sp=pd.DataFrame(sp.values(),columns=colnames)
        lista=list(df_sp['PVALUE'])

        def findminimum(dataframe):
            z=str(min(dataframe['PVALUE']))
            if 'e' in z:
                zl=list(z)
                z1=str(floatorint(z[-1])+1)
                zl[-1]=z1
                zm=''.join(zl)
            if not 'e' in z:
                if '.' in z:
                    zl=list(z)
                    z1=str(floatorint(z[-1])+1)
                    zl[-1]=z1
                    zm=''.join(zl)
            if not '.' in z and not 'e' in z:
                zm=z+'.1'
            return zm
        
        zmin=findminimum(df_sp)
        lista2=[]
        for i in lista:
            if i > 1:
                lista2.append(1)
            elif i == 0 or i == 0.0:
                lista2.append(floatorint(zmin))
            else:
                lista2.append(i)
        lista3=[]
        for i in lista2:
            x=np.log10(i)
            lista3.append(x)
        df_sp['PVALUELOG']=lista3

        lista1=df_sp['SCORE']
        lista4=[]
        for i in lista1:
            if i < 0:
                lista4.append(np.log10(1))
            else:
                lista4.append(np.log10(i))
        df_sp['LOGSCORE']= lista4

        def plot_pval_score(dataframe,pvalue, score , species):
            if score == 0:
                score = 1
            
            file_name=f'Pvalue_distribution_{species}.png'
            filename=unique_file(f"{file_name}")
            title=f'Pvalue distribution {species}'
            plt.figure(figsize=(10,10))
            plt.axvline(np.log10(pvalue)*-1, color='red', linestyle='dashed', linewidth=1)
            plt.hist(dataframe["PVALUELOG"]*-1, bins= 50 , rwidth = 0.8 ,facecolor='limegreen', alpha=0.5)
            plt.title(title,loc='center')
            plt.xlabel("Log10_PVALUE")
            plt.ylabel("Counts")
            plt.savefig(filename)

            file_name1=f'Score_distribution_{species}.png'
            filename1=unique_file(f"{file_name1}")
            title1=f'Score distribution {species}'

            plt.figure(figsize=(10,10))
            plt.axvline(np.log10(score), color='red', linestyle='dashed', linewidth=1)
            plt.hist(dataframe["LOGSCORE"], bins= 50, rwidth = 0.8 ,facecolor='deepskyblue', alpha=0.5)
            plt.title(title1,loc='center')
            plt.xlabel("Log10_Score")
            plt.ylabel("Counts")
            plt.savefig(filename1)
        
        dataframe=plot_pval_score(df_sp,pvalue = pvalue, score = score, species= species )

        return None

    def exaligntop2(self,percentage,pval,score):
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
        df=df.loc[(df['PVALUE'] <= pval) & (df['SCORE'] >= score)]#0.001, 0
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

    def exalignrbh(self,tab2, percentage, threshold,pval,score):
        from software.library.functions import unique_file
        sp1=self.exaligntop2(percentage,pval,score)
        sp2=exaligntab(tab2).exaligntop2(percentage,pval,score)
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
        filename=unique_file('exalign_RBH.txt')
        line=[]
        for v in brh.values():
            line.append(v)
        with open(filename,'w') as text:
            text.write('\n\n'.join(line))
        text.close()

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