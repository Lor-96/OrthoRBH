def checkhit(data, dictionary):

    def get_key(val):
        for key, value in dict2.items():
            for x in value:
                if val == x:
                    return key

    d={}
    line=''
    with open("reordered_pDmelpDpse.txt", 'r') as infile:
        Line = infile.readlines()
        for li in Line:
            if not li.startswith('#'):
                line= li.split()
                if not line[0] in d.keys():
                    d.setdefault(line[0], [line])
                else:
                    for v in d.values():
                        if line[0] == v[0][0]:
                            if not len(v)== 2:
                                if get_key(line[1]) != get_key(v[0][1]):
                                    d[line[0]].append(line)

        for k,v in  d.items():
            if not len(v)==2:
                if len(v) == 1:
                    v.append(float(v[0][11])/float(v[0][11]))
            else:
                if not len(v)== 3:
                    v.append((float(v[0][11]) - float(v[1][11]))/float(v[0][11]))



    d2={}
    for k,v in d.items():
        d2.setdefault(tuple(v[0][0:2]), v[0:])

    return d2
