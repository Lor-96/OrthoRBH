import os,sys
sys.path.append(os.path.join(sys.path[0], '..'))
from software.options.extra_argparser7 import argparserextra7
import software.extra.extra7_pipeline as ex7

if __name__ == "__main__":
    params = argparserextra7()
    print("commanding params: ",params)
    oneiso1=params['faa1']
    oneiso2=params['faa2']
    gtf1=params['gtf1']
    gtf2=params['gtf2']
    genome1=params['g1']
    genome2=params['g2']
    logical=params['l']

    ex7.extra_n7_pipeline(oneiso1,oneiso2,gtf1,gtf2,genome1,genome2,logical)