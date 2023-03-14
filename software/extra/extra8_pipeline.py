def extra_n8_pipeline(rbhprotein,rbhcds,gtf1,gtf2):
    from software.library.functions import unique_file
    from software.library.rbh import Rbh
    #from software.library.cdsutrfunctions import get_cds_exceeded, get_common_id_brh,get_all_cds_final_list
    from software.library.gtf_functions import get_name_protein_transcript_from_cds_in_gtf
    #import pandas as pd

    protein=Rbh(rbhprotein).readrbhpath()
    cds=Rbh(rbhcds).readrbhpath()
    protein=[k.strip() for k in protein.keys()]
    cds=[k.strip() for k in cds.keys()]

    sp1=get_name_protein_transcript_from_cds_in_gtf(gtf1)
    sp2=get_name_protein_transcript_from_cds_in_gtf(gtf2)

    pt_sp1=dict(zip(sp1['Protein'],sp1['Transcript']))
    pt_sp2=dict(zip(sp2['Protein'],sp2['Transcript']))
    tp_sp1=dict(zip(sp1['Transcript'],sp1['Protein']))
    tp_sp2=dict(zip(sp2['Transcript'],sp2['Protein']))
    pnsp1=dict(zip(sp1['Protein'],sp1['Gene name']))
    pnsp2=dict(zip(sp2['Protein'],sp2['Gene name']))

    cds_names=[]
    for i in cds:
        p1=None
        p2=None
        n1=None
        n2=None
        i1=i.split('\t')[0]
        i2=i.split('\t')[1]
        if i1 in tp_sp1.keys():
            p1=tp_sp1.get(i1)
            if p1 in pnsp1.keys():
                n1=pnsp1.get(p1)
        if i2 in tp_sp2.keys():
            p2=tp_sp2.get(i2)
            if p2 in pnsp2.keys():
                n2=pnsp2.get(p2)
                if p1!= None and p2 != None:
                    if n1 != None and p2 !=None:
                        val=n1+'\t'+n2
                        cds_names.append(val)
    protein_names=[]
    for i in protein:
        n1=None
        n2=None
        p1 = i.split('\t')[0]
        p2 = i.split('\t')[1]
        if p1 in pnsp1.keys():
            n1=pnsp1.get(p1)
        if p2 in pnsp2.keys():
            n2=pnsp2.get(p2)
            if n1 != None and p2 !=None:
                val=n1+'\t'+n2
                protein_names.append(val)
                
    common=[]
    notcommon=[]
    for i in cds_names:
        if i in protein_names:
            common.append(i)
        else:
            notcommon.append(i)
    
    print('The number of the genes that are common is: '+str(len(common)))
    
    with open(unique_file('cds_notcommon_oneisoform.txt'), 'w') as txt:
        txt.write('\n'.join(notcommon))
    txt.close()
