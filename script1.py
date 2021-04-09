def blastab7(data):
    file = open(data,'r')
    file= file.readlines()
    mylist=[line.split() for line in file if not line.startswith('#')]
    d={}
    for line in mylist:
        if not line[0] in d.keys():
            d.setdefault(line[0],line[1:])
        elif line[0] in d.keys():
            continue
    d={(k, v[0]) : v[1:] for k, v in d.items() }
    return d

d=blastab7('melanogaster_vs_pseudobscura.txt')
d2= blastab7('pseudobscura_vs_melanogaster.txt')

