def extra_n9_pipeline(cds1,cds2):
    from software.library.functions import unique_file
    def tablebrowser_cds(path):
        dictionary={}
        d={}
        count=0
        nucleotides=['A','T','G','C']
        with open(path,'r') as file:
            for line in file:
                if line.startswith('>'):
                    name=None
                    count += 1
                    start=line.find('NM_')
                    if start == -1:
                        start=line.find('NP_')
                    end=line.find(' ')
                    name='>'+line[start:end]
                    if name == '>':
                        print(line)
                    st=line.find('chr')
                    en=line.find(':')
                    chrm=line[st:en]
                    if not name in dictionary.keys():
                        dictionary[name]=[]
                        d[name]=[chrm]
                    elif name in d.keys():
                        if not chrm in d.get(name):
                            name=name+'_'+chrm
                            d[name]=[chrm]
                            dictionary[name]=[]
                if any(line.startswith(i.strip()) for i in nucleotides):
                    if name != None:
                        dictionary[name].append(line[:-1].strip())
            for name in dictionary:
                dictionary[name] = '\n'.join(dictionary[name])
                
            lista=[]
            for k,v in dictionary.items():
                lista.append('%s\n%s' % (k.strip(),v.strip(),))
        if len(dictionary) == count:
            return lista
        else:
            return print('Error number of count do not correspond to the number of the cds in the dictionary')

    sp1=tablebrowser_cds(cds1)
    sp2=tablebrowser_cds(cds2)

    with open(unique_file('hg38cds.fa'),'w') as txt1, open(unique_file('mm39cds.fa'),'w') as txt2:
        txt1.write('\n'.join(sp1))
        txt2.write('\n'.join(sp2))
    txt1.close()
    txt2.close()
    return None
