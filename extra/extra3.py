import os,sys
sys.path.append(os.path.join(sys.path[0], '..'))
from software.library.functions import floatorint
from software.options.extra_argparser3 import argparserextra3
from software.library.orthodb import Tab_odb
import software.extra.extra3_pipeline as ex3

if __name__ == "__main__":
    params = argparserextra3()
    print("commanding params: ",params)
    rbh=params['rbh']
    orthodb=params['odb']
    tab1=params['t1']
    tab2=params['t2']
    blast1=params['b1']
    blast2=params['b2']
    perc=floatorint(params['perc'])
    bit=floatorint(params['bit'])
    ex3.extra_n3_pipeline(rbh,orthodb,tab1,tab2,blast1,blast2,perc,bit)
    