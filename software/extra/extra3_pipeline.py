def extra_n3_pipeline(rbh,orthodb,tab1,tab2,blast1,blast2,perc,bit):
    from software.library.rbh import Rbh
    from software.library.functions import unique_file
    import software.library.ex3fun as ex3f
    import pandas as pd
    import matplotlib.pyplot as plt

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

    num_bins=30

    plt.figure()
    plt.hist(df1['%ID'],num_bins,facecolor='green', alpha=0.5,rwidth=0.8)
    plt.xlabel('% ID')
    plt.ylabel('Frequency')
    plt.title(title1, loc='center')
    plt.savefig(unique_file('Perc_'+title1+'.png'))
    plt.show()

    plt.figure()
    plt.hist(df2['%ID'],num_bins,facecolor='blue', alpha=0.5,rwidth=0.8)
    plt.xlabel('% ID')
    plt.ylabel('Frequency')
    plt.title(title2, loc='center')
    plt.savefig(unique_file('Perc_'+title2+'.png'))
    plt.show()

    plt.figure()
    plt.hist(df3['%ID'],num_bins,facecolor='orange', alpha=0.5, rwidth=0.8)
    plt.xlabel('% ID')
    plt.ylabel('Frequency')
    plt.title(title3, loc='center')
    plt.savefig(unique_file('Perc_'+title3+'.png'))
    plt.show()

    plt.figure()
    plt.hist(df4['%ID'],num_bins,facecolor='red', alpha=0.5, rwidth=0.8)
    plt.xlabel('% ID')
    plt.ylabel('Frequency')
    plt.title(title4, loc='center')
    plt.savefig(unique_file('Perc_'+title4+'.png'))
    plt.show()

    plt.figure()
    plt.hist(df1['alignment length'],num_bins,facecolor='green', alpha=0.5,rwidth=0.8)
    plt.xlabel('Alignment Length')
    plt.ylabel('Frequency')
    plt.title(title1, loc='center')
    plt.savefig(unique_file('Length_'+title1+'.png'))
    plt.show()

    plt.figure()
    plt.hist(df2['alignment length'],num_bins,facecolor='blue', alpha=0.5,rwidth=0.8)
    plt.xlabel('Alignment Length')
    plt.ylabel('Frequency')
    plt.title(title2, loc='center')
    plt.savefig(unique_file('Length_'+title2+'.png'))
    plt.show()

    plt.figure()
    plt.hist(df3['alignment length'],num_bins,facecolor='orange', alpha=0.5, rwidth=0.8)
    plt.xlabel('Alignment Length')
    plt.ylabel('Frequency')
    plt.title(title3, loc='center')
    plt.savefig(unique_file('Length_'+title3+'.png'))
    plt.show()

    plt.figure()
    plt.hist(df4['alignment length'],num_bins,facecolor='red', alpha=0.5, rwidth=0.8)
    plt.xlabel('Alignment Length')
    plt.ylabel('Frequency')
    plt.title(title4, loc='center')
    plt.savefig(unique_file('Length_'+title4+'.png'))
    plt.show()


    '''
    From now this part of the script is focused on making a scatterplot with the
    data obtained from the score and the Best Reciprocal Hit file
    '''

    brh_plt=ex3f.plotbrh(bestrep)
    
    colnames2=["ID","Percentage","BitRatio"]
    df6=pd.DataFrame(brh_plt.values(), columns=colnames2)
    df7=pd.DataFrame(score.values(), columns=colnames2)

    plt.figure()
    plt.scatter(x=df6["BitRatio"],y=df6["Percentage"],marker="o", c='green', alpha=0.2)
    plt.scatter(x=df7["BitRatio"],y=df7["Percentage"],marker="d" , c='darkorange', alpha=0.2)
    plt.title("Percentage VS BitRatio")
    plt.legend(["BRH","Excluded by BRH"])
    plt.xlabel("BitRatio")
    plt.ylabel("Percentage")
    plt.savefig(unique_file('Percentage_VS_BitRatio_both.png'))
    plt.show()

    plt.figure()
    plt.scatter(x=df6["BitRatio"],y=df6["Percentage"],marker="o",c='green', alpha=0.2)
    plt.title("BRH Percentage VS BitRatio")
    plt.xlabel("BitRatio")
    plt.ylabel("Percentage")
    plt.savefig(unique_file('Percentage_VS_BitRatio_BRH.png'))
    plt.show()

    plt.figure()
    plt.scatter(x=df7["BitRatio"],y=df7["Percentage"], marker="d",c='darkorange', alpha=0.2)
    plt.title("Orthologs in OrthoDB but not in BRH \n Percentage VS BitRatio")
    plt.xlabel("BitRatio")
    plt.ylabel("Percentage")
    plt.savefig(unique_file('Percentage_VS_BitRatio_excluded.png'))
    plt.show()