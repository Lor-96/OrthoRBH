import os,sys
sys.path.append(os.path.join(sys.path[0], '..'))
from software.options.extra_argparser10 import argparserextra10
import software.library.doubledictionary as ex10

if __name__ == "__main__":
    params = argparserextra10()
    print("commanding params: ",params)
    rbh=params['rbh1']
    rbhexalign=params['rbh2']
    rbhcds=params['rbh3']
    gtf1=params['gtf1']
    gtf2=params['gtf2']

    ex10.doubledictionary_comaparison(rbh,rbhexalign,rbhcds,gtf1,gtf2)