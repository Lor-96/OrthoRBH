def gene_name_result(lista, convertersp1,convertersp2):
    r={}
    for pro_trnsc in lista:
        name1=None
        name2= None
        if pro_trnsc[0] in convertersp1.keys():
            name1= convertersp1.get(pro_trnsc[0])
        if pro_trnsc[1] in convertersp2.keys():
            name2=convertersp2.get(pro_trnsc[1])
            if name1 != None and name2!= None:
                r.setdefault(name1,{}).setdefault(name2,[]).append(pro_trnsc)
    result={}
    for k,v in r.items():
        for i,j in v.items():
            result.setdefault(k,{}).setdefault(i,len(j))

    return result

def print_discrepancies(dictionary):
    import os
    from software.library.functions import unique_file
    filename=unique_file('RBH_discrepancies.txt')
    with open(filename,'w') as txt:
        for k,v in dictionary.items():
            txt.write(k+'\n')
            for i,j in v.items():
                txt.write('\t'+str(i)+':'+str(j)+'\n')
        txt.close()
    return None

def print_exalign_discrepancies(dictionary):
    import os
    from software.library.functions import unique_file
    filename=unique_file('exalign_RBH_discrepancies.txt')
    with open(filename,'w') as txt:
        for k,v in dictionary.items():
            txt.write(k+'\n')
            for i,j in v.items():
                txt.write('\t'+str(i)+':'+str(j)+'\n')
        txt.close()
    return None

def print_dd(dictionary=dict):
    import os
    from software.library.functions import unique_file
    filename=unique_file('RBH_gene_names.txt')
    with open(filename,'w') as txt:
        for k,v in dictionary.items():
            for i,j in v.items():
                if j>1:
                    print('Are present '+str(j)+' proteins/transcripts that encode for the gene: '+i)
                val=k+'\t'+i+'\n'
                txt.write(val)
        txt.close()
    return None

def print_exalign_dd(dictionary=dict):
    import os
    from software.library.functions import unique_file
    filename=unique_file('exalign_RBH_gene_names.txt')
    with open(filename,'w') as txt:
        for k,v in dictionary.items():
            for i,j in v.items():
                if j>1:
                    print('Are present '+str(j)+' proteins/transcripts that encode for the gene: '+i)
                val=k+'\t'+i+'\n'
                txt.write(val)
        txt.close()
    return None

def trimming_discrepancy_dd(dictionary):
    from functools import reduce
    notconvertible={}
    convertible={}
    for k,v in dictionary.items():
        if len(v) != 1:
            lista=list(v.items())
            result=reduce(lambda x, y: x if (x[1] > y[1]) else y, list(v.items()))
            logical=all(i[1] == lista[0][1] for i in lista)
            if logical == True:
                notconvertible.setdefault(k,v)
            else :
                convertible.setdefault(k,{}).setdefault(result[0],result[1])
        else :
            convertible.setdefault(k,v)
    return convertible,notconvertible

def print_final_tab_brh(rbh_pro_tr,dict1,dict2):
    from software.library.functions import unique_file
    lista=[]
    for i in rbh_pro_tr:
        v1=str(dict1.get(i[0].strip())).strip()
        v2=str(dict2.get(i[1].strip())).strip()
        val = i[0].strip().split('.')[0]+'\t'+v1+'\t'+i[1].strip().split('.')[0]+'\t'+v2
        lista.append(val)
    filename=unique_file('list_BRH.txt')
    with open(filename,'w') as txt:
        txt.write('\n'.join(lista))
    txt.close()
    return None

def print_exalign_final_tab_brh(rbh,dict1,dict2):
    from software.library.functions import unique_file
    lista=[]
    for i in rbh:
        v1=str(dict1.get(i[0].strip())).strip()
        v2=str(dict2.get(i[1].strip())).strip()
        val = i[0].strip().split('.')[0]+'\t'+v1+'\t'+i[1].strip().split('.')[0]+'\t'+v2
        lista.append(val)
    filename=unique_file('list_exalign_BRH.txt')
    with open(filename,'w') as txt:
        txt.write('\n'.join(lista))
    txt.close()
    return None

