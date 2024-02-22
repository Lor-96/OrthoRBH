class Biomart:

    def __init__(self,path):
        self.path=path
    

    def biomart_getorthologs(self,predicted,gtf1,gtf2,tav1,tav2,bmpath1,bmpath2,conversion_genenames):

        from software.library.gtf_functions import get_name_protein_transcript_from_cds_in_gtf
        from software.library.functions import unique_file
        
        def getorthologs(path,predicted_id):
            import time
            if predicted_id == False:
                d={}
                d1={}
                ex=[]
                with open(path ,'r') as file:
                    for line in file:
                        col=line.split('\t')
                        if not col[0].strip() =='Gene name':
                            if len(col) == 4:
                                if col[0] or col[1] or col[2] or col[3] == '' or '\n':
                                    col=list(map(lambda x: 'N/A' if x == '' or x=='\n' else x, col))
                                    d.setdefault(col[0],[col[2]])
                                    if not col[2].strip() in d.get(col[0].strip()):
                                        d[col[0]].append(col[2].strip())
                                    name = col[0].strip()+'\t'+col[2].strip()
                                    rs1=col[1].split('.')
                                    rs2=col[3].split('.')
                                    couple=[rs1[0].strip(),rs2[0].strip()]
                                    if not name in d1.keys():
                                        d1.setdefault(name,[]).append(couple)
                                    if name in d1.keys():
                                        if not couple in d1.get(name):
                                            d1[name].append(couple)
                            elif len(col) != 4:
                                ex.append(col)
                if len(ex) >= 1:
                    print('Error the file must be obtained from Biomart Ensembl, it is not composed by 4 element spaced by a tab (columns), so check the integrity of the file in order to make the function work properly')
                    print('There are '+str(len(ex))+' lines in the file that are excluded from the analysis that are reported instead of the final result, to check both set "Ignore = True" and add a another variable name in the script')
            
                df={}
                for k,v in d.items():
                    if len(v) == 1:
                        df.setdefault(k,v[0].strip())
                    if len(v) > 1:
                        count = 0
                        for i in v:
                            if i.strip() == 'N/A':
                                count +=1
                            else:
                                val=i.strip()
                        if count == len(v) - 1:
                            df.setdefault(k,val)
                        else:
                            continue      
                d2={}
                for k,v in d.items():
                    d2.setdefault(v[0],[]).append(k)
                d2={k.strip():v[0].strip()+'\t'+k.strip() for k,v in d2.items() if len(v)==1}
        
                d3={}
                for v in d2.values():
                    d3.setdefault(v,d1.get(v.strip()))
                print('The lines that have a missing value in the Biomart file were replaced by N/A')
                print('The total number of the orthologs in the Biomart file is: '+str(len(d3)))

                return d3 , ex

            if predicted_id == True:
                lista = []
                ex=[]
                import time
                start_time=time.time()
                with open(path,'r') as file:
                    for line in file:
                        if not line.startswith('Gene name'):
                            columns=line.split('\t')
                            if len(columns) == 6:
                                col= list(map(lambda x: 'N/A' if x == '' or x=='\n' else x, columns))
                                if col[0] == 'N/A' and col[1] == 'N/A' and col[2] == 'N/A' and col[3] == 'N/A' and col[4] == 'N/A' and col[5] == 'N/A':
                                    continue
                                else:
                                    k1=col[0].strip()
                                    k2=col[3].strip()
                                    if col[1] == 'N/A':
                                        v1=col[2].split('.')[0].strip()
                                        if col[4] == 'N/A':
                                            v2= col[5].split('.')[0].strip()
                                            value = '\t'.join([k1,v1,k2,v2])
                                            if not value in lista:
                                                lista.append(value)
                                        if col[4] != 'N/A':
                                            v2=col[4].split('.')[0].strip()
                                            value = '\t'.join([k1,v1,k2,v2])
                                            if not value in lista:
                                                lista.append(value)
                                    if col[1] != 'N/A':
                                        v1=col[1].split('.')[0].strip()
                                        if col[4] == 'N/A':
                                            v2= col[5].split('.')[0].strip()
                                            value = '\t'.join([k1,v1,k2,v2])
                                            if not value in lista:
                                                lista.append(value)
                                        if col[4] != 'N/A':
                                            v2= col[4].split('.')[0].strip()
                                            value = '\t'.join([k1,v1,k2,v2])
                                            if not value in lista:
                                                lista.append(value)
                            elif len(columns) != 6:
                                ex.append(columns)
                if len(ex) >= 1:
                    print('Error the file must be obtained from Biomart Ensembl, it is not composed by 4 element spaced by a tab (columns), so check the integrity of the file in order to make the function work properly')
                    print('There are '+str(len(ex))+' lines in the file that are excluded from the analysis that are reported instead of the final result, to check both set "Ignore = True" and add a another variable name in the script')
                end_time=time.time()
                print('The total time for the loop is: ' + str(end_time - start_time)+' seconds that in minutes are: '+str((end_time - start_time)/60)+' minutes')

                d={}
                d1={}
                for line in lista:
                    col=line.split('\t')
                    d.setdefault(col[0],[col[2]])
                    if not col[2].strip() in d.get(col[0].strip()):
                        d[col[0]].append(col[2].strip())
                    name = col[0].strip()+'\t'+col[2].strip()
                    rs1=col[1].split('.')[0].strip()
                    rs2=col[3].split('.')[0].strip()
                    couple=[rs1,rs2]
                    if not name in d1.keys():
                        d1.setdefault(name,[couple])
                    if name in d1.keys():
                        if not couple in d1.get(name):
                            d1[name].append(couple)
            
                df={}
                for k,v in d.items():
                    if len(v) == 1:
                        df.setdefault(k,v[0].strip())
                    if len(v) > 1:
                        count = 0
                        for i in v:
                            if i.strip() == 'N/A':
                                count +=1
                            else:
                                val=i.strip()
                        if count == len(v) - 1:
                            df.setdefault(k,val)
                        else:
                            continue
            
                d2={}
                for k,v in d.items():
                    d2.setdefault(v[0],[]).append(k)
                d2={k.strip():v[0].strip()+'\t'+k.strip() for k,v in d2.items() if len(v)==1}
            
                d3={}
                for v in d2.values():
                    d3.setdefault(v,d1.get(v.strip()))
                print('The lines that have a missing value in the Biomart file were replaced by N/A')
                print('The total number of the orthologs in the Biomart file is: '+str(len(d3)))

                return d3 , ex

        def readt(tab):
            d={}
            with open(tab,'r') as file:
                for line in file:
                    col=line.split('\t')
                    d.setdefault(col[1].split('.')[0].strip(),col[0].strip())
            return d

        def readbtab(btab,predicted_id):
            if predicted_id == False:
                d={}
                with open(btab,'r') as file:
                    for line in file:
                        col=line.split('\t')
                        if not col[0].strip() == 'Gene name':
                            col=list(map(lambda x: 'N/A' if x == '' or x=='\n' else x.strip(), col))
                            pid=col[1].split('.')[0].strip()
                            value=col[0].strip()
                            if pid != 'N/A':
                                if not pid in d.keys():
                                    d.setdefault(pid, []).append(value)
                                if pid in d.keys():
                                    if not value in d.get(pid):
                                        d[pid].append(value)
                   
                df={}
                for k,v in d.items():
                    if len(v) == 1:
                        df.setdefault(k,v[0].strip())
                    if len(v) > 1:
                        count = 0
                        for i in v:
                            if i.strip() == 'N/A':
                                count +=1
                            else:
                                val=i.strip()
                        if count == len(v) - 1:
                            df.setdefault(k,val)
                        else:
                            continue
                return df
        
            else:
                d={}
                with open(btab,'r') as file:
                    for line in file:
                        col=line.split('\t')
                        if not col[0].strip() == 'Gene name':
                            col=list(map(lambda x: 'N/A' if x == '' or x=='\n' else x.strip(), col))
                            pid=col[1].split('\t')[0].strip()
                            ppid=col[2].split('\t')[0].strip()
                            value=col[0].strip()
                            if  pid != 'N/A' and ppid != 'N/A':
                                if not pid in d.keys():
                                    d.setdefault(pid,[]).append(value)
                                if pid in d.keys():
                                    if not value in d.get(pid):
                                        d[pid].append(value)
                                if not ppid in d.keys():
                                    d.setdefault(ppid,[]).append(value)
                                if ppid in d.keys():
                                    if not value in d.get(ppid):
                                        d[ppid].append(value)
                            if pid != 'N/A' and ppid == 'N/A':
                                if not pid in d.keys():
                                    d.setdefault(pid,[]).append(value)
                                if pid in d.keys():
                                    if not value in d.get(pid):
                                        d[pid].append(value)
                            if pid == 'N/A' and ppid != 'N/A':
                                if not ppid in d.keys():
                                    d.setdefault(ppid,[]).append(value)
                                if ppid in d.keys():
                                    if not value in d.get(ppid):
                                        d[ppid].append(value)
                            if pid == 'N/A' and ppid == 'N/A':
                                continue
                df={}
                for k,v in d.items():
                    if len(v) == 1:
                        df.setdefault(k,v[0].strip())
                    if len(v) > 1:
                        count = 0
                        for i in v:
                            if i.strip() == 'N/A':
                                count +=1
                            else:
                                val=i.strip()
                        if count == len(v) - 1:
                            df.setdefault(k,val)
                        else:
                            continue
                return df

        sp1=get_name_protein_transcript_from_cds_in_gtf(gtf1)
        sp2=get_name_protein_transcript_from_cds_in_gtf(gtf2)
        p_sp1=dict(zip(sp1['Protein'],sp1['Gene name']))
        p_sp2=dict(zip(sp2['Protein'],sp2['Gene name']))
        p_sp1={k.split('.')[0].strip():v for k,v in p_sp1.items()}
        p_sp2={k.split('.')[0].strip():v for k,v in p_sp2.items()}
        
        ortho,ex=getorthologs(self.path , predicted)

        table1=readt(tav1)
        table2=readt(tav2)

        biotab1=readbtab(bmpath1,predicted_id=predicted)
        biotab2=readbtab(bmpath2,predicted_id=predicted)

        p1={k:v for k,v in p_sp1.items() if k in biotab1.keys()}
        p2={k:v for k,v in p_sp2.items() if k in biotab2.keys()}

        p_1={}
        for k,v in p1.items():
            p_1.setdefault(v,[]).append(k)

        p_2={}
        for k,v in p2.items():
            p_2.setdefault(v,[]).append(k)

        
        if conversion_genenames == True:
            ortho2={}
            for k,v in ortho.items():
                for i in v:
                    r1=i[0].strip()
                    r2=i[1].strip()
                    n1=p1.get(r1)
                    n2=p2.get(r2)
                    if n1 != None:
                        if n2 != None:
                            ortho2.setdefault(n1+'\t'+n2, []).append(r1+'\t'+n1+'\t'+r2+'\t'+n2)
            lis=[]
            for k,v in ortho2.items():
                for i in v:
                    lis.append(i)
            lis=set(lis)
            d1={}
            for i in lis:
                v1=None
                v2=None
                col=i.split('\t')
                n1=col[1].strip()
                n2=col[3].strip()
                r1=col[0].strip()
                r2=col[2].strip()
                if r1 in table1.keys():
                    v1=r1
                if r2 in table2.keys():
                    v2=r2
                if v1 != None and v2 != None:
                    key=n1+'\t'+n2
                    value=v1+'\t'+n1+'\t'+v2+'\t'+n2
                    if not key in d1.keys():
                        d1.setdefault(key,[]).append(value)
                    if key in d1.keys():
                        if not value in d1.get(key):
                            d1[key].append(value)
            with open(unique_file('biomart.txt'),'w') as file1, open(unique_file('list_Biomart.txt'),'w') as file2:
                file1.write('\n'.join(ortho2.keys()))
                lista=[]
                for k,v in d1.items():
                    for i in v:
                        lista.append(i)
                lista=set(lista)
                file2.write('\n'.join(lista))
            file1.close()
            file2.close()
                            
            return ortho2,d1
        else:
            ortho2={}
            for k,v in ortho.items():
                k1=k.split('\t')[0].strip()
                k2=k.split('\t')[1].strip()
                val1=p_1.get(k1)
                val2=p_2.get(k2)
                if val1 != None and val2 != None:
                    key=k1+'\t'+k2
                    if len(val1) == 1 and len(val2) == 1:
                        r1=val1[0]
                        r2=val2[0]
                        val=r1+'\t'+k1+'\t'+r2+'\t'+k2
                        if not key in ortho2.keys():
                            ortho2.setdefault(key,[]).append(val)
                        if key in ortho2.keys():
                            if not val in ortho2.get(key):
                                ortho2[key].append(val)
                    if len(val1) > 1 and len(val2) == 1:
                        r2=val2[0]
                        for i in val1:
                            r1=i.strip()
                            val=r1+'\t'+k1+'\t'+r2+'\t'+k2
                            if not key in ortho2.keys():
                                ortho2.setdefault(key,[]).append(val)
                            if key in ortho2.keys():
                                if not val in ortho2.get(key):
                                    ortho2[key].append(val)
                    if len(val1) == 1 and len(val2) > 1:
                        r1=val1[0]
                        for j in val2:
                            r2=j.strip()
                            val=r1+'\t'+k1+'\t'+r2+'\t'+k2
                            if not key in ortho2.keys():
                                ortho2.setdefault(key,[]).append(val)
                            if key in ortho2.keys():
                                if not val in ortho2.get(key):
                                    ortho2[key].append(val)
                    if len(val1) > 1 and len(val2) > 1:
                        for i in val1:
                            r1=i
                            for j in val2:
                                r2=j.strip()
                                val=r1+'\t'+k1+'\t'+r2+'\t'+k2
                                if not key in ortho2.keys():
                                    ortho2.setdefault(key,[]).append(val)
                                if key in ortho2.keys():
                                    if not val in ortho2.get(key):
                                        ortho2[key].append(val)
            #ortho2={}
            #for k,v in ortho.items():
            #    k1=k.split('\t')[0].strip()
            #    k2=k.split('\t')[1].strip()
            #    for i in v:
            #        r1=i[0].strip()
            #        r2=i[1].strip()
            #        if r1 in p_sp1.keys():
            #            if r2 in p_sp2.keys():
            #                ortho2.setdefault(k1+'\t'+k2, []).append(r1+'\t'+k1+'\t'+r2+'\t'+k2)
            lis=[]
            for k,v in ortho2.items():
                for i in v:
                    lis.append(i)
            lis=set(lis)
            d1={}
            for i in lis:
                v1=None
                v2=None
                col=i.split('\t')
                n1=col[1].strip()
                n2=col[3].strip()
                r1=col[0].strip()
                r2=col[2].strip()
                if r1 in table1.keys():
                    v1=r1
                if r2 in table2.keys():
                    v2=r2
                if v1 != None and v2 != None:
                    key=n1+'\t'+n2
                    value=v1+'\t'+n1+'\t'+v2+'\t'+n2
                    if not key in d1.keys():
                        d1.setdefault(key,[]).append(value)
                    if key in d1.keys():
                        if not value in d1.get(key):
                            d1[key].append(value)
            with open(unique_file('biomart.txt'),'w') as file1, open(unique_file('list_Biomart.txt'),'w') as file2:
                file1.write('\n'.join(ortho2.keys()))
                lista=[]
                for k,v in d1.items():
                    for i in v:
                        lista.append(i)
                lista=set(lista)
                file2.write('\n'.join(lista))
            file1.close()
            file2.close()
            return ortho2,d1

