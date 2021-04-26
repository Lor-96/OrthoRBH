def cdsintoprotein(cds):
    with open (cds, "r") as myfile:
        data=myfile.readlines()
        
        #### MAKE A DICTIONARY WITH THE FASTA AS CHROMOSOMES AS KEYS
        d2={}
        for line in data:
            if line.startswith('>'):
                seq = line[1:line.find(' ')].strip('lcl|')
                d2[seq] = []
            else:
                d2[seq].append(line[:-1].upper())
        for seq in d2:
            d2[seq] = '\n'.join(d2[seq])
        
        
        def n_to_aa(seq):
            seq=seq.replace("\n","")

            table = {"TTT":"F", "TCT":"S", "TAT":"Y", "TGT":"C",
                     "TTC":"F", "TCC":"S", "TAC":"Y", "TGC":"C",
                     "TTA":"L", "TCA":"S", "TAA":"*", "TGA":"*",
                     "TTG":"L", "TCG":"S", "TAG":"*", "TGG":"W",
                     "CTT":"L", "CCT":"P", "CAT":"H", "CGT":"R",
                     "CTC":"L", "CCC":"P", "CAC":"H", "CGC":"R",
                     "CTA":"L", "CCA":"P", "CAA":"Q", "CGA":"R",
                     "CTG":"L", "CCG":"P", "CAG":"Q", "CGG":"R",
                     "ATT":"I", "ACT":"T", "AAT":"N", "AGT":"S",
                     "ATC":"I", "ACC":"T", "AAC":"N", "AGC":"S",
                     "ATA":"I", "ACA":"T", "AAA":"K", "AGA":"R",
                     "ATG":"M", "ACG":"T", "AAG":"K", "AGG":"R",
                     "GTT":"V", "GCT":"A", "GAT":"D", "GGT":"G",
                     "GTC":"V", "GCC":"A", "GAC":"D", "GGC":"G",
                     "GTA":"V", "GCA":"A", "GAA":"E", "GGA":"G",
                     "GTG":"V", "GCG":"A", "GAG":"E", "GGG":"G",}
            
            protein=''
            if len(seq)%3 == 0:
                for i in range(0, len(seq), 3):
                    codon = seq[i:i + 3]
                    protein+= table[codon]
            return protein

    d3={k:n_to_aa(v) for k,v in d2.items()}
    
    def insert_newlines(string, every=80):
        return '\n'.join(string[i:i+every] for i in range(0, len(string), every))
    
    d3={k:insert_newlines(v) for k,v in d3.items()}
    
    return d3

x=cdsintoprotein('CDS_fasta.fna')
