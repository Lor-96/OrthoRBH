import os,sys
sys.path.append(os.path.join(sys.path[0], '..'))
from software.options.argparserR1 import argparserR1
import rpy2.robjects as robjects

if __name__ == "__main__":
    params = argparserR1()
    print("commanding params: ",params)
    mgi_db=params['mgi']
    odb_db=params['odb']
    biomart_db=params['bio']
    exanotcom=params['exa']
    cdsnotcom=params['cds']

    r = robjects.r

    rsource=os.path.abspath(os.path.join('software', os.pardir))
    rsource=rsource+'\\software\\rscript\\'
    r['source'](rsource+"barplotfunction.R")
    barplot_function_r=robjects.globalenv['barplotnotcommon']
    barplot_function_r(mgi_db,odb_db,biomart_db,exanotcom, cdsnotcom)

