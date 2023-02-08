import os,sys
sys.path.append(os.path.join(sys.path[0], '..'))
from software.options.extra_argparser9 import argparserextra9
import software.extra.extra9_pipeline as ex9

if __name__ == "__main__":
    params = argparserextra9()
    print("commanding params: ",params)
    cds1=params['cds1']
    cds2=params['cds2']

    ex9.extra_n9_pipeline(cds1,cds2)