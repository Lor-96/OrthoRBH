import parser
import argparse

def argparser():
    import parser
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-b1',type=str , required=True ,metavar='--blast1', help='Blast result for Species 1 vs Species 2' )
    parser.add_argument('-b2',type=str , required=True , metavar='--blast2' ,help='Blast result for Species 2 vs Species 1' )
    parser.add_argument('-gtf1',type=str , required = True, metavar='--gtf1' , help='GTF file for Species 1' )
    parser.add_argument('-gtf2', type=str , required = True, metavar='--gtf2',help='GTF file for Species 2')
    parser.add_argument('-perc', type=str, required=True , metavar = '--percentage', help='Threshold for the percentage of identity' )
    parser.add_argument('-bit', type=str, required = True , metavar='--bitscore',help='Threshold for the Bitscore')
    parser.add_argument('-ev',type=str, required = False , default= '0.001' ,metavar='--pvalue',help='Exalign Threshold for the pvalue')
    parser.add_argument('-sc',type=str, required = False, default='0', metavar='--score',help='Exalign threshold for the score')
    parser.add_argument('-tr', type=bool, required = False, default=False, metavar='--transcript', help= 'Set it as "True" if in the BLAST there are transcripts instead of proteins')
    args = parser.parse_args()
    params = vars(args)
    return params
