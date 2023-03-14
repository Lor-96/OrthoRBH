import os,sys
sys.path.append(os.path.join(sys.path[0], '..'))
from software.options.extra_argparser8 import argparserextra8
import software.extra.extra8_pipeline as ex8

if __name__ == "__main__":
    params = argparserextra8()
    print("commanding params: ",params)
    rbhprotein=params['rbh1']
    rbhcds=params['rbh2']
    gtf1=params['gtf1']
    gtf2=params['gtf2']

    ex8.extra_n8_pipeline(rbhprotein = rbhprotein, rbhcds=rbhcds ,gtf1 = gtf1,gtf2 =gtf2)