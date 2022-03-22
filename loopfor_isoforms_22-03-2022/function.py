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
