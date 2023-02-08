import parser
import argparse

def argparserextra9():
    import parser
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-cds1',type=str , required=True , metavar='--cds species1', help='CDS for species 1 from Table Browser more isoform per gene')
    parser.add_argument('-cds2',type=str , required=True , metavar='--cds species2', help='CDS for species 2 from Table Browser more isoform per gene')
    args = parser.parse_args()
    params = vars(args)
    return params