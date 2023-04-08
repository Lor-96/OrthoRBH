
from software.library.blast import Blast
from software.library.gtf_functions import get_name_protein_transcript_from_cds_in_gtf,get_name_transcript_from_gtf
from software.library.rbh import Rbh
from software.library.doubledictionary import doubledictionary_pipeline,doubledictionary_exalign_pipeline
from software.library.functions import unique_file, getnoncodingtranscriptexa
from software.rbh.exalign_workflow import exalign_pipeline
import pandas as pd
import matplotlib.pyplot as plt
import os

def previewblast(blast1,blast2, percentage, threshold):
        bl1=Blast(blast1).top2hit(0)
        bl2=Blast(blast2).top2hit(0)
        def plotbitratio(dictionary):
                def floatorint(string):
                        if type(string)==str :
                                if string.isdigit() == True:
                                        return int(string)
                                elif string.isdigit() == False:
                                        return float(string)
                        if type(string) == int:
                                return string
                        if type(string) == float:
                                return string
                lista=[]
                for k,v in dictionary.items():
                        if  len(v)== 3:
                                val=[v[0][0:]+[str(v[2])]]
                                value=[val[0][0:12] + list(map(floatorint, val[0][12:]))]
                                lista.append(value[0])
                        elif len(v)==2:
                                val=[v[0][0:]+[str(v[1])]]
                                value=[val[0][0:12] + list(map(floatorint, val[0][12:]))]
                                lista.append(value[0])
                return lista
        
        sp1=plotbitratio(bl1)
        sp2=plotbitratio(bl2)
        colnames=['Query','Subject','%ID','alignment length','mismatches','gap opens','q.start','q.end','s.start','s.end','evalue','biscore','Bitratio']
        df1=pd.DataFrame(sp1,columns=colnames)
        df2=pd.DataFrame(sp2,columns=colnames)

        def saveplotperc(dataframe,species, percentage):
                color='darkorange'
                file_name=f'preview_percentage_distribution_{species}.png'
                filename=unique_file(f"{file_name}")
                title=f'Preview Percentage Distribution {species}'
                plt.figure(figsize=(10,10))
                plt.axvline((percentage), color='red', linestyle='dashed', linewidth=1)
                plt.hist(dataframe['%ID'],bins = 50, facecolor=color, alpha=0.5,rwidth=0.8)
                plt.xlabel('Identity Percentage')
                plt.ylabel('Counts')
                plt.title(title, loc='center')
                plt.savefig(f"{filename}")

        def saveplotbit(dataframe,species, threshold):
                color = 'royalblue'
                file_name=f'preview_bitscore_distribution_{species}.png'
                filename=unique_file(f"{file_name}")
                title=f'Preview Bitscore Distribution {species}'
                plt.figure(figsize=(10,10))
                plt.axvline((threshold), color='red', linestyle='dashed', linewidth=1)
                plt.hist(dataframe['Bitratio'],bins= 50, facecolor=color, alpha=0.5,rwidth=0.8)
                plt.xlabel('Bitscore Ratio')
                plt.ylabel('Counts')
                plt.title(title, loc='center')
                plt.savefig(f"{filename}")

        saveplotperc(dataframe = df1, species = 'species1', percentage=percentage)
        saveplotperc(dataframe = df2,species= 'species2', percentage = percentage)
        saveplotbit(dataframe = df1, species = 'species1', threshold = threshold)
        saveplotbit(dataframe = df2, species = 'species2', threshold = threshold)
        return None

