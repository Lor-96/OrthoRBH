import parser
import argparse

def argparserextra7():
    import parser
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-bl1',type=str , required=True ,metavar='--BLAST1', help='BLAST of species 1 vs species 2 oneisoform per gene')
    parser.add_argument('-bl2',type=str , required=True ,metavar='--BLAST2', help='BLAST of species 2 vs species 1 oneisoform per gene')
    parser.add_argument('-gtf1',type=str , required=True ,metavar='--gtf_species1', help='FILE GTF FOR SPECIES 1' )
    parser.add_argument('-gtf2',type=str , required=True ,metavar='--gtf_species2', help='FILE GTF FOR SPECIES 2' )
    parser.add_argument('-g1', type=str , required=True ,metavar='--genome_species1', help='GENOME FOR SPECIES 1')
    parser.add_argument('-g2',type=str , required=True ,metavar='--genome_species2', help='GENOME FOR SPECIES 2' )
    parser.add_argument('-l', type = bool, required=True, metavar='--logical', help='True for the CDS False for the UTR')
    args = parser.parse_args()
    params = vars(args)
    return params