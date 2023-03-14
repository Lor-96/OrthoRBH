import parser
import argparse

def argparserextra11():
    import parser
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-bl1',type=str , required=True ,metavar='--BLAST1', help='CDS BLAST of species 1 vs species 2 multiple isoforms')
    parser.add_argument('-bl2',type=str , required=True ,metavar='--BLAST2', help='CDS BLAST of species 2 vs species 1 multiple isoforms')
    parser.add_argument('-ext1',type=str,required=True,metavar='--exaligntab1',help='Exalign table result for species1')
    parser.add_argument('-ext2',type=str,required=True,metavar='--exaligntab2',help='Exalign table result for species2')
    parser.add_argument('-rbh1',type=str , required=True ,metavar='--RBH_1', help='RBH of CDS obtained from main' )
    parser.add_argument('-rbh2',type=str , required=True ,metavar='--RBH_2', help='RBH of Exalign obtained from main')
    parser.add_argument('-perc', type=str, required=True , metavar = '--percentage', help='Same percentage threshold for the RBH' )
    parser.add_argument('-bit', type=str, required = True , metavar='--bitscore',help='Same bitscore threshold for the RBH')
    parser.add_argument('-exm',type=str,required=True,metavar='--exonmatch',help='Exon match threshold set for the RBH')
    parser.add_argument('-sc',type=str,required=True,metavar='--score',help='Score threshold set for the RBH')
    parser.add_argument('-pval',type=str,required=False, default= 0.001, metavar='--PVALUE',help='Pvalue threshold set for the RBH together with the score (not mandatory default = 0.001)')
    parser.add_argument('-score',type=str,required=False, default = 0, metavar='--score', help='Score threshold set for the RBH together with the pvalue (not mandatory default = 0)')
    args = parser.parse_args()
    params = vars(args)
    return params