def bestreciprocal(blast1,blast2,percentage,threshold):
                sp1=Blast(blast1).top2hit(percentage)
                sp2=Blast(blast2).top2hit(percentage)
                
                file1={}
                for k,v in sp1.items():
                        if threshold == 0:
                                if len(v)==3:
                                        if v[2]> threshold:
                                                file1.setdefault(k,v)
                                if len(v)==2:
                                        if v[1]> threshold:
                                                file1.setdefault(k,v)
                        elif threshold != 0:   
                                if len(v)==3:
                                        if v[2]>= threshold:
                                                file1.setdefault(k,v)
                                if len(v)==2:
                                        if v[1]>= threshold:
                                                file1.setdefault(k,v)
                file2={}
                for k,v in sp2.items():
                        if threshold == 0:
                                if len(v)==3:
                                        if v[2]> threshold:
                                                file2.setdefault(k,v)
                                if len(v)== 2:
                                        if v[1]> threshold:
                                                file2.setdefault(k,v)


                        elif threshold != 0:
                                if len(v)==3:
                                        if v[2]>= threshold:
                                                file2.setdefault(k,v)
                                if len(v)== 2:
                                        if v[1]>= threshold:
                                                file2.setdefault(k,v)
                brh={}
                for k,v in file1.items():
                        stg=k.split('\t')
                        x=stg[1] + '\t' + stg[0]
                        if x in file2.keys():
                                t=file2.get(x)
                                st=str(k).split("\t")
                                key=st[0].strip()+ '\t' + st[1].strip()
                                hashtag='#ID:' + st[0] + '\t' + st[1]
                                row='>1st:\t' + '\t'.join(map("{}".format,v[0][0:]))
                                rep='>Reciprocal 1:\t' + '\t'.join(map("{}".format, t[0][0:]))
                                if t[0][2]==v[0][2]:
                                        perc='>Percentage:\t' + str(v[0][2])
                                        if len(t)==3:
                                                rep2='>Reciprocal 2:\t' + '\t'.join(map("{}".format,t[1][0:]))
                                                if len(v)==3:
                                                        row2='>2nd:\t' + '\t'.join(map("{}".format,v[1][0:]))
                                                        if t[2] == v[2]:
                                                                ratio='>BitRatio:\t' + str(v[2])
                                                                value='\n'.join([hashtag,row,row2,rep,rep2,perc,ratio])
                                                                brh.setdefault(key,value)
                                                        if t[2] != v[2]:
                                                                MB=max(t[2],v[2])
                                                                Ratio='>BitRatio:\t'+str(MB)
                                                                value='\n'.join([hashtag,row,row2,rep,rep2,perc,Ratio])
                                                                brh.setdefault(key,value)
                                                if len(v)==2:
                                                        if t[2] == v[1]:
                                                                ratio='>BitRatio:\t' + str(v[1])
                                                                value='\n'.join([hashtag,row,rep,rep2,perc,ratio])
                                                                brh.setdefault(key,value)
                                                        if t[2] != v[1]:
                                                                MB=max(t[2],v[1])
                                                                Ratio='>BitRatio:\t'+str(MB)
                                                                value='\n'.join([hashtag,row,rep,rep2,perc,Ratio])
                                                                brh.setdefault(key,value)
                                        if len(t)==2:
                                                if len(v)==3:
                                                        row2='>2nd:\t' + '\t'.join(map("{}".format,v[1][0:]))
                                                        if t[1] == v[2]:
                                                                ratio='>BitRatio:\t' + str(v[2])
                                                                value='\n'.join([hashtag,row,row2,rep,perc,ratio])
                                                                brh.setdefault(key,value)
                                                        if t[1] != v[2]:
                                                                MB=max(t[1],v[2])
                                                                Ratio='>BitRatio:\t'+str(MB)
                                                                value='\n'.join([hashtag,row,row2,rep,perc,Ratio])
                                                                brh.setdefault(key,value)
                                                if len(v)==2:
                                                        if t[1] == v[1]:
                                                                ratio='>BitRatio:\t' + str(v[1])
                                                                value='\n'.join([hashtag,row,rep,perc,ratio])
                                                                brh.setdefault(key,value)
                                                        if t[1] != v[1]:
                                                                MB=max(t[1],v[1])
                                                                Ratio='>BitRatio:\t'+str(MB)
                                                                value='\n'.join([hashtag,row,rep,perc,Ratio])
                                                                brh.setdefault(key,value)
                                if t[0][2]!=v[0][2]:
                                        MP=max(t[0][2],v[0][2])
                                        Perc='>Percentage:\t' + str(MP)
                                        if len(t)==3:
                                                rep2='>Reciprocal 2:\t' + '\t'.join(map("{}".format,t[1][0:]))
                                                if len(v)==3:
                                                        row2='>2nd:\t' + '\t'.join(map("{}".format,v[1][0:]))
                                                        if t[2] == v[2]:
                                                                ratio='>BitRatio:\t' + str(v[2])
                                                                value='\n'.join([hashtag,row,row2,rep,rep2,Perc,ratio])
                                                                brh.setdefault(key,value)
                                                        if t[2] != v[2]:
                                                                MB=max(t[2],v[2])
                                                                Ratio='>BitRatio:\t'+str(MB)
                                                                value='\n'.join([hashtag,row,row2,rep,rep2,Perc,Ratio])
                                                                brh.setdefault(key,value)
                                                if len(v)==2:
                                                        if t[2] == v[1]:
                                                                ratio='>BitRatio:\t' + str(v[1])
                                                                value='\n'.join([hashtag,row,rep,rep2,Perc,ratio])
                                                                brh.setdefault(key,value)
                                                        if t[2] != v[1]:
                                                                MB=max(t[2],v[1])
                                                                Ratio='>BitRatio:\t'+str(MB)
                                                                value='\n'.join([hashtag,row,rep,rep2,Perc,Ratio])
                                                                brh.setdefault(key,value)
                                        if len(t)==2:
                                                if len(v)==3:
                                                        row2='>2nd:\t' + '\t'.join(map("{}".format,v[1][0:]))
                                                        if t[1] == v[2]:
                                                                ratio='>BitRatio:\t' + str(v[2])
                                                                value='\n'.join([hashtag,row,row2,rep,Perc,ratio])
                                                                brh.setdefault(key,value)
                                                        if t[1] != v[2]:
                                                                MB=max(t[1],v[2])
                                                                Ratio='>BitRatio:\t'+str(MB)
                                                                value='\n'.join([hashtag,row,row2,rep,Perc,Ratio])
                                                                brh.setdefault(key,value)
                                                if len(v)==2:
                                                        if t[1] == v[1]:
                                                                ratio='>BitRatio:\t' + str(v[1])
                                                                value='\n'.join([hashtag,row,rep,Perc,ratio])
                                                                brh.setdefault(key,value)
                                                        if t[1] !=v[1]:
                                                                MB=max(t[1],v[1])
                                                                Ratio='>BitRatio:\t'+str(MB)
                                                                value='\n'.join([hashtag,row,rep,Perc,Ratio])
                                                                brh.setdefault(key,value)
                
                print("The number of the Best Reciprocal Hit between the 2 species is: "+str(len(brh.keys())))

                return brh

