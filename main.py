import os
from software.library.functions import floatorint
from software.options.argparser import argparser

if __name__ == "__main__":
    params = argparser()
    print("commanding params: ",params)
    blast1=params['b1']
    blast2=params['b2']
    gtfsp1=params['gtf1']
    gtfsp2=params['gtf2']
    percentage=floatorint(params['perc'])
    bitscore=floatorint(params['bit'])
    pvalue=floatorint(params['ev'])
    score=floatorint(params['sc'])
    transcript=params['tr']

    import software.rbh.rbh_workflow as rbhw

    rbhw.rbh_workflow(blast1,blast2,gtfsp1,gtfsp2,percentage,bitscore,pvalue,score,transcript)
    
