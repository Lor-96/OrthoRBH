with open('pDmel_vs_pDpse.txt', 'r') as infile:
    lines = [line for line in infile if not line.startswith('#')]
with open ('pDmelvspDpse_nocomments.txt', 'w') as t:
    t.write(''.join(line for line in lines))

import pandas as pd 
df = pd.read_table('file_nocomments.txt', header=None)
default_outfmt6_cols = 'qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore'.strip().split(' ')
df.columns = default_outfmt6_cols
df.sort_values(by=["qseqid","bitscore","evalue","pident","sseqid"], ascending=(True,False,False,False,False), inplace=True)
x=df.values.tolist()

j=[]
for i in x:
    j.append([str(i[0]),str(i[1]),str(i[2]),str(i[3]),str(i[4]),str(i[5]),str(i[6]),str(i[7]),str(i[8]),str(i[9]),str(i[10]),str(i[11])])
        
y=[]
for line in j:
    y.append("\t".join(line))


with open('reordered_pDmelpDpse.txt','w') as t:
    for line in y:
        t.write(line + '\n')

