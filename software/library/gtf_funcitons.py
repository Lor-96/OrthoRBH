
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
