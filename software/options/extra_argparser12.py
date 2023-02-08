import parser
import argparse

def argparserextra12():
    import parser
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-rbh',type=str , required=True ,metavar='-RBH Proteins', help='Orthologs predicted by OrthoRBH (genenames) from RBH for proteins')
    parser.add_argument('-mgi',type=str , required=True ,metavar='MGI', help='Orthologs predicted by MGI (genenames)')
    parser.add_argument('-odb',type=str , required=True ,metavar='ODB', help='Orthologs predicted by ODB (genenames)')
    parser.add_argument('-bio',type=str , required=True ,metavar='', help='Orthologs predicted by Biomart (genenames)')
    parser.add_argument('-exa',type=str , required=True ,metavar='', help='Orthologs predicted by Exalign-OrthoRBH (genenames) from RBH')
    parser.add_argument('-gtf1',type=str , required=True , metavar='--GTF1', help='GTF file for species1 ')
    parser.add_argument('-gtf2',type=str , required=True , metavar='--GTF2', help='GTF file for species2')
    args = parser.parse_args()
    params = vars(args)
    return params