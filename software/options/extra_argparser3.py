import parser
import argparse

def argparserextra3():
    import parser
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-rbh',type=str , required=True ,metavar='--RBH', help='RBH file')
    parser.add_argument('-odb',type=str , required=True ,metavar='--OrthoDB', help='OrthoDB Orthologs file')
    parser.add_argument('-t1',type=str , required=True ,metavar='--Tab_sp1', help='Species 1 table from extra_2')
    parser.add_argument('-t2',type=str , required=True , metavar='--Tab_sp2', help='Species 2 table from extra_2')
    parser.add_argument('-b1',type=str , required=True ,metavar='--blast1', help='Blast result for Species 1 vs Species 2' )
    parser.add_argument('-b2',type=str , required=True , metavar='--blast2' ,help='Blast result for Species 2 vs Species 1' )
    parser.add_argument('-perc', type=str, required=True , metavar = '--percentage', help='Same percentage threshold for the RBH' )
    parser.add_argument('-bit', type=str, required = True , metavar='--bitscore',help='Same bitscore threshold for the RBH')
    args = parser.parse_args()
    params = vars(args)
    return params