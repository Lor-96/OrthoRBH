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

def print_final_tab_brh(brh_protein,dict1,dict2):
    from software.library.functions import unique_file
    lista=[]
    for i in brh_protein:
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

def doubledictionary_pipeline(rbh,converter1,converter2):
    brh_dd=gene_name_result(rbh,converter1,converter2)
    brh_discrepancy=[k for k,v in brh_dd.items() if len(v) != 1]
    if len(brh_discrepancy) > 0:
        conv,notconv=trimming_discrepancy_dd(brh_dd)
        print_discrepancies(notconv)
        print_dd(conv)
        print('Some genes are associated to more than one, number of discrepancy: '+str(len(brh_discrepancy)))
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
        print('Some genes are associated to more than one, number of discrepancy: '+str(len(brh_discrepancy)))
        print('The number of discrepancy not converted is: '+str(len(notconv)))
    else:
        print_exalign_dd(brh_dd)
        print('No discrepancy found')
        print_exalign_final_tab_brh(rbh, converter1,converter2)
