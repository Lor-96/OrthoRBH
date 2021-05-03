def top2(data):
    file = open(data,'r')
    file= file.readlines()
    mylist=[line.split() for line in file if not line.startswith('#')]
    
    
    d={}
    for idx, line in enumerate(mylist):
        if not line[0] in d.keys():
            nextline = mylist[(idx + 1) % len(mylist)] 
            d.setdefault(line[0], [line[0:],nextline, ((float(line[11]) - float(nextline[11]))/ float(line[11]) ) ])
        elif line[0] in d.keys():
            continue

    d2={}
    for k,v in d.items():
        d2.setdefault(tuple(v[0][0:2]), v[0:])

    return d2



def top2reverse(data):
    file = open(data,'r')
    file= file.readlines()
    mylist=[line.split() for line in file if not line.startswith('#')]
    
    
    d={}
    for idx, line in enumerate(mylist):
        if not line[0] in d.keys():
            nextline = mylist[(idx + 1) % len(mylist)] 
            d.setdefault(line[0], [line[0:],nextline, ((float(line[11]) - float(nextline[11]))/ float(line[11]) ) ])
        elif line[0] in d.keys():
            continue

    d2={}
    for k,v in d.items():
        d2.setdefault(tuple(v[0][0:2][::-1]), v[0:])
    
    return d2




d= top2('Dmel_vs_Dpse.txt')
d2= top2reverse('Dpse_vs_Dmel.txt')

x=top2('Dmel_vs_Dpse2.txt')
y= top2reverse('Dpse_vs_Dmel2.txt')


dset = set(d)
d2set = set(d2)
prova=[]
for k in dset.intersection(d2set):
    prova.append(k)

xset= set(x) 
yset=set(y)
prova2=[]
for k in xset.intersection(yset):
    prova2.append(k)
