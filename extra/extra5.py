import os,sys
sys.path.append(os.path.join(sys.path[0], '..'))
from software.library.functions import floatorint
from software.options.extra_argparser5 import argparserextra5
import software.extra.extra5_pipeline as ex5

if __name__ == "__main__":
    params = argparserextra5()
    print("commanding params: ",params)
    biomartexport=params['b']
    predicted=params['p']
    gtf1=params['gtf1']
    gtf2=params['gtf2']
    tav1=params['t1']
    tav2=params['t2']
    bmpath1=params['bt1']
    bmpath2=params['bt2']
    conversion_genenames=params['c']

    ex5.extra_n5_pipeline(biomartexport,predicted, gtf1,gtf2,tav1,tav2,bmpath1,bmpath2,conversion_genenames)

