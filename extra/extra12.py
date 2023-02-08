import os,sys
sys.path.append(os.path.join(sys.path[0], '..'))
from software.options.extra_argparser12 import argparserextra12
import software.extra.extra10_pipeline as ex12

if __name__ == "__main__":
    params = argparserextra12()
    print("commanding params: ",params)
    rbh=params['rbh']
    mgi=params['mgi']
    odb=params['odb']
    biomart=params['bio']
    exalign=params['exa']
    gtf1=params['gtf1']
    gtf2=params['gtf2']

    ex12.extra_n10_pipeline(rbh,mgi,odb,biomart,exalign,gtf1,gtf2)