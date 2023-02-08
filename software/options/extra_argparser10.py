import parser
import argparse

def argparserextra10():
    parser = argparse.ArgumentParser()
    parser.add_argument('-rbh1',type=str , required=True ,metavar='--RBH_1', help='RBH of Proteins (one isoform per gene) obtained from main' )
    parser.add_argument('-rbh2',type=str , required=True ,metavar='--RBH_2', help='RBH of Exalign obtained from main')
    parser.add_argument('-rbh3',type=str , required=True ,metavar='--RBH_3', help='RBH of CDS obtained from main')
    parser.add_argument('-gtf1',type=str , required=True , metavar='--GTF1', help='GTF file for species1 ')
    parser.add_argument('-gtf2',type=str , required=True , metavar='--GTF2', help='GTF file for species2')
    args = parser.parse_args()
    params = vars(args)
    return params

