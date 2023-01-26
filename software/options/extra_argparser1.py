import parser
import argparse

def argparserextra1():
    import parser
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-tx1',type=str , required=True ,metavar='--taxid_species1', help='TAX ID OF THE FIRST SPECIES')
    parser.add_argument('-tx2',type=str , required=True ,metavar='--taxid_species2', help='TAX ID OF THE SECOND SPECIES')
    parser.add_argument('-lvl',type=str , required=True ,metavar='--level', help='LEVEL OF ANALYSIS BETWEEN THE 2 SPECIES PRECEDED BY "at" I.E. DROSOPHILIDAE = at7214' )
    parser.add_argument('-gtf1',type=str , required=True ,metavar='--gtf_species1', help='FILE GTF FOR SPECIES 1' )
    parser.add_argument('-gtf2',type=str , required=True ,metavar='--gtf_species2', help='FILE GTF FOR SPECIES 2' )
    parser.add_argument('-af',type=str , required=True ,metavar='--all_fasta', help='PATH TO THE ALL_FASTA FILE OF ORTHODB')
    parser.add_argument('-og2g',type=str , required=True ,metavar='--OG2genes', help='PATH TO THE OG2_GENES.TAB FILE OF ORTHODB')
    parser.add_argument('-gen',type=str , required=True ,metavar='--genes', help='PATH TO THE GENES.TAB FILE OF ORTHODB')
    args = parser.parse_args()
    params = vars(args)
    return params

