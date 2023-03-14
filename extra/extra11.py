import os,sys
sys.path.append(os.path.join(sys.path[0], '..'))
from software.library.functions import floatorint
from software.options.extra_argparser11 import argparserextra11
import software.library.doubledictionary as ex11

if __name__ == "__main__":
    params = argparserextra11()
    print("commanding params: ",params)
    blast1=params['bl1']
    blast2=params['bl2']
    exaligntab1=params['ext1']
    exaligntab2=params['ext2']
    cdsrbh=params['rbh1']
    exalignrbh=params['rbh2']
    perc=floatorint(params['perc'])
    bit=floatorint(params['bit'])
    exnmatch=floatorint(params['exm'])
    scoreratio=floatorint(params['sc'])
    score=params['score']
    pvalue=params['pval']

    ex11.doubledictionary_transcripts_excluded(blast1,blast2,exaligntab1,exaligntab2, cdsrbh,exalignrbh, perc,bit,exnmatch,scoreratio, pvalue = pvalue, score = score)