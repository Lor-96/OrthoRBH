def extra_n1_pipeline(taxid1,taxid2,level, gtfsp1,gtfsp2,allfasta,og2genes,genes):
    from software.library.fasta import Fasta
    from software.library.orthodb import Tab_odb
    from software.library.gtf_functions import genebiotype
    from software.library.functions import unique_file

    genebiotype(gtfsp1,'gene_biotype_sp1')
    genebiotype(gtfsp2,'gene_biotype_sp2')

    Fasta(allfasta).ODBfasta(taxid1, taxid1+'.faa')
    Fasta(allfasta).ODBfasta(taxid2, taxid2+'.faa')

    dsp1,dsp2=Tab_odb(genes).getgenes(taxid1,taxid2)

    ortho=Tab_odb(og2genes).getorthologs(level,dsp1,dsp2)

    with open(unique_file(taxid1+'_'+taxid2+'_ODB_orthologs.txt'),'w') as txt:
        txt.write('\n'.join(ortho.values()))
    txt.close()
    return None
