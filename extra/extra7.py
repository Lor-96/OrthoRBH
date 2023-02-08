import os,sys
sys.path.append(os.path.join(sys.path[0], '..'))
from software.options.extra_argparser7 import argparserextra7
import software.extra.extra7_pipeline as ex7

if __name__ == "__main__":
    params = argparserextra7()
    print("commanding params: ",params)
    blast1=params['bl1']
    blast2=params['bl2']
    gtf1=params['gtf1']
    gtf2=params['gtf2']
    genome1=params['g1']
    genome2=params['g2']
    logical=params['l']

    ex7.extra_n7_pipeline(blast1,blast2,gtf1,gtf2,genome1,genome2,logical)