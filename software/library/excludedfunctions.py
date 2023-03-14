def getexcluded1(path1,path2,dictionary,percent,threshold): 
    from software.library.functions import unique_file
    import pandas as pd
    import time
    start_time = time.time()

    def floatorint(string):
        if string.isdigit() == True :
            return int(string)
        elif string.isdigit() == False :
            return float(string)
    d1={}
    with open(path1,'r') as file:
        for line in file:
            if not line.startswith('#'):
                columns=line.split('\t')
                if not columns[0].strip() in d1.keys():
                    v=[columns[0].strip(),columns[1].strip()] + list(map(floatorint,columns[2:]))
                    d1.setdefault(v[0],[v])
                    successive=next(file).split('\t')
                    if not successive[0].startswith('#'):
                        if v[1].strip() == successive[1].strip():
                            while successive[1].strip() == v[1].strip():
                                successive=next(file).split('\t')
                                if successive[0].strip().startswith('#'):
                                    break
                    if not successive[0].startswith('#'):
                        if successive[0].strip() in d1.keys():
                            val=[successive[0].strip(),successive[1].strip()]+list(map(floatorint,successive[2:]))
                            d1[val[0]].append(val)
                        elif successive[0].strip() not in d1.keys():
                            val=[successive[0].strip(),successive[1].strip()]+list(map(floatorint,successive[2:]))
                            d1.setdefault(val[0],[val])        

        for k,v in  d1.items():
            if len(v) == 1:
                v.append(v[0][11]/v[0][11])
            elif len(v)== 2:
                v.append((v[0][11] - v[1][11])/v[0][11])
        d_1={}
        for k,v in d1.items():
            k=v[0][0].strip() + '\t' + v[0][1].strip()
            d_1.setdefault(k, v[0:])
    
    d2={}
    with open(path2,'r') as file:
        for line in file:
            if not line.startswith('#'):
                columns=line.split('\t')
                if not columns[0].strip() in d2.keys():
                    v=[columns[0].strip(),columns[1].strip()] + list(map(floatorint,columns[2:]))
                    d2.setdefault(v[0],[v])
                    successive=next(file).split('\t')
                    if not successive[0].startswith('#'):
                        if v[1].strip() == successive[1].strip():
                            while successive[1].strip() == v[1].strip():
                                successive=next(file).split('\t')
                                if successive[0].strip().startswith('#'):
                                    break
                    if not successive[0].startswith('#'):
                        if successive[0].strip() in d2.keys():
                            val=[successive[0].strip(),successive[1].strip()]+list(map(floatorint,successive[2:]))
                            d2[val[0]].append(val)
                        elif successive[0].strip() not in d2.keys():
                            val=[successive[0].strip(),successive[1].strip()]+list(map(floatorint,successive[2:]))
                            d2.setdefault(val[0],[val])        

        for k,v in  d2.items():
            if len(v) == 1:
                v.append(v[0][11]/v[0][11])
            elif len(v)== 2:
                v.append((v[0][11] - v[1][11])/v[0][11])
        d_2={}
        for k,v in d2.items():
            k=v[0][1].strip() + '\t' + v[0][0].strip()
            d_2.setdefault(k, v[0:])
    
    d_p1={}
    for k,v in d_1.items():
        if k in dictionary.keys():
            d_p1.setdefault(k,v)
    d_p2={}
    for k,v in d_2.items():
        if k in dictionary.keys():
            d_p2.setdefault(k,v)

    d_p3={k:v for k,v in d_p1.items()}
    for k,v in d_p2.items():
        if k not in d_p3.keys():
            d_p3.update({k:v})
    
    end_time=time.time()
    print('The total time for the loop is: ' + str(end_time - start_time)+' seconds that in minutes are: '+str((end_time - start_time)/60)+' minutes')

    notintop={}
    excluded_percentage={}
    excluded_bitscore={}
    excluded_both={}
    notreciprocalpassfilt={}
    
    for k,v in d_p3.items():
        if k in dictionary.keys():
            perc=v[0][2]
            if len(v)==2:
                ratio=v[1]
                if perc < percent:
                    if not k in excluded_percentage.keys():
                        excluded_percentage.setdefault(k,[v[0],ratio])
                if perc >= percent:
                    if not k in notreciprocalpassfilt.keys():
                        notreciprocalpassfilt.setdefault(k,[v[0],ratio])
            if len(v)>2:
                ratio=v[2]
                if perc < percent and ratio < threshold:
                    if k not in excluded_both.keys():
                        excluded_both.setdefault(k,[v[0],v[1],ratio])
                if perc < percent and ratio >= threshold:
                    if k not in excluded_percentage.keys():
                        excluded_percentage.setdefault(k,[v[0],v[1],ratio])
                if perc >= percent and ratio < threshold:
                    if k not in excluded_bitscore.keys():
                        excluded_bitscore.setdefault(k,[v[0],v[1],ratio])
                if perc >= percent and ratio >= threshold:
                    if k not in notreciprocalpassfilt.keys():
                        notreciprocalpassfilt.setdefault(k,[v[0],v[1],ratio])

    for k,v in dictionary.items():
        if k not in excluded_percentage.keys():
            if k not in excluded_bitscore.keys():
                if k not in excluded_both.keys(): 
                    if k not in notreciprocalpassfilt.keys():
                        notintop.setdefault(k,v)
    drep1={}
    with open(path1,'r') as file:
        for line in file:
            if not line.startswith('#'):
                columns=line.split('\t')
                key=columns[0].strip()+'\t'+columns[1].strip()
                if key in notintop.keys():
                    if not key in drep1.keys():
                        drep1.setdefault(key,line)

    drep2={}
    with open(path2,'r') as file:
        for line in file:
            if not line.startswith('#'):
                columns=line.split('\t')
                key=columns[1].strip()+'\t'+columns[0].strip()
                if key in notintop.keys():
                    if not key in drep2.keys():
                        drep2.setdefault(key,line) 
        
    for k,v in drep2.items():
        if k not in drep1.keys():
            drep1.update({k:v})
    for k,v in drep1.items():
        if k not in drep2.keys():
            drep2.update({k:v})
    
    miss=[]     
    for i in notintop.keys():
        if i not in drep1.keys():
            miss.append(i)

    if len(excluded_percentage)>0:
        print('The number of the hits that do not pass both the percentage threshold is: '+str(len(excluded_percentage.keys())))
        with open(unique_file('blast_excludedpercentage.txt'),'w') as txt:
            for k,v in excluded_percentage.items():
                if len(v)==2:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=str(v[1])+'\n'
                    fline='\n'.join([line1,line2])
                    txt.write(fline)
                if len(v)==3:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=list(map(str,v[1][0:]))
                    line2='\t'.join(line2)
                    line3=str(v[2])+'\n'
                    fline='\n'.join([line1,line2,line3])
                    txt.write(fline)
        txt.close()

    if len(excluded_bitscore)>0:
        print('The number of the hits that do not pass both the bitscore threshold is: '+str(len(excluded_bitscore.keys())))
        with open(unique_file('blast_excludedbitscore.txt'),'w') as txt:
            for k,v in excluded_bitscore.items():
                if len(v)==2:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=str(v[1])+'\n'
                    fline='\n'.join([line1,line2])
                    txt.write(fline)
                if len(v)==3:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=list(map(str,v[1][0:]))
                    line2='\t'.join(line2)
                    line3=str(v[2])+'\n'
                    fline='\n'.join([line1,line2,line3])
                    txt.write(fline)
        txt.close()

    if len(excluded_both)>0:
        print('The number of the hits that do not pass both the thresholds is: '+str(len(excluded_both.keys())))
        with open(unique_file('blast_excludedboth.txt'),'w') as txt:
            for k,v in excluded_both.items():
                if len(v)==2:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=str(v[1])+'\n'
                    fline='\n'.join([line1,line2])
                    txt.write(fline)
                if len(v)==3:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=list(map(str,v[1][0:]))
                    line2='\t'.join(line2)
                    line3=str(v[2])+'\n'
                    fline='\n'.join([line1,line2,line3])
                    txt.write(fline)
        txt.close()

    if len(notreciprocalpassfilt)>0:
        print('The number of the not reciprocal hits that pass the thresholds is: '+str(len(notreciprocalpassfilt.keys())) )
        with open(unique_file('blast_notreciprocalpassfilt.txt'),'w') as txt:
            for k,v in notreciprocalpassfilt.items():
                if len(v)==2:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=str(v[1])+'\n'
                    fline='\n'.join([line1,line2])
                    txt.write(fline)
                if len(v)==3:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=list(map(str,v[1][0:]))
                    line2='\t'.join(line2)
                    line3=str(v[2])+'\n'
                    fline='\n'.join([line1,line2,line3])
                    txt.write(fline)
        txt.close()

    if len(drep1)>0:
        print('The number of the hits predicted by Exalign but not in top 1 on the BLAST is: '+str(len(drep1.keys())))
        with open(unique_file('blast_notintop.txt'),'w') as txt:
            for k,v in drep1.items():
                txt.write(v)
        txt.close()

    if len(miss)> 0:
        print('The number of the hits predicted by Exalign but not present in the BLAST is: '+str(len(miss)))
        with open(unique_file('blast_missing.txt'),'w') as txt:
            txt.write('\n'.join(miss))
        txt.close()

    return None
    
