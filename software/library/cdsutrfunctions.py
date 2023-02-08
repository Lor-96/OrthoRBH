def get_cds_coordinates_and_table(gtf_path):
    import os
    import regex as re
    d=[]
    with open(gtf_path,'r') as file:
        for line in file:
            if not line.startswith('#'):
                col=line.split('\t')
                d.append(col)
    
        ann=list(filter(lambda i:i[2] == 'CDS',d))
        del(d)
        data=[]
        rx=re.compile(r'"[^"]*"(*SKIP)(*FAIL)| \s*')
        for i in ann:
            f=i[8].split(';')
            t=[rx.split((j.strip())) for j in f]
            data.append([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],t])
        del(ann)
        protein_transcript_table={}
        coordinates_cds={}
        for i in  data:
            x=list(i[8])
            for j in x:
                if j[0] == 'transcript_id':
                    value = j[1].strip('"')
                if j[0] == 'exon_number':
                    exon=j[0]+': '+j[1].strip('"')
                    coordinates_cds.setdefault(value,[]).append(i[0]+'\t'+i[3].strip()+'\t'+i[4].strip()+'\t'+exon+'\t'+'strand: '+i[6])
                if j[0] == 'protein_id':
                    key = j[1].strip('"')
                    protein_transcript_table.setdefault(key,[])
                    if not value in protein_transcript_table.get(key):
                        protein_transcript_table[key].append(value)
        protein_transcript_table={k:v[0] for k,v in protein_transcript_table.items()} 
        lista=[k+'\t'+v for k,v in protein_transcript_table.items()]
        filename='RefSeq_transcript_to_protein_id_sp'
        i=1
        while os.path.exists(f"{filename}{i}.txt"):
            i += 1
        with open(f"{filename}{i}.txt",'w') as txt:
            txt.write('\n'.join(lista))
        txt.close()

    return coordinates_cds,protein_transcript_table

def readoneisoID(oneiso,table_protein_transcript):
    lista=[]
    with open(oneiso,'r') as file:
        for line in file:
            if line.startswith('>'):
                v=line.split(' ')[0].strip()
                lista.append(v.strip('>'))
    d={}
    for k,v in table_protein_transcript.items():
        if k in lista:
            d.setdefault(k,table_protein_transcript.get(k))
    return d

def get_cds_from_genomic(coordinates_cds,genome,lista_sp):
        minus={}
        plus={}
        for k,v in coordinates_cds.items():
            count=0
            for i in v:
                strand=i.split('\t')[4].strip('strand: ')
                if strand == '+':
                    count += 1
                    chrm=i.split('\t')[0]
                    start=int(i.split('\t')[1])-1
                    stop=int(i.split('\t')[2])
                    last_codon=int(i.split('\t')[2])+3
                    if count==len(v):
                        if chrm in genome.keys():
                            chr_seq=genome.get(chrm)
                            exon=chr_seq[start:last_codon]
                            plus.setdefault(k,[]).append(exon)
                    else:
                        if chrm in genome.keys():
                            chr_seq=genome.get(chrm)
                            exon=chr_seq[start:stop]
                            plus.setdefault(k,[]).append(exon)
                else:
                    count += 1
                    chrm=i.split('\t')[0]
                    start=int(i.split('\t')[1])-1
                    stop=int(i.split('\t')[2])
                    last_codon=int(i.split('\t')[1])-4
                    if count == len(v):
                        if chrm in genome.keys():
                            chr_seq=genome.get(chrm)
                            exon=chr_seq[last_codon:stop]
                            minus.setdefault(k,[]).append(exon[::-1].translate(exon.maketrans('AaTtGgCc','TtAaCcGg')))
                    else:
                        if chrm in genome.keys():
                            chr_seq=genome.get(chrm)
                            exon=chr_seq[start:stop]
                            minus.setdefault(k,[]).append(exon[::-1].translate(exon.maketrans('AaTtGgCc','TtAaCcGg')))
        plus={k:''.join(v) for k,v in plus.items()}
        minus={k:''.join(v) for k,v in minus.items()}
        cds={}
        for k,v in minus.items():
            cds.setdefault(k,v)
        for k,v in plus.items():
            cds.setdefault(k,v)
        def insert_newlines(string, every=80):
            return '\n'.join(string[i:i+every] for i in range(0, len(string), every))

        cds={k:insert_newlines(v.upper()) for k,v in cds.items() if k in lista_sp.values()}

        lista_cds=[]
        for k,v in cds.items():
            lista_cds.append('%s\n%s' % ('>'+k.strip(),v.strip(),))
        print('The number of the CDS is: '+str(len(cds.keys()))+' over '+str(len(lista_sp.values())))

