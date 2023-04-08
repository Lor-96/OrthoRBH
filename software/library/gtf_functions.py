
def get_name_protein_transcript_from_cds_in_gtf(gtf_path):
    import regex as re
    import pandas as pd
    import gzip
    if gtf_path.endswith('.gz'):
        d=[]
        with gzip.open(gtf_path,'rb') as fh:
            for line in fh:
                line =line.decode('utf-8')
                if not line.startswith('#'):
                    col=line.split('\t')
                    d.append(col)
    else:
        d=[]
        with open(gtf_path,'r') as fh:
            for line in fh:
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
    for i in  data:
        x=list(i[8])
        for j in x:
            if j[0] == 'gene_id':
                name = j[1].strip('"')
            if j[0] == 'transcript_id':
                transcript = j[1].strip('"')
            if j[0] == 'protein_id':
                protein = j[1].strip('"')
                value=[name+'\t'+transcript]
                protein_transcript_table.setdefault(protein,[])
                if not value in protein_transcript_table.get(protein):
                    protein_transcript_table[protein].append(value)
    protein_transcript_table={k:v[0] for k,v in protein_transcript_table.items()}
    del(data)
    lista=[]
    for k,v in protein_transcript_table.items():
        protein=k
        name=v[0].split('\t')[0].strip()
        transcript=v[0].split('\t')[1].strip()
        value = [name, protein, transcript]
        lista.append(value)
    df=pd.DataFrame(lista, columns=['Gene name', 'Protein', 'Transcript'])

    return df

def genebiotype(gtf_file_path,filename):
    from software.library.functions import unique_file
    with open(gtf_file_path,'r') as data:
        counts={}
        lines=[]
        for line in data:
            if not line.startswith('#'):
                l=line.split('\t')
                lines.append(l)
        annotation=list(filter(lambda i:i[2] == 'gene', lines))
        ann_list= [i[8].split(';') for i in annotation]
        data_ann=[[i.split() for i in lista] for lista in ann_list]
        data_ann2=[]
        for lista in data_ann:
            for i in lista:
                if not len(i)==0:
                    data_ann2.append(i)

        data_filt= list(filter(lambda i:i[0]=='gene_biotype', data_ann2))
        value= [i[1] for i in data_filt]
        for item in value:
            if item in counts:
                counts[item] += 1
            else:
                counts[item] = 1
        for k,v in counts.items():
            print(k+':'+str(v))
    
    name=unique_file(filename)
    
    with open(name,'w') as txt:
        for key in counts:
            line=':'.join((key,str(counts[key])))
            txt.write(line+'\n')
    txt.close()

    return None

def get_name_transcript_nexon_from_gtf(gtf_path):
    import regex as re
    import pandas as pd
    import gzip
    rx=re.compile(r'"[^"]*"(*SKIP)(*FAIL)| \s*')
    d={}
    with open(gtf_path,'r') as fh:
        for line in fh:
            if not line.startswith('#'):
                col=line.split('\t')
                if  col[2]== 'exon':
                    t=[rx.split((j.strip())) for j in col[8].split(';')]
                    dt={i[0].strip():i[1].strip() for i in t if len(i)>1}
                    gene=dt.get('gene_id').strip('"')
                    transcript=dt.get('transcript_id').strip('"')
                    exonnumber=dt.get('exon_number').strip('"')
                    if gene not in d.keys():
                        d.setdefault(gene,{}).setdefault(transcript,[]).append(exonnumber)
                    elif gene in d.keys():
                        d[gene].setdefault(transcript,[]).append(exonnumber)
    d1={}
    for k,v in d.items():
        for i,j in v.items():
            d1.setdefault(k,{}).setdefault(i,len(j))

    return d1

def get_name_transcript_from_gtf(gtf_path):
    import regex as re
    import pandas as pd
    import gzip
    rx=re.compile(r'"[^"]*"(*SKIP)(*FAIL)| \s*')
    d={}
    with open(gtf_path,'r') as fh:
        for line in fh:
            if not line.startswith('#'):
                col=line.split('\t')
                if  col[2]== 'exon':
                    t=[rx.split((j.strip())) for j in col[8].split(';')]
                    dt={i[0].strip():i[1].strip() for i in t if len(i)>1}
                    gene=dt.get('gene_id').strip('"')
                    transcript=dt.get('transcript_id').strip('"')
                    #exonnumber=dt.get('exon_number').strip('"')
                    #if gene not in d.keys():
                    #    d.setdefault(gene,{}).setdefault(transcript,[]).append(exonnumber)
                    #elif gene in d.keys():
                    #    d[gene].setdefault(transcript,[]).append(exonnumber)
                    d.setdefault(transcript,[])
                    if not gene in d.get(transcript):
                        d[transcript].append(gene)
    d1={k:v[0] for k,v in d.items()}
    lista=[]
    for k,v in d1.items():
        transcript=k.strip()
        gene=v.strip()
        value=[gene,transcript]
        lista.append(value)

    df=pd.DataFrame(lista, columns=['Gene name', 'Transcript'])

    return df

