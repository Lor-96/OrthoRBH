def floatorint(string):
    if string.isdigit() == True :
        return int(string)
    elif string.isdigit() == False :
        return float(string)

def unique_file(file_name):
    import os
    name='output'
    if not os.path.exists(name):
        os.makedirs(name)
    
    file_name=f"{name}/{file_name}"

    filename, extension = os.path.splitext(file_name)
    i = 1

    while os.path.exists(file_name):
        file_name = filename + " (" + str(i) + ")" + extension
        i += 1

    return file_name
        
def sequence_refseq_or_orthodb(taxid,refseqfaa,odbfaa,tablespecies,switch):
    from software.library.functions import unique_file
    from software.library.fasta import Fasta
    if switch == False:    
        d1={}
        for v in tablespecies.values():
            value=refseqfaa.data.get(v[0][1].strip()).strip()
            d1.setdefault(v[0][1].strip(),value)
        n1=[]
        for k,v in d1.items():
            n1.append('>%s\n%s' % (k, v))
        with open(unique_file('oneiso_RefSeq_'+taxid.strip('>')+'.faa'), 'w') as species:
            species.write('\n'.join(n1))
        species.close()
        return d1
    else:
        d1={}
        for k,v in tablespecies.items():
            value= odbfaa.data.get(v[0][0].strip()).strip()
            d1.setdefault(v[0][1].strip(),value)
        n1=[]
        for k,v in d1.items():
            n1.append('>%s\n%s' % (k, v))
        with open(unique_file('oneiso_OrthoDBseq_'+taxid.strip('>')+'.faa'), 'w') as species:
            species.write('\n'.join(n1))
        species.close()
        return d1

def getnoncodingtranscriptexa(rbh_exalign,dict1,dict2):
    noncoding=[]
    for i in rbh_exalign:
        transcript1=i[0].strip()
        transcript2=i[1].strip()
        gene1=str(dict1.get(transcript1))
        gene2=str(dict2.get(transcript2))
        if transcript1.startswith(('NR_','XR_')) or transcript2.startswith(('NR_','XR_')):
            transcript=transcript1+'\t'+transcript2
            gene=gene1+'\t'+gene2
            noncoding.append(transcript+'\t'+gene)
    with open(unique_file('noncoding_transcript_exalign.txt'),'w') as txt:
        txt.write('\n'.join(noncoding))
    txt.close()
    return None