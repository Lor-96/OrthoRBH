def top2(data):
    file = open(data,'r')
    file= file.readlines()
    mylist=[line.split() for line in file if not line.startswith('#')]
    
    
    d={}
    for line in mylist:
        if not line[0] in d.keys():
            d.setdefault(line[0],[line[1:]])
        elif line[0] in d.keys():
            d[line[0]].append(line[1:])
    
    d2={}
    for k,v in d.items():
        if len(v) > 1:
            d2.setdefault(k, [v[0] , v[1]])
        elif len(v) == 1:
            d2.setdefault(k, v)
    
    d3={}
    
    for k,v in d2.items():        
        if len(v) > 1:
            if v[0][0]==v[1][0]:
                for i in v:
                    d3.setdefault((k,v[0][0]), []).append(i[0:])
            elif v[0][0] != v[1][0]:
                for i in v:
                    d3.setdefault((k,i[0]),i[0:])
        elif len(v) == 1:
            d3.setdefault((k,v[0][0]),v[0][0:])
    
    return d3

x= top2('melanogaster_vs_pseudobscura.txt')

