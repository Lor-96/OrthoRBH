def top2(data):
    file = open(data,'r')
    file= file.readlines()
    mylist=[line.split() for line in file if not line.startswith('#')]
    
    
    d={}
    for idx, line in enumerate(mylist):
        if not line[0] in d.keys():
            nextline = mylist[(idx + 1) % len(mylist)] 
            d.setdefault(line[0],[line[0:],nextline, ((float(line[11]) - float(nextline[11]))/ float(line[11]) ) ])
        elif line[0] in d.keys():
            continue
    
    

    return d

x= top2('Dmel_vs_Dpse.txt')
y= top2('Dpse_vs_Dmel.txt')

x2=top2('Dmel_vs_Dpse2.txt')
y2= top2('Dpse_vs_Dmel2.txt')
