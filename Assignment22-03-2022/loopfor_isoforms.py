with open('Orthomelall_DB_vs_proteinDmel.txt','r') as odbvsdmel:
    d={}
    for line in odbvsdmel:
        if not line.startswith('#'):
            l=line.split()
            if not l[0] in d.keys():
                d.setdefault(l[0], []).append([l[1:3],l[11]])

cento={}
for k,v in d.items():
    if float(v[0][0][1]) == 100.000:
        cento.setdefault(k,[v[0][0][0],v[0][0][1],v[0][1]])
    
invcent={}
for k,v in cento.items():
    invcent.setdefault(v[0],set()).add(k)

def floatorint(string):
    if string.isdigit() == True :
        return int(string)
    elif string.isdigit() == False :
        return float(string)

noisomel={}
for k,v in cento.items():
    if len(invcent.get(str(v[0]))) == 1:
        noisomel.setdefault(k,v)
    if len(invcent.get(str(v[0]))) > 1:
        l= list(invcent.get(str(v[0])))
        sublist=[]
        for i in l:
            sublist.append(cento.get(str(i)))
            sublist=[[j[0],j[1],floatorint(str(j[2]))] for j in sublist]
            max_v= max(sublist)
            max_v= ['% s' % m for m in max_v]
        noisomel.setdefault(list(cento.keys())[list(cento.values()).index(max_v)],max_v)