def saveplotperc(dataframe,species= str):
    num_bins=50
    color='darkorange'
    file_name=f'percentage_distribution_{species}.png'
    filename=unique_file(f"{file_name}")
    title=f'Percentage Distribution {species}'
    plt.figure(figsize=(10,10))
    plt.hist(dataframe['Percentage'],num_bins, facecolor=color, alpha=0.5,rwidth=0.8)
    plt.xlabel('Identity Percentage')
    plt.ylabel('Counts')
    plt.title(title, loc='center')
    plt.savefig(f"{filename}")

def saveplotbit(dataframe,species=str):
    num_bins=50
    color = 'royalblue'
    file_name=f'bitscore_distribution_{species}.png'
    filename=unique_file(f"{file_name}")
    title=f'Bitscore Distribution {species}'
    plt.figure(figsize=(10,10))
    plt.hist(dataframe['Bitscore'],num_bins, facecolor=color, alpha=0.5,rwidth=0.8)
    plt.xlabel('Bitscore Ratio')
    plt.ylabel('Counts')
    plt.title(title, loc='center')
    plt.savefig(f"{filename}")

def rbh_workflow(blast1,blast2,gtfsp1,gtfsp2,percentage,threshold,pval,score,transcript):
    if blast1.endswith('.tsv.tab') and blast2.endswith('.tsv.tab'):
        rbh=exalign_pipeline(blast1,blast2,percentage,threshold,pval,score)
        rbh_exa=[k.strip('#ID:') for k in Rbh(rbh).name]
        with open(unique_file('transcript_exalign_RBH.txt'),'w') as txt:
                txt.write('\n'.join(rbh_exa))
        txt.close()
        dfsp1=get_name_protein_transcript_from_cds_in_gtf(gtfsp1)
        dfsp2=get_name_protein_transcript_from_cds_in_gtf(gtfsp2)
        tgsp1=get_name_transcript_from_gtf(gtfsp1)
        tgsp2=get_name_transcript_from_gtf(gtfsp2)
        exa_name_sp1=dict(zip(dfsp1['Transcript'],dfsp1['Gene name']))
        exa_name_sp2=dict(zip(dfsp2['Transcript'],dfsp2['Gene name']))
        exa_tg_sp1=dict(zip(tgsp1['Transcript'],tgsp1['Gene name']))
        exa_tg_sp2=dict(zip(tgsp2['Transcript'],tgsp2['Gene name']))
        rbh_exalign=[i.strip('\n').split('\t') for i in rbh_exa]
        getnoncodingtranscriptexa(rbh_exalign = rbh_exalign, dict1 =exa_tg_sp1 , dict2= exa_tg_sp2)
        doubledictionary_exalign_pipeline(rbh_exalign,exa_name_sp1,exa_name_sp2)
    else :
        previewblast(blast1,blast2, percentage, threshold)
        rbh=bestreciprocal(blast1,blast2,percentage,threshold)
        sp1,sp2=Rbh(rbh).getblastlines()
        saveplotperc(sp1,'species1')
        saveplotperc(sp2,'species2')
        saveplotbit(sp1,'species1')
        saveplotbit(sp2,'species2')
        rbh_p=[k.strip('#ID:') for k in Rbh(rbh).name]
        Rbh(rbh).print_rbh()
        dfsp1=get_name_protein_transcript_from_cds_in_gtf(gtfsp1)
        dfsp2=get_name_protein_transcript_from_cds_in_gtf(gtfsp2)
        rbh_pro_tr=[i.strip('\n').split('\t') for i in rbh_p]
        if transcript == False:
                pro_name_sp1=dict(zip(dfsp1['Protein'],dfsp1['Gene name']))
                pro_name_sp2=dict(zip(dfsp2['Protein'],dfsp2['Gene name']))
                doubledictionary_pipeline(rbh_pro_tr,pro_name_sp1,pro_name_sp2)
        if transcript == True:
                trnscr_name_sp1=dict(zip(dfsp1['Transcript'],dfsp1['Gene name']))
                trnscr_name_sp2=dict(zip(dfsp2['Transcript'],dfsp2['Gene name']))
                doubledictionary_pipeline(rbh_pro_tr,trnscr_name_sp1,trnscr_name_sp2)

