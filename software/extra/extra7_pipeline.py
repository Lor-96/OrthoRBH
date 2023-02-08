def extra_n7_pipeline(blast1,blast2,gtf1,gtf2,genome1,genome2,logical):
    from software.library.functions import unique_file

    if logical == True:
        import software.library.cdsutrfunctions as cds_utr

        coordinates_cds_sp1,table_protein_transcript_sp1=cds_utr.get_cds_coordinates_and_table(gtf1)

        lista_sp1=cds_utr.readoneisoID(blast1,table_protein_transcript_sp1)

        genome_sp1=cds_utr.get_genome(genome1,coordinates_cds_sp1)

        cds_sp1= cds_utr.get_cds_from_genomic(coordinates_cds_sp1, genome_sp1,lista_sp1)

        with open(unique_file('cds_sp1.fna'),'w') as txt:
            txt.write('\n'.join(cds_sp1))
        txt.close()

        del(coordinates_cds_sp1, genome_sp1, table_protein_transcript_sp1,lista_sp1)

        coordinates_cds_sp2,table_protein_transcript_sp2=cds_utr.get_cds_coordinates_and_table(gtf2)

        lista_sp2=cds_utr.readoneisoID(blast2,table_protein_transcript_sp2)

        genome_sp2=cds_utr.get_genome(genome2,coordinates_cds_sp2)

        cds_sp2= cds_utr.get_cds_from_genomic(coordinates_cds_sp2, genome_sp2,lista_sp2)

        with open(unique_file('cds_sp2.fna'),'w') as txt:
            txt.write('\n'.join(cds_sp2))
        txt.close()
        return None
    else:
        import software.library.cdsutrfunctions as cds_utr

    coordinates_cds_sp1,table_protein_transcript_sp1=cds_utr.get_cds_coordinates_and_table(gtf1)

    lista_sp1=cds_utr.readoneisoID(blast1,table_protein_transcript_sp1)

    genome_sp1=cds_utr.get_genome(genome1,coordinates_cds_sp1)

    exon_coordinates_sp1=cds_utr.get_exon_coordinates(gtf1)

    utr5_sp1,utr3_sp1=cds_utr.get_utr_from_genomic(coordinates_cds_sp1, exon_coordinates_sp1, genome_sp1,lista_sp1, return_ex= True)

    with open('utr5_sp1.fna','w') as txt:
        txt.write('\n'.join(utr5_sp1))
    txt.close()

    with open('utr3_sp1.fna','w') as txt:
        txt.write('\n'.join(utr3_sp1))
    txt.close()

    del(coordinates_cds_sp1,table_protein_transcript_sp1,lista_sp1,genome_sp1,exon_coordinates_sp1)

    coordinates_cds_sp2,table_protein_transcript_sp2=cds_utr.get_cds_coordinates_and_table(gtf2)

    lista_sp2=cds_utr.readoneisoID(blast2,table_protein_transcript_sp2)

    genome_sp2=cds_utr.get_genome(genome2,coordinates_cds_sp2)

    exon_coordinates_sp2=cds_utr.get_exon_coordinates(gtf2)

    utr5_sp2,utr3_sp2=cds_utr.get_utr_from_genomic(coordinates_cds_sp2, exon_coordinates_sp2, genome_sp2,lista_sp2, return_ex = True)

    with open('utr5_sp2.fna','w') as txt:
        txt.write('\n'.join(utr5_sp2))
    txt.close()

    with open('utr3_sp2.fna','w') as txt:
        txt.write('\n'.join(utr3_sp2))
    txt.close()
    return None
