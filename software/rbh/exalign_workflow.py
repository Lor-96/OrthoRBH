from software.library.exalign import exaligntab

def exalign_pipeline(blast1,blast2,percentage,threshold,pval,score):
    rbh=exaligntab(blast1).exalignrbh(blast2,percentage,threshold,pval,score)
    print("The number of the Best Reciprocal Hit between the 2 species is: "+str(len(rbh.keys())))
    exaligntab(blast1).pltexaligntop1(species = 'species1')
    exaligntab(blast2).pltexaligntop1(species = 'species2')
    return rbh


