import parser
import argparse

def argparser():
    import parser
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-b1',type=str , required=True , help='Blast result for Species 1 vs Species 2' )
    parser.add_argument('-b2',type=str , required=True , help='Blast result for Species 2 vs Species 1' )
    parser.add_argument('-gtf1',type=str , required = True, help='GTF file for Species 1' )
    parser.add_argument('-gtf2', type=str , required = True, help='GTF file for Species 2')
    parser.add_argument('-perc', type=str, required=True , help='Threshold for the percentage of identity' )
    parser.add_argument('-bit', type=str, required = True , help='Threshold for the Bitscore')
    args = parser.parse_args()
    params = vars(args)
    return params