def get_genome(genomic_path, coordinates_cds):
    import gzip
    chrm_list=[]
    for k,v in coordinates_cds.items():
        chrm=v[0].split('\t')[0].strip()
        if not chrm in chrm_list:
            chrm_list.append(chrm)
    if genomic_path.endswith('.gz'):
        with gzip.open(genomic_path,'rt') as file:
            genome={}
            for line in file:
                if line.startswith('>'):
                    if line[1:line.find(' ')].strip('|lcl') in chrm_list:
                        name=line[1:line.find(' ')].strip('|lcl')
                        genome[name]=[]
                else:
                    genome[name].append(line.strip('\n'))
    else:
        with open(genomic_path,'r') as file:
            genome={}
            for line in file:
                if line.startswith('>'):
                    if line[1:line.find(' ')].strip('|lcl') in chrm_list:
                        name=line[1:line.find(' ')].strip('|lcl')
                        genome[name]=[]
                else:
                    genome[name].append(line.strip('\n'))

    genome={k:''.join(v) for k,v in genome.items()}
    
    return genome

def get_exon_coordinates(gtf_path):
    import regex as re
    d=[]
    with open(gtf_path,'r') as file:
        for line in file:
            if not line.startswith('#'):
                col=line.split('\t')
                d.append(col)
    
        ann=list(filter(lambda i:i[2] == 'exon',d))

        del(d)
        data=[]
        rx=re.compile(r'"[^"]*"(*SKIP)(*FAIL)| \s*')
        for i in ann:
            f=i[8].split(';')
            t=[rx.split((j.strip())) for j in f]
            data.append([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],t])
        del(ann)
        exon_coordinates={}
        for i in data:
            x=list(i[8])
            for j in x:
                if j[0] == 'transcript_id':
                    key=j[1].strip('"')
                if j[0] == 'exon_number':
                    exon=j[0]+': '+j[1].strip('"')
                    coordinates=i[0]+'\t'+i[3].strip()+'\t'+i[4].strip()+'\t'+exon+'\t'+'strand: '+i[6]
                    exon_coordinates.setdefault(key,[]).append(coordinates)
    return exon_coordinates

