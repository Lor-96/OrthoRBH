
from software.library.blast import Blast
from software.library.gtf_funcitons import get_name_protein_transcript_from_cds_in_gtf
from software.library.rbh import Rbh
from software.library.doubledictionary import doubledictionary_pipeline,doubledictionary_exalign_pipeline
from software.library.functions import unique_file
from software.rbh.exalign_workflow import exalign_pipeline
import pandas as pd
import matplotlib.pyplot as plt
import os

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
    num_bins=30
    color='red'
    file_name=f'percentage_distribution_{species}.png'
    filename=unique_file(f"{file_name}")
    title=f'Percentage Distribution {species}'
    plt.figure()
    plt.hist(dataframe['Percentage'],num_bins, facecolor=color, alpha=0.5,rwidth=0.8)
    plt.xlabel('% ID')
    plt.ylabel('Frequency')
    plt.title(title, loc='center')
    plt.savefig(f"{filename}")

def saveplotbit(dataframe,species=str):
    num_bins=30
    color = 'blue'
    file_name=f'bitscore_distribution_{species}.png'
    filename=unique_file(f"{file_name}")
    title=f'Bitscore Distribution {species}'
    plt.figure()
    plt.hist(dataframe['Bitscore'],num_bins, facecolor=color, alpha=0.5,rwidth=0.8)
    plt.xlabel('Bitscore Ratio')
    plt.ylabel('Frequency')
    plt.title(title, loc='center')
    plt.savefig(f"{filename}")

def rbh_workflow(blast1,blast2,gtfsp1,gtfsp2,percentage,threshold):
    if blast1.endswith('.tsv.tab') and blast2.endswith('.tsv.tab'):
        rbh=exalign_pipeline(blast1,blast2,percentage,threshold)
        rbh_exa=[k.strip('#ID:') for k in Rbh(rbh).name]
        Rbh(rbh).print_rbh()
        dfsp1=get_name_protein_transcript_from_cds_in_gtf(gtfsp1)
        dfsp2=get_name_protein_transcript_from_cds_in_gtf(gtfsp2)
        exa_name_sp1=dict(zip(dfsp1['Transcript'],dfsp1['Gene name']))
        exa_name_sp2=dict(zip(dfsp2['Transcript'],dfsp2['Gene name']))
        rbh_exalign=[i.strip('\n').split('\t') for i in rbh_exa]
        doubledictionary_exalign_pipeline(rbh_exalign,exa_name_sp1,exa_name_sp2)
    else :
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
        pro_name_sp1=dict(zip(dfsp1['Protein'],dfsp1['Gene name']))
        pro_name_sp2=dict(zip(dfsp2['Protein'],dfsp2['Gene name']))
        rbhprotein=[i.strip('\n').split('\t') for i in rbh_p]
        doubledictionary_pipeline(rbhprotein,pro_name_sp1,pro_name_sp2)

    

    

