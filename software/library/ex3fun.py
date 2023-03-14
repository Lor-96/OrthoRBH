def readODBorthotab(path):
    d={}
    with open(path,'r') as file:
        for line in file:
            columns=line.split('\t')
            key='\t'.join(list(map(str.strip,columns[0:2])))
            value=list(map(str.strip,columns[0:]))
            d.setdefault(key,[]).append(value)
    return d

def read_binarytab(path,inv=False):
    d={}
    with open(path,'r') as file:
        for line in file:
            columns=line.split('\t')
            if inv == False:
                d.setdefault(columns[0].strip(),columns[1].strip())
            else:
                d.setdefault(columns[1].strip(),columns[0].strip())
    return d

def odb_refseq_table(d1,d2,dorthodb,dbrh):
    import time
    start_time = time.time()
    def get_key(val,dictionary):
        for key, value in dictionary.items():
             if val == value:
                 return key
        return "N/A"
    
    print('This function return a table with the OrthoDB orthologs associated with the RefSeq IDs obtained with the conversion file from the Blast, the common orthologs between the Best Reciprocal Hit file and OrthoDB and the possible hit that can be in the Blast that are not in the Best Reciprocal Hit file but are in OrthoDB')
    
    d={}
    for k,v in dorthodb.items():
        c1=get_key(v[0][0].strip(),d1).strip()
        c2=get_key(v[0][1].strip(),d2).strip()
        value=c1.strip()+'\t'+c2.strip()
        d.setdefault(k,value)
    end_time=time.time()
    print('The total time for the loop is: ' + str(end_time - start_time)+' seconds that in minutes are: '+str((end_time - start_time)/60)+' minutes')
    print('The number of orthologs by OrthoDB is: '+str(len(d.keys())))
    conv={k:v for k,v in d.items() if not 'N/A' in v}
    print('The number of the convertible Orthodb IDs in the table is: '+str(len(conv)))
    notconv={k:v for k,v in d.items() if 'N/A' in v}
    print('The number of the not convertible IDs in the table is: '+str(len(notconv)))
    
    convbrh={}
    for k,v in dbrh.items():
        value=get_key(k.strip(),d)
        convbrh.setdefault(k,value)
    print('The number of Best Reciprocal Hits is: '+str(len(convbrh)))
    common={k:v for k,v in convbrh.items() if not v == 'N/A'}
    print('The common IDs between the Best Reciprocal Hit file and the OrthoDB orthologs are: '+str(len(common)))
    notcommon={k:v for k,v in convbrh.items() if v == 'N/A'}
    print('The number of the IDs that are not in common between OrthoDB and the Best Reciprocal Hit file is: '+str(len(notcommon)))

    maybeinblast={v:k for k,v in conv.items() if k not in common.values()}
    print('There are '+str(len(maybeinblast))+' IDs that are convertible but not in common with the Best Reciprocal Hit file, so is possible to find all or some of them in the Blast')

    return d,common,notcommon,maybeinblast

def getexcluded(path1,path2,dictionary,percent,threshold):
    import time
    from software.library.functions import unique_file
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

    if len(excluded_percentage)!=0:
        print('The number of hits that do not match the percentage threshold are: '+str(len(excluded_percentage.keys())))
        with open(unique_file('excludedpercentage.txt'),'w') as txt:
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

    if len(excluded_bitscore)!=0:
        print('The number of hits that do not match the bitscore threshold are: '+str(len(excluded_bitscore.keys())))
        with open(unique_file('excludedbitscore.txt'),'w') as txt:
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

    if len(excluded_both)!=0:
        print('The number of hits that do not match both the thresholds are: '+str(len(excluded_both.keys())))
        with open(unique_file('excludedboth.txt'),'w') as txt:
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

    if len(notreciprocalpassfilt)!=0:
        print('The number of hits that match the thresholds but are not reciprocal are: '+str(len(notreciprocalpassfilt.keys())))
        with open(unique_file('notreciprocalpassfilt.txt'),'w') as txt:
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

    if len(drep1)!=0:
        print('The number of hits that are in the BLAST but not in top 1 are: '+str(len(drep1.keys())))
        with open(unique_file('notintop.txt'),'w') as txt:
            for k,v in drep1.items():
                txt.write(v)
        txt.close()

    if len(miss)!= 0:
        print('The number of hits that are missing are: '+str(len(miss)))
        with open(unique_file('missing.txt'),'w') as txt:
            txt.write('\n'.join(miss))
        txt.close()

    all_dict={ **excluded_percentage, **excluded_bitscore, **excluded_both, **notreciprocalpassfilt}
    score={}
    for k,v in all_dict.items():
        name=k
        perc=v[0][2]
        if len(v)==2:
            ratio=v[1]
            score.setdefault(name,[name,perc,ratio])
        if len(v)>2:
            ratio=v[2]
            score.setdefault(name,[name,perc,ratio])
    print('The number of the excluded from the RBH are: '+ str(len(score.keys())))
    return excluded_percentage, excluded_bitscore, excluded_both, notreciprocalpassfilt, notintop, miss, score

def plotbitratio(dictionary):
    def floatorint(string):
        if string.isdigit() == True:
            return int(string)
        elif string.isdigit() == False:
            return float(string)
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

def plotbrh(brh):
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
    
    if type(brh) == str:
        d={0}
        with open(brh,'r') as file:
            for line in file:
                if line.startswith('#'):
                    key=line.strip('#ID:')
                if line.startswith('>Percentage:'):
                    p=floatorint(line.strip('>Percentage:\t'))
                if line.startswith('>BitRatio:'):
                    b=floatorint(line.strip('>BitRatio:\t'))
                    d.setdefault(key,[key,p,b])
            return d
    elif type(brh) == dict:
        d={}
        for k,v in brh.items():
            lines=v.split('\n')
            for i in lines:
                if i.startswith('#ID:'):
                    key=i.strip('#ID:')
                if i.startswith('>Percentage:'):
                    p=floatorint(i.strip('>Percentage:\t'))
                if i.startswith('>BitRatio:'):
                    b=floatorint(i.strip('>BitRatio:\t'))
                    d.setdefault(key,[key,p,b])
        return d