def get_utr_from_genomic(coordinates_cds, exon_coordinates, genome,lista_sp, return_ex=False):
    import os
    plus_utr5={}
    minus_utr5={}
    plus_utr3={}
    minus_utr3={}
    genome=dict(genome)
    for k,v in coordinates_cds.items():
        count_cds = 0
        count_exon = 0
        exonc=exon_coordinates.get(k)
        strand_cds=v[0].split('\t')[4].strip('strand: ')
        strand_exon= exonc[0].split('\t')[4].strip('strand: ')
        start5=None
        end3=None
        start3=None
        end3=None
        #start_exon=None
        chrm_cds=v[0].split('\t')[0]
        chrm_exon= exonc[0].split('\t')[0]
        if strand_cds == strand_exon == '+':
            for i in v:               
                count_cds += 1
                if count_cds == 1:
                    end5 =int(i.split('\t')[1].strip())-1
                    #start_exon=i.split('\t')[3].strip()
                if count_cds == len(v):
                    start3=int(i.split('\t')[2].strip()) +3
            for j in exonc:
                count_exon += 1
                #start_exon1=j.split('\t')[3].strip()
                #if start_exon == start_exon1:
                if count_exon == 1:
                    start5=int(j.split('\t')[1].strip()) -1
                if count_exon == len(exonc):
                    end3=int(j.split('\t')[2])
            if start5 != None and end5 != None and start3 != None and end3 != None:
                #plus_utr5.setdefault(k,[start5,end5])
                #plus_utr3.setdefault(k,[start3,end3])
                if chrm_cds == chrm_exon and chrm_cds in genome.keys():
                    chrm_seq= genome.get(chrm_cds)
                    utr_5=chrm_seq[start5:end5]
                    utr_3=chrm_seq[start3:end3]
                    plus_utr5.setdefault(k,utr_5)
                    plus_utr3.setdefault(k,utr_3)
                    
        elif strand_cds == strand_exon == '-':
            for i in v:
                count_cds += 1
                if count_cds == 1:
                    end5= int(i.split('\t')[2].strip())
                if count_cds == len(v):
                    start3=int(i.split('\t')[1].strip()) -4 
            for j in exonc:
                count_exon += 1
                if count_exon == 1:
                    start5=int(j.split('\t')[2].strip())
                if count_exon == len(exonc):
                    end3= int(j.split('\t')[1].strip()) + 1
            if start5 != None and end5 != None and start3 != None and end3 != None:
                #minus_utr5.setdefault(k,[start5,end5])
                #minus_utr3.setdefault(k,[start3,end3])
                if chrm_cds == chrm_exon and chrm_cds in genome.keys():
                    chrm_seq= genome.get(chrm_cds)
                    utr_5=chrm_seq[end5:start5]
                    utr_3=chrm_seq[end3:start3]
                    minus_utr5.setdefault(k,utr_5[::-1].translate(utr_5.maketrans('AaTtGgCc','TtAaCcGg')))
                    minus_utr3.setdefault(k,utr_3[::-1].translate(utr_3.maketrans('AaTtGgCc','TtAaCcGg')))
    
    def insert_newlines(string, every=80):
        return '\n'.join(string[i:i+every] for i in range(0, len(string), every))
    
    d_utr5={k:insert_newlines(v.upper()) for k,v in plus_utr5.items() if k in lista_sp.values()}
    d_utr5.update({k:insert_newlines(v.upper()) for k,v in minus_utr5.items() if k in lista_sp.values()})
    d_utr3={k:insert_newlines(v.upper()) for k,v in plus_utr3.items() if k in lista_sp.values()}
    d_utr3.update({k:insert_newlines(v.upper()) for k,v in minus_utr3.items() if k in lista_sp.values()})

    lista_utr5=[]
    ex5=[]
    for k,v in d_utr5.items():
        if not v == '':
            lista_utr5.append('%s\n%s' % ('>'+k.strip(),v.strip(),))
        elif v == '':
            print(str(k)+' does not have a sequence so it will not be included in the fasta file')
            ex5.append(k)
    
    lista_utr3=[]
    ex3=[]
    for k,v in d_utr3.items():
        if not v == '':
            lista_utr3.append('%s\n%s' % ('>'+k.strip(),v.strip(),))
        elif v == '':
            print(str(k)+' does not have a sequence so it will not be included in the fasta file')
            ex3.append(k)

    print('The total number of IDs that have a sequence in the UTR5 file is: '+str(len(lista_utr5))+'/'+str(len(d_utr5)))
    print('The total number of IDs that have a sequence in the UTR3 file is: '+str(len(lista_utr3))+'/'+str(len(d_utr3)))
    print('The number of IDs that do not have a sequence in the UTR5 file is: '+str(len(ex5)))
    print('The number of IDs that do not have a sequence in the UTR3 file is: '+str(len(ex3)))

    if return_ex == True:
        filename5='excluded_5UTR_sp'
        filename3='excluded_3UTR_sp'
        i=1
        while os.path.exists(f"{filename5}{i}.txt"):
            i += 1
        with open(f"{filename5}{i}.txt",'w') as txt:
            txt.write('\n'.join(ex5))
        txt.close()

        j=1
        while os.path.exists(f"{filename3}{j}.txt"):
            j += 1
        with open(f"{filename3}{i}.txt",'w') as txt:
            txt.write('\n'.join(ex3))
        txt.close()
        return lista_utr5,lista_utr3
    else:
        return lista_utr5,lista_utr3

