import os,sys
sys.path.append(os.path.join(sys.path[0], '..'))
from software.options.argparserR2 import argparserR2
import rpy2.robjects as robjects
from rpy2.robjects.packages import  importr

if __name__ == "__main__":
    params = argparserR2()
    print("commanding params: ",params)
    mgi_db=params['mgi']
    odb_db=params['odb']
    biomart_db=params['bio']
    orthorbh=params['rbh']
    exalign=params['exarbh']
    cds=params['cdsrbh']
    cdsnotcommon=params['cdsnc']
    

    graphics=importr("graphics")
    r = robjects.r
    rsource=os.path.abspath(os.path.join('software', os.pardir))
    rsource=rsource+'\\software\\rscript\\'
    r['source'](rsource+"upsetfunction.R")
    upsetplotfunctionr=robjects.globalenv['upsetplotfunction']
    upsetplotfunctionr(mgi_db = mgi_db, odb_db = odb_db,  biomart_db = biomart_db , orthorbh = orthorbh, exalign = exalign, cds= cds, cdsnotcommon= cdsnotcommon)
