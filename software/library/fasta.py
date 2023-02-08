class Fasta:
    """
    Create a class that allow us to better handling the fasta file
    """
    def __init__(self,path):
        self.path=path
        self.data={}

    def ODBfasta(self,taxid, filename):
        from software.library.functions import unique_file
        sp={}
        with open(self.path, 'r') as file:
            for line in file:
                if line.startswith('>'):
                    columns=line.split('\t')
                    if columns[1].strip() == taxid.strip():
                        sp.setdefault(columns[0].strip(),next(file))
            def insert_newlines(string, every=80):
                return '\n'.join(string[i:i+every] for i in range(0, len(string), every))

            sp={k : insert_newlines(v) for k,v in sp.items()}
            self.data = sp
            
            print("The total number of ID in the fasta file is: "+str(len(self.data.keys())))

            lista=[]
            for k,v in sp.items():
                lista.append('%s\n%s' % (k,v,))
        file_name=unique_file(filename)
        with open(file_name, 'w') as txt:
            txt.write('\n'.join(lista))
        txt.close()
        return None

    def getfasta(self):
        with open(self.path,'r') as file:
            d={}
            for line in file:
                if line.startswith('>'):
                    seq = line[1:line.find(' ')].strip('lcl|')
                    d[seq] = []
                else:
                    d[seq].append(line[:-1].upper().strip())
            for seq in d:
                d[seq] = '\n'.join(d[seq])
            
            self.data = d

    def getfasta_odb(self):
        d={}
        l=[]
        with open(self.path,'r') as file:
            for line in file:
                line=line.strip()
                if not line =='':
                    l.append(line.strip())
        for line in l:
            if line.startswith('>'):
                seq=line.strip('>')
                d[seq]=[]
            else:
                d[seq].append(line.upper())
        for seq in d:
            d[seq] = '\n'.join(d[seq])
            
        self.data = d

        print("The total number of ID in the fasta file is: "+str(len(self.data.keys())))

        lista=[]
        for k,v in d.items():
            lista.append('%s\n%s' % (k.strip(),v.strip(),))
        return lista

    def getlongestisofrom_gtf(self,gtf_table):
        from functools import reduce
        import regex as re
        d=[]
        with open(gtf_table,'r') as file:
            for line in file:
                if not line.startswith('#'):
                    col=line.split('\t')
                    d.append(col)
        ann=list(filter(lambda i:i[2] == 'CDS',d))
        data=[]
        rx=re.compile(r'"[^"]*"(*SKIP)(*FAIL)| \s*')
        for i in ann:
            f=i[8].split(';')
            t=[rx.split((j.strip())) for j in f]
            data.append([i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],t])
        d1={}
        for i in  data:
            x=list(i[8])
            for j in x:
                if j[0] == 'gene_id':
                    key=j[1]
                if j[0] == 'protein_id':
                    value=j[1]
                    d1.setdefault(key,[]).append(value.strip('"'))
        
        with open(self.path,'r') as file:
            d2={}
            for line in file:
                if line.startswith('>'):
                    seq = line[1:line.find(' ')].strip('lcl|')
                    d2[seq] = []
                else:
                    d2[seq].append(line[:-1].upper())
            for seq in d2:
                d2[seq] = '\n'.join(d2[seq])
        d3={}
        for k,v in d1.items():
            for i in v:
                if i in d2.keys():
                    if d3.get(k)== None:
                        d3.setdefault(k,[]).append(i)
                    else:
                        if i not in d3.get(k):
                            d3.setdefault(k,[]).append(i)
        d4={}
        for k,v in d3.items():
            for i in v:
                if i in d2.keys():
                    d4.setdefault(k,[]).append([i,d2.get(i),len(d2.get(i))])
        longiso={}
        for k,v in d4.items():
            if len(v)==1:
                longiso.setdefault(v[0][0],v[0][1])
            elif len(v) > 1:
                l=[]
                for i in v:
                    l.append(i)
                maxv=reduce(max,l)
                longiso.setdefault(maxv[0],maxv[1])
        return longiso