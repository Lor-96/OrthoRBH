def extra_n6_pipeline(mgihomologs,tab1,tab2):
    from software.library.functions import unique_file
    with open(mgihomologs,'r') as file:
        colnames=[next(file).split('\t') for x in range(1)][0]
        lista=[]
        d={}
        for line in file:
            columns= line.split('\t')
            lista.append(columns)
            value=[columns[2],columns[3],columns[11]]
            d.setdefault(columns[0],[]).append(value)

    d1={k:v for k,v in d.items() if len(v)==2}        
    dex={k:v for k,v in d.items() if len(v)>2}

    l={}
    dc1={}
    dc2={}
    for k,v in d1.items():
        if v[0][0] == '10090':
            mouse=v[0]
            if v[1][0]=='9606':
                human=v[1]
                l.setdefault(mouse[1],[]).append(human[1])
                dc1.setdefault(human[1],[]).append(human[2])
                dc2.setdefault(mouse[1],[]).append(mouse[2])
        
    l1={}
    for k,v in l.items():
        l1.setdefault(v[0],[]).append(k)

    li={k:v for k,v in l1.items() if len(v)==1}

    with open(tab1,'r') as file:
        tabsp1=[]
        for line in file:
            col=line.split('\t')
            col=list(map(lambda x:x.strip(),col[0:]))
            tabsp1.append([col[0].strip(), col[1].split('.')[0].strip()])
    dtabsp1={i[1].strip():i[0].strip() for i in tabsp1}

    with open(tab2,'r') as file:
        tabsp2=[]
        for line in file:
            col=line.split('\t')
            col=list(map(lambda x:x.strip(),col[0:]))
            tabsp2.append([col[0].strip(), col[1].split('.')[0].strip()])
    dtabsp2={i[1].strip():i[0].strip() for i in tabsp2}


    flist=[]
    names=[]
    for k,v in li.items():
        n1=dc1.get(k.strip())[0].split(',')
        n2=dc2.get(v[0].strip())[0].split(',')
        for i in n1:
            if i in dtabsp1.keys():
                r1=i
                for j in n2:
                    if j in dtabsp2.keys():
                        r2=j
                        flist.append(i+'\t'+k.strip()+'\t'+j+'\t'+v[0].strip())
                        names.append(k.strip()+'\t'+v[0].strip())

    flistx=set(flist)
    namesx=set(names)

    with open(unique_file('MGI_DB_final_list.txt'),'w') as file,open(unique_file('mgi.txt'),'w') as txt:
        file.write('\n'.join(flistx))
        txt.write('\n'.join(namesx))
    file.close()
    txt.close()
    return None