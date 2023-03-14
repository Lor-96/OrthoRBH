import parser
import argparse

def argparserextra7():
    import parser
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-faa1',type=str , required=True ,metavar='--FAA1', help='FAA file containing the peptide sequences of the single isoform per gene fpr the species 1')
    parser.add_argument('-faa2',type=str , required=True ,metavar='--FAA2', help='FAA file containing the peptide sequences of the single isoform per gene fpr the species 2')
    parser.add_argument('-gtf1',type=str , required=True ,metavar='--gtf_species1', help='FILE GTF FOR SPECIES 1' )
    parser.add_argument('-gtf2',type=str , required=True ,metavar='--gtf_species2', help='FILE GTF FOR SPECIES 2' )
    parser.add_argument('-g1', type=str , required=True ,metavar='--genome_species1', help='GENOME SPECIES 1')
    parser.add_argument('-g2',type=str , required=True ,metavar='--genome_species2', help='GENOME SPECIES 2' )
    parser.add_argument('-l', type = bool, required=True, metavar='--logical', help='True for the CDS False for the UTR')
    args = parser.parse_args()
    params = vars(args)
    return params