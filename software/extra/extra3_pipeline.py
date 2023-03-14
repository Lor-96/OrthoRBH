def extra_n3_pipeline(rbh,orthodb,tab1,tab2,blast1,blast2,perc,bit):
    from software.library.rbh import Rbh
    from software.library.functions import unique_file
    import software.library.ex3fun as ex3f
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    import statistics as st
    import matplotlib.figure as fig

    title1='Excluded by Percentage'
    title2='Excluded by Bitscore Ratio'
    title3='Excluded by Percentage and Bitscore Ratio'
    title4='Not reciprocal'

    bestrep=Rbh(rbh).readrbhpath()
    orthoOdb=ex3f.readODBorthotab(orthodb)
    tab1=ex3f.read_binarytab(tab1,inv=True)
    tab2=ex3f.read_binarytab(tab2,inv=True)

    odb_refseq_tab,common,notcommon,maybeinblast=ex3f.odb_refseq_table(tab1,tab2,orthoOdb,bestrep)

    with open(unique_file('conversiontab_orthoDB_RefSeq.txt') ,'w') as file: 
        for k,v in odb_refseq_tab.items():
            file.write(k.strip()+'\t'+v.strip()+'\n')
    file.close()

    percentage,bitscore, both, notreciprocal_passfilt, notintop, miss, score=ex3f.getexcluded(blast1,blast2,maybeinblast,perc,bit)

    percentage_plt=ex3f.plotbitratio(percentage)
    bitscore_plt=ex3f.plotbitratio(bitscore)
    both_plt=ex3f.plotbitratio(both)
    notreciprocal_passfilt_plt=ex3f.plotbitratio(notreciprocal_passfilt)

    colnames=['Query','Subject','%ID','alignment length','mismatches','gap opens','q.start','q.end','s.start','s.end','evalue','biscore','Bitratio']
    df1=pd.DataFrame(percentage_plt,columns=colnames)
    df2=pd.DataFrame(bitscore_plt,columns=colnames)
    df3=pd.DataFrame(both_plt,columns=colnames)
    df4=pd.DataFrame(notreciprocal_passfilt_plt,columns=colnames)

    def getbinsizeperc(df):
        x=(max(df['%ID']) - min(df['%ID'])+((np.std(df['%ID'])**2)/len(df['%ID']))) / st.mean(df['%ID'])
        return x

    binsizedf1=getbinsizeperc(df1)
    binsizedf2=getbinsizeperc(df2)
    binsizedf3=getbinsizeperc(df3)
    binsizedf4=getbinsizeperc(df4)

    plt.figure(figsize=(10,10))
    plt.hist(df1['%ID'],bins=np.arange(min(df1['%ID']), max(df1['%ID']) + binsizedf1,binsizedf1),facecolor='green', alpha=0.5,rwidth=0.8)
    plt.xlabel('% ID')
    plt.ylabel('Counts')
    plt.title(title1, loc='center')
    plt.savefig(unique_file('Percent_idenitity_distribution_'+title1+'.png'))

    plt.figure(figsize=(10,10))
    plt.hist(df2['%ID'],bins=np.arange(min(df2['%ID']), max(df2['%ID']) + binsizedf2,binsizedf2),facecolor='blue', alpha=0.5,rwidth=0.8)
    plt.xlabel('% ID')
    plt.ylabel('Counts')
    plt.title(title2, loc='center')
    plt.savefig(unique_file('Percent_idenitity_distribution_'+title2+'.png'))

    plt.figure(figsize=(10,10))
    plt.hist(df3['%ID'],bins=np.arange(min(df3['%ID']), max(df3['%ID']) + binsizedf3,binsizedf3),facecolor='orange', alpha=0.5, rwidth=0.8)
    plt.xlabel('% ID')
    plt.ylabel('Counts')
    plt.title(title3, loc='center')
    plt.savefig(unique_file('Percent_idenitity_distribution_'+title3+'.png'))

    plt.figure(figsize=(10,10))
    plt.hist(df4['%ID'],bins=np.arange(min(df4['%ID']), max(df4['%ID']) + binsizedf4,binsizedf4),facecolor='red', alpha=0.5, rwidth=0.8)
    plt.xlabel('% ID')
    plt.ylabel('Counts')
    plt.title(title4, loc='center')
    plt.savefig(unique_file('Percent_idenitity_distribution_'+title4+'.png'))

    def getbinsizealign(df):
        z=st.mean(df['alignment length'])
        x=((max(df['alignment length']) - min(df['alignment length']))+((np.std(df['alignment length'])**2)/len(df['alignment length']))) / z
        return x

    binsizedf1=getbinsizealign(df1)
    binsizedf2=getbinsizealign(df2)
    binsizedf3=getbinsizealign(df3)
    binsizedf4=getbinsizealign(df4)

    plt.figure(figsize=(10,10))
    plt.hist(df1['alignment length'],bins=np.arange(min(df1['alignment length']), max(df1['alignment length']) + binsizedf1,binsizedf1),facecolor='green', alpha=0.5,rwidth=0.8)
    plt.xlabel('Alignment Length')
    plt.ylabel('Counts')
    plt.title(title1, loc='center')
    plt.savefig(unique_file('Length_of_'+title1+'.png'))

    plt.figure(figsize=(10,10))
    plt.hist(df2['alignment length'],bins=np.arange(min(df2['alignment length']), max(df2['alignment length']) + binsizedf2,binsizedf2),facecolor='blue', alpha=0.5,rwidth=0.8)
    plt.xlabel('Alignment Length')
    plt.ylabel('Counts')
    plt.title(title2, loc='center')
    plt.savefig(unique_file('Length_of_'+title2+'.png'))

    plt.figure(figsize=(10,10))
    plt.hist(df3['alignment length'],bins=np.arange(min(df3['alignment length']), max(df3['alignment length']) + binsizedf3,binsizedf3),facecolor='orange', alpha=0.5, rwidth=0.8)
    plt.xlabel('Alignment Length')
    plt.ylabel('Counts')
    plt.title(title3, loc='center')
    plt.savefig(unique_file('Length_of_'+title3+'.png'))

    plt.figure(figsize=(10,10))
    plt.hist(df4['alignment length'],bins=np.arange(min(df4['alignment length']), max(df4['alignment length']) + binsizedf4,binsizedf4),facecolor='red', alpha=0.5, rwidth=0.8)
    plt.xlabel('Alignment Length')
    plt.ylabel('Counts')
    plt.title(title4, loc='center')
    plt.savefig(unique_file('Length_of_'+title4+'.png'))

    '''
    From now this part of the script is focused on making a scatterplot with the
    data obtained from the score and the Best Reciprocal Hit file
    '''

    brh_plt=ex3f.plotbrh(bestrep)

    colnames2=["ID","Percentage","BitRatio"]
    df6=pd.DataFrame(brh_plt.values(), columns=colnames2)
    df7=pd.DataFrame(score.values(), columns=colnames2)

    plt.figure(figsize=(10,10))
    plt.scatter(x=df6["BitRatio"],y=df6["Percentage"],marker="o", c='green', alpha=0.2)
    plt.scatter(x=df7["BitRatio"],y=df7["Percentage"],marker="d" , c='darkorange', alpha=0.2)
    plt.title("Percentage VS BitRatio")
    plt.legend(["RBH","Excluded by RBH"], bbox_to_anchor=(0.2, -0.05))
    plt.xlabel("BitRatio")
    plt.ylabel("Percentage")
    plt.savefig(unique_file('Percentage_VS_BitRatio_both.png'))

    plt.figure(figsize=(10,10))
    plt.scatter(x=df6["BitRatio"],y=df6["Percentage"],marker="o",c='green', alpha=0.2)
    plt.title("RBH Percentage VS BitRatio")
    plt.xlabel("BitRatio")
    plt.ylabel("Percentage")
    plt.savefig(unique_file('Percentage_VS_BitRatio_RBH.png'))

    plt.figure(figsize=(10,10))
    plt.scatter(x=df7["BitRatio"],y=df7["Percentage"], marker="d",c='darkorange', alpha=0.2)
    plt.title("Orthologs in OrthoDB but not in RBH \n Percentage VS BitRatio")
    plt.xlabel("BitRatio")
    plt.ylabel("Percentage")
    plt.savefig(unique_file('Percentage_VS_BitRatio_excluded.png'))
