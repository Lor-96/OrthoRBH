class Tab_odb:

    def __init__(self,path):
        self.path= path

    def getgenes(self,species1,species2):
        with open(self.path, 'r') as file:
            l1=[]
            l2=[]
            for line in file:
                columns=line.split('\t')
                if columns[1].strip() == species1:
                    l1.append(columns)
                if columns[1].strip() == species2:
                    l2.append(columns)
        print('The genes of the first species are: ' + str(len(l1)) + ' by OrthoDB')
        print('The genes of the second species are: '+ str(len(l2)) +' by OrthoDB')

        d1={i[0].strip():i[2].strip() for i in l1}
        d2={i[0].strip():i[2].strip() for i in l2}
        return d1,d2
    
    def getorthologs(self,level,d_species1,d_species2):
        
        import time
        start_time=time.time()
        with open(self.path ,'r') as file:
            og1=[]
            og2=[]
            for line in file:
                columns=line.split('\t')
                if level in columns[0].strip():
                    if columns[1].strip() in list(d_species1.keys()):
                        og1.append(columns[0].strip() +'\t'+ columns[1].strip()+'\t'+d_species1.get(columns[1].strip()))
                    if columns[1].strip() in list(d_species2.keys()):
                        og2.append(columns[0].strip() +'\t'+ columns[1].strip()+'\t'+d_species2.get(columns[1].strip()))
        end_time=time.time()

        print('The total time for the loop is: ' + str(end_time - start_time)+' seconds that in minutes are: '+str((end_time - start_time)/60)+' minutes')
        print('The genes that are in the Orhtologs Group '+level +' by OrthoDB are '+ str(len(og1)) +' for the first species')
        print('The genes that are in the Orthologs Group '+level +' by OrthoDB are '+ str(len(og2)) +' for the second species')

        d={}
        for l in og1:
            columns=l.split('\t')
            for i in og2:
                col=i.split('\t')
                if columns[0].strip() == col[0].strip():
                    d.setdefault(col[0].strip(),[]).append(columns[1].strip() +'\t'+col[1].strip())
        
        """
        Eliminate the paralogs genes by selecting the orthologs groups where there are only one gene
        """

        ortho={k:v[0] for k,v in d.items() if len(v) == 1}
        print("The number of Orthologs by OrthoDB is: "+str(len(ortho.keys())))
        
        return ortho

    def getlevel(self,taxid1,taxid2):
        with open(self.path) as file:
            level=[]
            tax1=None
            tax2=None
            for line in file:
                col=line.split('\t')
                if col[1].strip() == taxid1:
                    tax1= {col[1].strip():col[3].strip('{}').split(',')}
                if col[1].strip() == taxid2:
                    tax2= {col[1].strip():col[3].strip('{}').split(',')}
                if tax1 != None and tax2 != None:
                    for i in tax1.get(taxid1):
                        for j in tax2.get(taxid2):
                            if i == j:
                                if not i in level:
                                    level.append(i)
        lev=level[len(level)-1].strip('}')
        return lev