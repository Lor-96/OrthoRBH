import argparse

def argparserextra5():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-b',type=str , required=True , metavar='--biomart_orthologs', help='FILE DOWNLOADED FROM BIOMART WITH ORTHOLOGS' )
    parser.add_argument('-p',type=bool , required=True, metavar='--predicted', help='TRUE IF THE BIOMART EXPORT FILE CONTAINS THE PREDICTED ID ELSE FALSE')
    parser.add_argument('-gtf1',type=str , required=True ,metavar='--gtf_species1', help='FILE GTF FOR SPECIES 1' )
    parser.add_argument('-gtf2',type=str , required=True ,metavar='--gtf_species2', help='FILE GTF FOR SPECIES 2' )
    parser.add_argument('-t1',type=str , required=True ,metavar='--Tab_sp1', help='Species 1 table from extra_2')
    parser.add_argument('-t2',type=str , required=True , metavar='--Tab_sp2', help='Species 2 table from extra_2')
    parser.add_argument( '-bt1', type = str, required = True, metavar='--Biomart_species1' , help='Biomart_Table_species1')
    parser.add_argument( '-bt2', type = str, required = True, metavar='--Biomart_species2' , help='Biomart_Table_species2')
    parser.add_argument('-c',  type = bool, required = True, metavar ='Change_gene_names' , help = 'Set it to True to use the GTF Gene names')
    args = parser.parse_args()
    params = vars(args)
    return params