def compare_tp(dictionary1,dictionary2):
    def list_dd(dictionary):
        flist=[]
        for k,v in dictionary.items():
            for i,j in v.items():
                val=k.strip()+'\t'+i.strip()
                flist.append(val)
        return flist
    l1=list_dd(dictionary1)
    l2=list_dd(dictionary2)
    def comparison2(lista1,lista2):
        common=[]
        notcommon=[]
        for i in lista1:
            if i in lista2:
                common.append(i)
            else:
                notcommon.append(i)
        return common,notcommon
    
    common,notcommon=comparison2(l1,l2)

    return common,notcommon

def compare_dd(dictionary1,dictionary2):
    def list_dd(dictionary):
        flist=[]
        for k,v in dictionary.items():
            for i,j in v.items():
                val=k.strip()+'\t'+i.strip()
                flist.append(val)
        return flist
    l1=list_dd(dictionary1)
    l2=list_dd(dictionary2)
    def comparison(lista1,lista2):
        common=[]
        notcommonl1=[]
        notcommonl2=[]
        for i in lista1:
            if i in lista2:
                common.append(i)
            else:
                notcommonl1.append(i)
        for i in lista2:
            if i not in lista1:
                notcommonl2.append(i)
        return common,notcommonl1,notcommonl2
    
    common,notcommon1,notcommon2=comparison(l1,l2)

    return common,notcommon1,notcommon2

def compare_transcript(lista1,lista2):
    def gluevalues(lista):
        newlist=[]
        for i in lista:
            if len(i) > 1:
                if len(i)==2:
                    val=i[0]+'\t'+i[1]
                    newlist.append(val)
            else:
                newlist.append(i)
        return newlist
    l1=gluevalues(lista1)
    l2=gluevalues(lista2)
    common=[]
    notcommonl1=[]
    notcommonl2=[]
    for i in l1:
        if i in l2:
            common.append(i)
        else:
            notcommonl1.append(i)
    for i in l2:
        if i not in l1:
            notcommonl2.append(i)

    return common, notcommonl1, notcommonl2

def doubledictionary_pipeline(rbh,converter1,converter2):
    brh_dd=gene_name_result(rbh,converter1,converter2)
    brh_discrepancy=[k for k,v in brh_dd.items() if len(v) != 1]
    if len(brh_discrepancy) > 0:
        conv,notconv=trimming_discrepancy_dd(brh_dd)
        print_discrepancies(notconv)
        print_dd(conv)
        print('Some genes are associated to more than one, number of discrepancies: '+str(len(brh_discrepancy)))
        print('The number of discrepancy not converted is: '+str(len(notconv)))
    else:
        print_dd(brh_dd)
        print('No discrepancy found')
        print_final_tab_brh(rbh, converter1,converter2)
     
def doubledictionary_exalign_pipeline(rbh,converter1,converter2):
    brh_dd=gene_name_result(rbh,converter1,converter2)
    brh_discrepancy=[k for k,v in brh_dd.items() if len(v) != 1]
    if len(brh_discrepancy) > 0:
        conv,notconv=trimming_discrepancy_dd(brh_dd)
        print_exalign_discrepancies(notconv)
        print_exalign_dd(conv)
        print('Some genes are associated to more than one, number of discrepancies: '+str(len(brh_discrepancy)))
        print('The number of discrepancy not converted is: '+str(len(notconv)))
    else:
        print_exalign_dd(brh_dd)
        print('No discrepancy found')
        print_exalign_final_tab_brh(rbh, converter1,converter2)

