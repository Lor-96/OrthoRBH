import os,sys
sys.path.append(os.path.join(sys.path[0], '..'))
from software.options.extra_argparser6 import argparserextra6
import software.extra.extra6_pipeline as ex6

if __name__ == "__main__":
    params = argparserextra6()
    print("commanding params: ",params)
    mgihomologs=params['mgi']
    tab1=params['t1']
    tab2=params['t2']
    ex6.extra_n6_pipeline(mgihomologs,tab1,tab2)

    