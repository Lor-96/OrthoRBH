import parser
import argparse

def argparserR2():
    parser = argparse.ArgumentParser()
    parser.add_argument('-mgi',type=str , required=True ,metavar='MGI', help='Orthologs predicted by MGI (genenames)')
    parser.add_argument('-odb',type=str , required=True ,metavar='ODB', help='Orthologs predicted by ODB (genenames)')
    parser.add_argument('-bio',type=str , required=True ,metavar='Biomart', help='Orthologs predicted by Biomart (genenames)')
    parser.add_argument('-rbh', type=str, required = True, metavar= 'RBH', help= 'Orthologs gene names from protein RBH')
    parser.add_argument('-exarbh', type = str, required = True, metavar='Exalign_RBH', help= 'Exalign orthologs gene names from RBH')
    parser.add_argument('-cdsrbh', type = str, required = True, metavar='CDS_RBH' , help= 'CDS orthologs gene names from RBH')
    parser.add_argument('-cdsnc', type = str, required=True, metavar='--CDS',  help= 'CDS orthologs gene names not common with the protein RBH')
    args = parser.parse_args()
    params = vars(args)
    return params