def doubledictionary_comaparison(rbh,exalignrbh,cdsrbh,gtf1,gtf2):
    from software.library.doubledictionary import compare_tp,compare_dd,gene_name_result, trimming_discrepancy_dd
    from software.library.gtf_functions import get_name_protein_transcript_from_cds_in_gtf
    import pandas as pd
    from software.library.functions import unique_file
    from software.library.rbh import Rbh
    from software.library.exalign import exaligndict_rbh

    sp1=get_name_protein_transcript_from_cds_in_gtf(gtf1)
    sp2=get_name_protein_transcript_from_cds_in_gtf(gtf2)
    brhprotein=list(Rbh(rbh).readrbhpath().keys())
    brhcds=list(Rbh(cdsrbh).readrbhpath().keys())
    brhexa=list(exaligndict_rbh(exalignrbh).name)
    brhprotein=[i.strip('\n').split('\t') for i in brhprotein]
    brhcds=[i.strip('\n').split('\t') for i in brhcds]
    brhexa=[i.strip('\n').split('\t') for i in brhexa]
    p_sp1=dict(zip(sp1['Protein'],sp1['Gene name']))
    t_sp1=dict(zip(sp1['Transcript'],sp1['Gene name']))
    p_sp2=dict(zip(sp2['Protein'],sp2['Gene name']))
    t_sp2=dict(zip(sp2['Transcript'],sp2['Gene name']))
    exalign_dd=gene_name_result(brhexa,t_sp1,t_sp2)
    standard_dd=gene_name_result(brhcds,t_sp1,t_sp2)
    brhprotein_dd=gene_name_result(brhprotein,p_sp1,p_sp2)

    exalign_discrepancy=[k for k,v in exalign_dd.items() if len(v) != 1]
    standard_discrepancy=[k for k,v in standard_dd.items() if len(v) != 1]
    brhprotein_discrepancy=[k for k,v in brhprotein_dd.items() if len(v) != 1]

    exa_conv_dd, exa_nconv_dd=trimming_discrepancy_dd(exalign_dd)
    cds_conv_dd,cds_nconv_dd=trimming_discrepancy_dd(standard_dd)
    protein_conv_dd,protein_nconv_dd=trimming_discrepancy_dd(brhprotein_dd)

    exacommonp,exanotcommonp=compare_tp(exa_conv_dd,protein_conv_dd)
    cdscommonp,cdsnotcommonp=compare_tp(cds_conv_dd,protein_conv_dd)
    
    with open(unique_file('exalignnotcommonwithbrh.txt'),'w') as txt:
        txt.write('\n'.join(exanotcommonp))
    txt.close()

    with open(unique_file('cdsnotcommonwithbrh.txt'),'w') as txt:
        txt.write('\n'.join(cdsnotcommonp))

    print('The number or the common genes between Exalign and the protein isoforms is: '+str(len(exacommonp)))
    print('The number or the common genes between the CDS and the protein isoforms is: '+str(len(cdscommonp)))
    print('The number of the not common genes between Exalign and the protein isoforms is: '+str(len(exanotcommonp)))
    print('The number of the not commomn genes between the CDS and the protein isoforms is: '+str(len(cdsnotcommonp)))

    txt.close()

    commonnames,notcommonexa,notcommoncds=compare_dd(exa_conv_dd,cds_conv_dd)

    print('The number of the common genes between the genes predicted by Exalign and the CDS is:' +str(len(commonnames)))
    print('the number of the genes not common between exalign and the CDS is: '+str(len(notcommonexa)))
    print('The number of the genes not common between CDS and Exalign is: '+str(len(notcommoncds)))

    return None

def doubledictionary_transcripts_excluded(blast1,blast2,exaligntab1,exaligntab2, cdsrbh,exalignrbh, perc,bit,exnmatch,scoreratio,score,pvalue):
    from software.library.rbh import Rbh
    from software.library.exalign import exaligndict_rbh    
    from software.library.doubledictionary import compare_transcript
    from software.library.excludedfunctions import getexcluded1,getexcluded2
    brhcds=list(Rbh(cdsrbh).readrbhpath().keys())
    brhexa=list(exaligndict_rbh(exalignrbh).name)
    brhcds=[i.strip('\n').split('\t') for i in brhcds]
    brhexa=[i.strip('\n').split('\t') for i in brhexa]

    commontrnsc,notcommontrnscexa,notcommontrnsccds=compare_transcript(brhexa,brhcds)

    dexa={i:i for i in notcommontrnscexa}
    dcds={i:i for i in notcommontrnsccds}

    print('The number of the common transcripts between the genes predicted by Exalign and the CDS is:' +str(len(commontrnsc)))
    print('the number of the hits not common between exalign and the CDS is: '+str(len(dexa)))
    print('The number of the hits not common between CDS and Exalign is: '+str(len(dcds)))
    getexcluded1(path1 = blast1,path2 = blast2, dictionary = dexa, percent = perc, threshold = bit) #0,0
    getexcluded2(path1 = exaligntab1, path2 = exaligntab2, dictionary = dcds, percentage = exnmatch, threshold = scoreratio, pvalue = pvalue , score = score) #0,0

    return None
