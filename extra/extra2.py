import os,sys
sys.path.append(os.path.join(sys.path[0], '..'))
from software.library.functions import floatorint
from software.options.extra_argparser2 import argparserextra2
import software.extra.extra2_pipeline as ex2

if __name__ == "__main__":
    params = argparserextra2()
    print("commanding params: ",params)
    blast1=params['bl1']
    blast2=params['bl2']
    taxid1=params['tx1']
    taxid2=params['tx2']
    faa1=params['fa1']
    faa2=params['fa2']
    odbfaa1=params['ofa1']
    odbfaa2=params['ofa2']
    percentage1=floatorint(params['perc1'])
    percentage2=floatorint(params['perc2'])
    sw1=params['sw1']
    sw2=params['sw2']

    ex2.extra_n2_pipeline(blast1,taxid1,faa1,percentage1,odbfaa1,blast2 ,taxid2,faa2,percentage2,odbfaa2,sw1,sw2)