def extra_n10_pipeline(rbh,mgi,odb,biomart,exalign,gtf1,gtf2):
    import itertools
    import pandas as pd
    from software.library.functions import unique_file
    from software.library.gtf_functions import get_name_transcript_nexon_from_gtf
    from functools import reduce
    import numpy as np
    import seaborn as sb
    import matplotlib.pyplot as plt
    def readlistortho(path):
        lista=[]
        with open(path,'r') as file:
            for line in file:
                lista.append(line.strip())
        return lista

    rbh=readlistortho(rbh)
    mgi=readlistortho(mgi)
    odb=readlistortho(odb)
    biomart=readlistortho(biomart)
    exalign=readlistortho(exalign)
    brh=set(brh)
    mgi=set(mgi)
    odb=set(odb)
    biomart=set(biomart)
    sets={1:brh,2:mgi,3:odb,4:biomart}
    intersections = {}
    for n_combinations in range(1, len(sets) + 1):
        tmp = list(map(dict, itertools.combinations(sets.items(), n_combinations)))
        tmp = {tuple(x.keys()):set.intersection(*list(x.values())) for x in tmp}
        intersections.update(tmp)

    unique_in_intersection = {}
    for n_combinations in range(1, len(sets)+1):
        for lookup_set in itertools.combinations(range(1, len(sets)+1), n_combinations):
            s1_intersection_s2 = intersections[lookup_set]
            union_other_intersections = set.union(*[v if k != lookup_set and len(k) > len(lookup_set) else {'N/A'} for k, v in intersections.items()])
            unique_in_intersection[lookup_set] = s1_intersection_s2 - union_other_intersections

    lista=[]
    for k,v in unique_in_intersection.items():
        for i in v:
            if i not in lista:
                lista.append(i)

    dflist=[]
    for i in lista:
        gene1=i.split('\t')[0].strip()
        gene2=i.split('\t')[1].strip()
        val=gene1+'\t'+gene2
        if val in unique_in_intersection[(1,)]:
            dflist.append([gene1,gene2,1,1,0,0,0])
        if val in unique_in_intersection[(2,)]:
            dflist.append([gene1,gene2,1,0,1,0,0])
        if val in unique_in_intersection[(3,)]:
            dflist.append([gene1,gene2,1,0,0,1,0])
        if val in unique_in_intersection[(4,)]:
            dflist.append([gene1,gene2,1,0,0,0,1])
        if val in unique_in_intersection[(1, 2)]:
            dflist.append([gene1,gene2,2,1,1,0,0])
        if val in unique_in_intersection[(1, 3)]:
            dflist.append([gene1,gene2,2,1,0,1,0])
        if val in unique_in_intersection[(1, 4)]:
            dflist.append([gene1,gene2,2,1,0,0,1])
        if val in unique_in_intersection[(2, 3)]:
            dflist.append([gene1,gene2,2,0,1,1,0])
        if val in unique_in_intersection[(2, 4)]:
            dflist.append([gene1,gene2,2,0,1,0,1])
        if val in unique_in_intersection[(3, 4)]:
            dflist.append([gene1,gene2,2,0,0,1,1])
        if val in unique_in_intersection[(1, 2, 3)]:
            dflist.append([gene1,gene2,3,1,1,1,0])
        if val in unique_in_intersection[(1, 2, 4)]:
            dflist.append([gene1,gene2,3,1,1,0,1])
        if val in unique_in_intersection[(1, 3, 4)]:
            dflist.append([gene1,gene2,3,1,0,1,1])
        if val in unique_in_intersection[(2, 3, 4)]:
            dflist.append([gene1,gene2,3,0,1,1,1])
        if val in unique_in_intersection[(1, 2, 3, 4)]:
            dflist.append([gene1,gene2,4,1,1,1,1])
        
    header=['Gene1','Gene2','N°Methods','RBH','MGI','ODB','Biomart']
    df=pd.DataFrame(dflist,columns=header)
    dfgtf_sp1=get_name_transcript_nexon_from_gtf(gtf1)
    dfgtf_sp2=get_name_transcript_nexon_from_gtf(gtf2)

    d1={}
    for k,v in dfgtf_sp1.items():
        if k in list(df['Gene1']):
            if len(v)>1:
                result=reduce(lambda x, y: x if (x[1] > y[1]) else y, list(v.items()))
                d1.setdefault(k,{}).setdefault(result[0],result[1])
            else:
                for i,j in v.items():
                    d1.setdefault(k,{}).setdefault(i,j)
    d2={}
    for k,v in dfgtf_sp2.items():
        if k.strip() in list(df['Gene2']):
            if len(v)>1:
                result=reduce(lambda x, y: x if (x[1] > y[1]) else y, list(v.items()))
                d2.setdefault(k,{}).setdefault(result[0],result[1])
            else:
                for i,j in v.items():
                    d2.setdefault(k,{}).setdefault(i,j)

    dfgtf1={ 'Gene' : [], 'Transcript' : [], 'Exon number' : [] }
    for k,v in d1.items():
        for i,j in v.items():
            dfgtf1['Gene'].append(k)
            dfgtf1['Transcript'].append(i)
            dfgtf1['Exon number'].append(j)
    dfgtf1 = pd.DataFrame.from_dict( dfgtf1, orient="columns" )

    dfgtf2={ 'Gene' : [], 'Transcript' : [], 'Exon number' : [] }
    for k,v in d2.items():
        for i,j in v.items():
            dfgtf2['Gene'].append(k)
            dfgtf2['Transcript'].append(i)
            dfgtf2['Exon number'].append(j)
    dfgtf2 = pd.DataFrame.from_dict( dfgtf2, orient="columns" )

    dsp1={}
    for index1 , row1 in dfgtf1.iterrows():
        dsp1.setdefault(row1['Gene'],row1['Exon number'])
    dsp2={}
    for index2, row2 in dfgtf2.iterrows():
        dsp2.setdefault(row2['Gene'], row2['Exon number'])
    lexalign=[]
    lnexon=[]
    for index, row in df.iterrows():
        if row['Gene1']+'\t'+row['Gene2'] in exalign:
            exon1=dsp1.get(row['Gene1'].strip())
            exon2=dsp2.get(row['Gene2'].strip())
            if exon1 != None and exon2 != None:
                if exon2 > exon1:
                    lexalign.append(True)
                    lnexon.append(exon2)
                else:
                    lexalign.append(True)
                    lnexon.append(exon1)
        else:
            if row['Gene1'] in dsp1.keys() and  row['Gene2'] in dsp2.keys():
                exon1=dsp1.get(row['Gene1'].strip())
                exon2=dsp2.get(row['Gene2'].strip())
                if exon2 > exon1:
                    lexalign.append(False)
                    lnexon.append(exon2)
                else:
                    lexalign.append(False)
                    lnexon.append(exon1)
            if row['Gene1'] not in dsp1.keys() and row['Gene2'] in dsp2.keys():
                lexalign.append(False)
                exon2=dsp2.get(row['Gene2'].strip())
                lnexon.append(exon2)
            if row['Gene1'] in dsp1.keys() and not row['Gene2'] in dsp2.keys():
                lexalign.append(False)
                exon1=dsp1.get(row['Gene1'].strip())
                lnexon.append(exon1)
            if row['Gene1'] not in dsp1.keys() and not row['Gene2'] in dsp2.keys():
                lexalign.append(False)
                lnexon.append('N/A')
    df['Exalign']=lexalign
    df['Exon number']=lnexon

    df2=df.loc[(df['N°Methods']>=2)&(df['Exalign']== True)]
    df2=df2.sort_values(['Exon number'],ascending=False)
    df3=df.loc[(df['Exalign']== False)&(df['Exon number']!= 'N/A')&(df['N°Methods']>=2)]
    df3=df3.sort_values(['Exon number'],ascending=False)
    data1=df2['Exon number']
    data2 = df3['Exon number']
    
    filename=unique_file('Exalign_densityplot.png')
    plt.figure(figsize = (10,10))
    sb.kdeplot(data1, fill = True, clip=(0,30) , bw_adjust= 1,color='teal')
    sb.kdeplot(data2, fill = True, clip=(0,30) , bw_adjust= 1,color='orange')
    plt.xlabel('Number of Exon per Gene')
    plt.legend(['Exalign Orthologs', 'Exalign Orthologs not found'])
    plt.savefig(f"{filename}")
