import os,sys
sys.path.append(os.path.join(sys.path[0], '..'))
from software.options.extra_argparser1 import argparserextra1
from software.library.orthodb import Tab_odb
import software.extra.extra1_pipeline as ex1

if __name__ == "__main__":
    params = argparserextra1()
    print("commanding params: ",params)
    taxid1=params['tx1']
    taxid2=params['tx2']
    gtfsp1=params['gtf1']
    gtfsp2=params['gtf2']
    allfasta=params['af']
    og2genes=params['og2g']
    genes=params['gen']
    if params['lvl'] != None:
        level=params['lvl']
        ex1.extra_n1_pipeline(taxid1,taxid2,level, gtfsp1,gtfsp2,allfasta,og2genes,genes)
    else:
        level=Tab_odb(params['lv2sp']).getlevel(taxid1,taxid2)
        ex1.extra_n1_pipeline(taxid1,taxid2,level, gtfsp1,gtfsp2,allfasta,og2genes,genes)
    
    