def get_cds_exceeded(protein_list,cds_list,tab_sp1,tab_sp2,transcript_protein_sp1,transcript_protein_sp2):
    def get_key(val,dictionary):
        for key, value in dictionary.items():
            if val == value.strip():
                return key

        return "N/A"

    final_list=[]
    for i in cds_list:
        name1=i.split('\t')[0].strip()
        name2=i.split('\t')[1].strip()
        if name1 in transcript_protein_sp1.values():
            id_sp1=get_key(name1,transcript_protein_sp1)
        if name2 in transcript_protein_sp2.values(): 
            id_sp2=get_key(name2,transcript_protein_sp2)
        if id_sp1+'\t'+id_sp2 not in protein_list:
            id_sp1=id_sp1.split('.')[0]
            id_sp2=id_sp2.split('.')[0]
            if id_sp1 != 'N/A' and id_sp2 != 'N/A':
                if id_sp1 in tab_sp1.keys():
                    value1=tab_sp1.get(id_sp1)
                if id_sp2 in tab_sp2.keys():
                    value2=tab_sp2.get(id_sp2)
                if value1 != None and value2!= None:
                    fvalue=value1[0]+'\t'+value1[1]+'\t'+value2[0]+'\t'+value2[1]
                    final_list.append(fvalue)
    return final_list

def get_all_cds_final_list(cds_list,tab_sp1,tab_sp2,transcript_protein_sp1,transcript_protein_sp2,excluded=False):
    def get_key(val,dictionary):
        for key, value in dictionary.items():
            if val == value.strip():
                return key

        return "N/A"
    final_list=[]
    ex1=[]
    ex2=[]
    for i in cds_list:
        name1=i.split('\t')[0].strip()
        name2=i.split('\t')[1].strip()
        if name1 in transcript_protein_sp1.values():
            id_sp1=get_key(name1,transcript_protein_sp1)
            id_sp1=id_sp1.split('.')[0]
        if name2 in transcript_protein_sp2.values(): 
            id_sp2=get_key(name2,transcript_protein_sp2)
            id_sp2=id_sp2.split('.')[0]
        if id_sp1 in tab_sp1.keys():
            value1 = tab_sp1.get(id_sp1)
        elif not id_sp1 in tab_sp1.keys():
            ex1.append(id_sp1)
            value1= None
        if id_sp2 in tab_sp2.keys():
            value2 = tab_sp2.get(id_sp2)
        elif not id_sp2 in tab_sp2.keys():
            ex2.append(id_sp2)
            value2=None
        if value1 != None and value2!= None:
            fvalue=value1[0]+'\t'+value1[1]+'\t'+value2[0]+'\t'+value2[1]
            final_list.append(fvalue)
    print('The unique elements in the final list are: '+str(len(final_list)))
    print('The IDs that are not in the table are: '+str(len(cds_list) - len(final_list)))
    print('The number of the IDs that are not in the table for species 1 are: '+str(len(ex1)))
    print('The number of the IDs that are not in the table for species 2 are: '+str(len(ex2)))

    if excluded == False:
        return final_list
    else:
        with open("excluded_sp1.txt",'w') as txt1, open("excluded_sp2.txt",'w') as txt2:
            txt1.write('\n'.join(ex1))
            txt2.write('\n'.join(ex2))
        txt1.close()
        txt2.close()
        return final_list

def get_common_id_brh(protein_list,cds_list,d_sp1,d_sp2):
    common=[]
    excluded=[]
    count=0
    for i in protein_list:
        id_sp1=d_sp1.get(i.split('\t')[0].strip())
        id_sp2=d_sp2.get(i.split('\t')[1].strip())
        if not id_sp1 == None or not id_sp2 == None:
            couple=id_sp1+'\t'+id_sp2
            if couple in cds_list:
                common.append(couple)
            if couple not in cds_list:
                excluded.append(couple)
        else:
            count +=1
    print(count)
    return common,excluded

