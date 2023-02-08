def extra_n4_pipeline(gtfsp1,gtfsp2,odb_refseq_tab):
    from software.library.functions import unique_file
    from software.library.gtf_functions import get_name_protein_transcript_from_cds_in_gtf
    from software.library.rbh import Rbh

    sp1=get_name_protein_transcript_from_cds_in_gtf(gtfsp1)
    sp2=get_name_protein_transcript_from_cds_in_gtf(gtfsp2)
    p_sp1=dict(zip(sp1['Protein'],sp1['Gene name']))
    p_sp2=dict(zip(sp2['Protein'],sp2['Gene name']))
    
    def convert_genenames(converter1,converter2,table):
        lista=[]
        listanames=[]
        with open(table,'r') as file:
            for line in file:
                col=line.split('\t')
                if not col[2].strip() == 'N/A':
                    v1 = converter1.get(col[2].strip())
                    if not col[3].strip() == 'N/A':
                        v2=converter2.get(col[3].strip())
                        if v1 != None and v2 != None:
                            val=col[2].strip().split('.')[0]+'\t'+v1+'\t'+col[3].strip().split('.')[0]+'\t'+v2
                            value=v1+'\t'+v2
                            lista.append(val)
                            listanames.append(value)

        return lista,listanames

    odbflist1,odbflist2=convert_genenames(p_sp1,p_sp2,odb_refseq_tab)

    with open(unique_file('list_OrthoDB.txt'),'w') as txt:
        txt.write('\n'.join(odbflist1))
    txt.close()

    with open(unique_file('odb.txt'),'w') as txt:
        txt.write('\n'.join(odbflist2))
    txt.close()
    return None
