import os,sys
sys.path.append(os.path.join(sys.path[0], '..'))
from software.library.functions import floatorint
from software.options.extra_argparser4 import argparserextra4
import software.extra.extra4_pipeline as ex4

if __name__ == "__main__":
    params = argparserextra4()
    print("commanding params: ",params)
    gtfsp1=params['gtf1']
    gtfsp2=params['gtf2']
    odb_refseq_tab=params['t']

    ex4.extra_n4_pipeline(gtfsp1,gtfsp2,odb_refseq_tab)