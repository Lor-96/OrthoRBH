def extra_n2_pipeline(blast1,taxid1,faa1,percentage1,odbfaa1,blast2 ,taxid2,faa2,percentage2,odbfaa2,sw1,sw2):
    from software.library.fasta import Fasta
    from software.library.blast import Blast
    from software.library.functions import  sequence_refseq_or_orthodb,unique_file

    obj1=Blast(blast1)   
    obj2=Blast(blast2)

    sp1,nc1=obj1.conversiontable(percentage1)
    sp2,nc2=obj2.conversiontable(percentage2)

    tab1=[k.strip()+'\t'+v[0][1].strip() for k,v in sp1.items()]
    tab2=[k.strip()+'\t'+v[0][1].strip() for k,v in sp2.items()]

    with open(unique_file('tab_sp1.txt'),'w') as file1, open(unique_file('tab_sp2.txt'),'w') as file2:
        file1.write('\n'.join(tab1))
        file2.write('\n'.join(tab2))
    file1.close()
    file2.close()

    sp1faa= Fasta(faa1)
    sp2faa=Fasta(faa2)

    fasta1=sp1faa.getfasta()
    fasta2=sp2faa.getfasta() 

    odb_sp1=Fasta(odbfaa1)
    odb_sp2=Fasta(odbfaa2)

    odbfasta1=odb_sp1.getfasta_odb()
    odbfasta2=odb_sp2.getfasta_odb()

    d1=sequence_refseq_or_orthodb(taxid=taxid1,refseqfaa=sp1faa,odbfaa=odb_sp1,tablespecies=sp1,switch=sw1)
    d2=sequence_refseq_or_orthodb(taxid=taxid2,refseqfaa=sp2faa,odbfaa=odb_sp2,tablespecies=sp2,switch=sw2)

    print("The total number of the genes selected by single isoform per gene through the OrthoDB blast are: "+str(len(d1.keys())))
    print("The total number of the genes selected by single isoform per gene through the OrthoDB blast are: "+str(len(d2.keys())))