def getexcluded2(path1,path2,dictionary,percentage,threshold, pvalue, score):
    from software.library.functions import unique_file
    def function1(path,dictionary,percentage,threshold, pvalue =pvalue, score = score,swap=False):    
        with open(path,'r') as file:
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
        df1=df.loc[(df['PVALUE'] <= pvalue) & (df['SCORE'] >= score)]
        f=iter(df1.values.tolist())
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

        for k,v in  d.items():
            if len(v) == 1:
                v.append(((v[0][12])/v[0][1])/(v[0][12]/v[0][1]))
            elif len(v)== 2:
                v.append(((v[0][12]/v[0][1]) - (v[1][12]/v[1][1]))/(v[0][12]/v[0][1]))
            
        if swap == False:
            d1={}
            for k,v in d.items():
                k=v[0][0].strip() + '\t' + v[0][2].strip()
                d1.setdefault(k, v[0:])
            n1=df['QID']
            n2=df['GID']
            n3=pd.concat([n1,n2],axis=1)
            n3=list(iter(n3.values.tolist()))
            n4=[]
            for i in n3:
                n4.append(i[0]+'\t'+i[1])
            n1=list(n1)
            n2=list(n2)
            l=[v for v in dictionary.values()]
            missingboth=[]
            missingscnd=[]
            missingfrst=[]
            exist=[]
            genemisassigned=[]
            gene1=[]
            gene2=[]
            for i in l:
                col=i.split('\t')
                if col[0].strip()+'\t'+col[1].strip() in n4:
                    exist.append(i)
                else:
                    if col[0].strip() in n1:
                        if col[1].strip() in n2:
                            genemisassigned.append(i)
                            gene1.append(col[0].strip())
                            gene2.append(col[1].strip())
                    if col[0].strip() in n1:
                        if col[1].strip() not in n2:
                            missingscnd.append(i)
                    if col[0] not in n1:
                        if col[1] in n2:
                            missingfrst.append(i)
                    if col[0] not in n1:
                        if col[1] not in n2:
                            missingboth.append(i)
        
            dfgenemissigned=df.loc[(df['QID'].isin(gene1) & df['GID'].isin(gene2))]
            pval_score=[]
            for i in exist:
                if i in d1.keys():
                    pval_score.append(i)
            exonmatch=[]
            score=[]
            both=[]
            passfilt=[]
            for k,v in d1.items():
                if k in exist:
                    if k not in pval_score:
                        perc=v[0][5]
                        if len(v)== 2:
                            ratio=v[1]
                            if perc >= percentage:
                                passfilt.setdefault(k,v)
                            if perc < percentage:
                                exonmatch.setdefault(k,v)
                        if len(v) == 3:
                            ratio=v[2]
                            if threshold == 0:
                                if perc < percentage and ratio < threshold:
                                    both.setdefault(k,v)
                                if perc >= percentage and ratio < threshold:
                                    score.setdefault(k,v)
                                if perc < percentage and ratio > threshold:
                                    exonmatch.setdefault(k,v)
                                if perc >= percentage and ratio > threshold:
                                    passfilt.setdefault(k,v)
                            else:
                                if perc < percentage and ratio < threshold:
                                    both.setdefault(k,v)
                                if perc >= percentage and ratio < threshold:
                                    score.setdefault(k,v)
                                if perc < percentage and ratio >= threshold:
                                    exonmatch.setdefault(k,v)
                                if perc >= percentage and ratio >= threshold:
                                    passfilt.setdefault(k,v)
            notintop21=[]
            notintop22=[]
            notintop2=[]
            for i in exist:
                if i not in pval_score:
                    if i not in exonmatch:
                        if i not in score:
                            if i not in both:
                                if i not in passfilt:
                                    col=i.split('\t')
                                    notintop2.append(i)
                                    notintop21.append(col[0].strip())
                                    notintop22.append(col[1].strip())
            dfnottop2=df.loc[(df['QID'].isin(notintop21) & df['GID'].isin(notintop22))]
            return  missingboth, missingscnd,missingfrst,dfgenemissigned,genemisassigned,pval_score,exonmatch,score,both,passfilt,notintop2,dfnottop2

        else:
            d1={}
            for k,v in d.items():
                k=v[0][2].strip() + '\t' + v[0][0].strip()
                d1.setdefault(k, v[0:])
            n1=df['QID']
            n2=df['GID']
            n3=pd.concat([n1,n2],axis=1)
            n3=list(iter(n3.values.tolist()))
            n4=[]
            for i in n3:
                n4.append(i[1]+'\t'+i[0])
            n1=list(n1)
            n2=list(n2)
            l=[v for v in dictionary.values()]
            missingboth=[]
            missingscnd=[]
            missingfrst=[]
            exist=[]
            genemisassigned=[]
            gene1=[]
            gene2=[]
            for i in l:
                col=i.split('\t')
                if col[0].strip()+'\t'+col[1].strip() in n4:
                    exist.append(i)
                else:
                    if col[0].strip() in n2:
                        if col[1].strip() in n1:
                            genemisassigned.append(i)
                            gene2.append(col[0].strip())
                            gene1.append(col[1].strip())
                    if col[0].strip() in n2:
                        if col[1].strip() not in n1:
                            missingscnd.append(i)
                    if col[0] not in n2:
                        if col[1] in n1:
                            missingfrst.append(i)
                    if col[0] not in n2:
                        if col[1] not in n1:
                            missingboth.append(i)
        
            dfgenemissigned=df.loc[(df['QID'].isin(gene1) & df['GID'].isin(gene2))]
            pval_score=[]
            for i in exist:
                if i in d1.keys():
                    pval_score.append(i)
            exonmatch=[]
            score=[]
            both=[]
            passfilt=[]
            for k,v in d1.items():
                if k in exist:
                    if k not in pval_score:
                        perc=v[0][5]
                        if len(v)== 2:
                            ratio=v[1]
                            if perc >= percentage:
                                passfilt.setdefault(k,v)
                            if perc < percentage:
                                exonmatch.setdefault(k,v)
                        if len(v) == 3:
                            ratio=v[2]
                            if threshold == 0:
                                if perc < percentage and ratio < threshold:
                                    both.setdefault(k,v)
                                if perc >= percentage and ratio < threshold:
                                    score.setdefault(k,v)
                                if perc < percentage and ratio > threshold:
                                    exonmatch.setdefault(k,v)
                                if perc >= percentage and ratio > threshold:
                                    passfilt.setdefault(k,v)
                            else:
                                if perc < percentage and ratio < threshold:
                                    both.setdefault(k,v)
                                if perc >= percentage and ratio < threshold:
                                    score.setdefault(k,v)
                                if perc < percentage and ratio >= threshold:
                                    exonmatch.setdefault(k,v)
                                if perc >= percentage and ratio >= threshold:
                                    passfilt.setdefault(k,v)
            notintop21=[]
            notintop22=[]
            notintop2=[]
            for i in exist:
                if i not in pval_score:
                    if i not in exonmatch:
                        if i not in score:
                            if i not in both:
                                if i not in passfilt:
                                    col=i.split('\t')
                                    notintop2.append(i)
                                    notintop22.append(col[0].strip())
                                    notintop21.append(col[1].strip())
            dfnottop2=df.loc[(df['QID'].isin(notintop21) & df['GID'].isin(notintop22))]
            return missingboth, missingscnd,missingfrst,dfgenemissigned,genemisassigned,pval_score,exonmatch,score,both,passfilt,notintop2,dfnottop2

    misboth1,misfrst1,misscnd1,dfmisign1,misign1,pvalscore1,exomtch1,score1,both1,intop2_1,notintop2_1,dfnotop2_1=function1(path1,dictionary,percentage,threshold, pvalue = 0.001, score = 0,swap=False)
    misboth2,misfrst2,misscnd2,dfmisign2,misign2,pvalscore2,exomtch2,score2,both2,intop2_2,notintop2_2,dfnotop2_2=function1(path2,dictionary,percentage,threshold, pvalue = 0.001, score = 0,swap=True)
    
    if len(misboth1) > 0:
        print('The number of the hits that miss both the transcript IDs using species 1 as query is: '+str(len(misboth1)))
        with open(unique_file('exalign_missbothtab1.txt'),'w') as txt:
            txt.write('\n'.join(misboth1))
        txt.close()

    if len(misfrst1)>0:
        print('The number of the hits where miss the first transcript ID using species 1 as query is : '+str(len(misfrst1)))
        with open(unique_file('exalign_missfirstab1.txt'),'w') as txt:
            txt.write('\n'.join(misfrst1))
        txt.close()

    if len(misscnd1) > 0:
        print('The number of the hits where miss the second transcript ID using species 1 as query is : '+str(len(misscnd1)))
        with open(unique_file('exalign_misssecondtab1.txt'),'w') as txt:
            txt.write('\n'.join(misscnd1))
        txt.close()

    if len(misign1) >0:
        print('The number of the transcripts IDs assigned to another transcript ID predicted by the CDS using the species 1 as query is: '+str(len(misign1)))
        dfmisign1.to_csv(unique_file("exalign_misassigned_tab1.tsv"), sep="\t")
        with open(unique_file('exalign_transcripts_notreciprocal_tab1.txt'),'w') as txt:
            txt.write('\n'.join(misign1))
        txt.close()

    if len(pvalscore1)>0:
        print('The number of the hits excluded by the pvalue-score filter using the species 1 as query is: '+str(len(pvalscore1)))
        with open(unique_file('exalign_excluded_pval_scoretab1.txt'),'w') as txt:
            txt.write('\n'.join(pvalscore1))
        txt.close()

    if len(exomtch1)>0:
        print('The number of the hits excluded by the exon match percentage threshold using the species 1 as query is: '+str(len(exomtch1.keys())))
        with open(unique_file('exalign_exonmatch_tab1.txt'),'w') as txt:
            for k,v in exomtch1.items():
                if len(v)==2:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=str(v[1])+'\n'
                    fline='\n'.join([line1,line2])
                    txt.write(fline)
                if len(v)==3:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=list(map(str,v[1][0:]))
                    line2='\t'.join(line2)
                    line3=str(v[2])+'\n'
                    fline='\n'.join([line1,line2,line3])
                    txt.write(fline)
        txt.close()

    if len(score1)>0:
        print('The number of the hits excluded by the score threshold using the species 1 as query is: '+str(len(score1.keys())))
        with open(unique_file('exalign_score_tab1.txt'),'w') as txt:
            for k,v in score1.items():
                if len(v)==2:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=str(v[1])+'\n'
                    fline='\n'.join([line1,line2])
                    txt.write(fline)
                if len(v)==3:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=list(map(str,v[1][0:]))
                    line2='\t'.join(line2)
                    line3=str(v[2])+'\n'
                    fline='\n'.join([line1,line2,line3])
                    txt.write(fline)
        txt.close()

    if len(both1)>0:
        print('The number of the hits excluded by both the thresholds using the species 1 as query is: '+str(len(both1.keys())))
        with open(unique_file('exalign_both_tab1.txt'),'w') as txt:
            for k,v in both1.items():
                if len(v)==2:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=str(v[1])+'\n'
                    fline='\n'.join([line1,line2])
                    txt.write(fline)
                if len(v)==3:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=list(map(str,v[1][0:]))
                    line2='\t'.join(line2)
                    line3=str(v[2])+'\n'
                    fline='\n'.join([line1,line2,line3])
                    txt.write(fline)
        txt.close()

    if len(intop2_1)>0:
        print('The number of the hits not reciprocal in top 1 using the species 1 as query is: '+str(len(intop2_1.keys())))
        with open(unique_file('exalign_notreciprocal_intop1_tab1.txt'),'w') as txt:
            for k,v in intop2_1.items():
                if len(v)==2:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=str(v[1])+'\n'
                    fline='\n'.join([line1,line2])
                    txt.write(fline)
                if len(v)==3:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=list(map(str,v[1][0:]))
                    line2='\t'.join(line2)
                    line3=str(v[2])+'\n'
                    fline='\n'.join([line1,line2,line3])
                    txt.write(fline)
        txt.close()

    if len(notintop2_1)>0:
        print('The number of the transcripts predicted from the CDS not in top 1 in Exalign using the species 1 as query is: '+str(len(notintop2_1)))
        dfnotop2_1.to_csv(unique_file("exalign_notintop2_tab1.tsv"), sep="\t")
        with open(unique_file('exalign_notintop2_tab1.txt'),'w') as txt:
            txt.write('\n'.join(notintop2_1))
        txt.close()

    if len(misboth2)> 0:
        print('The number of the hits that miss both the transcript IDs using species 2 as query is: '+str(len(misboth2)))
        with open(unique_file('exalign_missbothtab2.txt'),'w') as txt:
            txt.write('\n'.join(misboth2))
        txt.close()

    if len(misfrst2)>0:
        print('The number of the hits where miss the first transcript ID using species 2 as query is : '+str(len(misfrst2)))
        with open(unique_file('exalign_missfirstab2.txt'),'w') as txt:
            txt.write('\n'.join(misfrst2))
        txt.close()

    if len(misscnd2)>0:
        print('The number of the hits where miss the second transcript ID using species 2 as query is : '+str(len(misscnd2)))
        with open(unique_file('exalign_misssecondtab2.txt'),'w') as txt:
            txt.write('\n'.join(misscnd2))
        txt.close()

    if len(misign2)>0:
        print('The number of the transcripts IDs assigned to another transcript ID predicted by the CDS using the species 2 as query is: '+str(len(misign2)))
        dfmisign2.to_csv(unique_file("exalign_misassigned_tab2.tsv"), sep="\t")
        with open(unique_file('exalign_gene_notreciprocal_tab2.txt'),'w') as txt:
            txt.write('\n'.join(misign2))
        txt.close()

    if len(pvalscore2)>0:
        print('The number of the hits excluded by the pvalue-score filter using the species 2 as query is: '+str(len(pvalscore2)))
        with open(unique_file('exalign_excluded_pvalscoretab2.txt'),'w') as txt:
            txt.write('\n'.join(pvalscore2))
        txt.close()

    if len(exomtch2)>0:
        print('The number of the hits excluded by the exon match percentage threshold using the species 2 as query is: '+str(len(exomtch2.keys())))
        with open(unique_file('exalign_exonmatch_tab2.txt'),'w') as txt:
            for k,v in exomtch2.items():
                if len(v)==2:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=str(v[1])+'\n'
                    fline='\n'.join([line1,line2])
                    txt.write(fline)
                if len(v)==3:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=list(map(str,v[1][0:]))
                    line2='\t'.join(line2)
                    line3=str(v[2])+'\n'
                    fline='\n'.join([line1,line2,line3])
                    txt.write(fline)
        txt.close()

    if len(score2)>0:
        print('The number of the hits excluded by the score threshold using the species 2 as query is: '+str(len(score2.keys())))
        with open(unique_file('exalign_score_tab2.txt'),'w') as txt:
            for k,v in score2.items():
                if len(v)==2:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=str(v[1])+'\n'
                    fline='\n'.join([line1,line2])
                    txt.write(fline)
                if len(v)==3:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=list(map(str,v[1][0:]))
                    line2='\t'.join(line2)
                    line3=str(v[2])+'\n'
                    fline='\n'.join([line1,line2,line3])
                    txt.write(fline)
        txt.close()

    if len(both2)> 0:
        print('The number of the hits excluded by both the thresholds using the species 2 as query is: '+str(len(both2.keys())))
        with open(unique_file('exalign_both_tab2.txt'),'w') as txt:
            for k,v in both2.items():
                if len(v)==2:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=str(v[1])+'\n'
                    fline='\n'.join([line1,line2])
                    txt.write(fline)
                if len(v)==3:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=list(map(str,v[1][0:]))
                    line2='\t'.join(line2)
                    line3=str(v[2])+'\n'
                    fline='\n'.join([line1,line2,line3])
                    txt.write(fline)
        txt.close()

    if len(intop2_2)>0:
        print('The number of the hits not reciprocal in top 1 using the species 2 as query is: '+str(len(intop2_2.keys())))
        with open(unique_file('exalign_notreciprocal_intop1_tab2.txt'),'w') as txt:
            for k,v in intop2_2.items():
                if len(v)==2:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=str(v[1])+'\n'
                    fline='\n'.join([line1,line2])
                    txt.write(fline)
                if len(v)==3:
                    line1=list(map(str,v[0][0:]))
                    line1='\t'.join(line1)
                    line2=list(map(str,v[1][0:]))
                    line2='\t'.join(line2)
                    line3=str(v[2])+'\n'
                    fline='\n'.join([line1,line2,line3])
                    txt.write(fline)
        txt.close()

    if len(notintop2_2)>0:
        print('The number of the transcripts predicted from the CDS not in top 1 in Exalign using the species 2 as query is: '+str(len(notintop2_2)))
        dfnotop2_2.to_csv(unique_file("exalign_notintop2_tab2.tsv"), sep="\t")
        with open(unique_file('exalign_notintop2_tab2.txt'),'w') as txt:
            txt.write('\n'.join(notintop2_2))
        txt.close()
