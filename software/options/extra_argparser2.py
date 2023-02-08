#extra_argparser2
import parser
import argparse

def argparserextra2():
    import parser
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-bl1',type=str , required=True ,metavar='--BLAST1', help='BLAST of species 1 ODB vs species 1 RefSeq')
    parser.add_argument('-bl2',type=str , required=True ,metavar='--BLAST2', help='BLAST of species 2 ODB vs species 2 RefSeq')
    parser.add_argument('-tx1',type=str , required=True ,metavar='--taxid_species1', help='Tax ID species 1 from ODB level.tab' )
    parser.add_argument('-tx2',type=str , required=True ,metavar='--taxid_species2', help='Tax ID species 2 from ODB level.tab' )
    parser.add_argument('-fa1',type=str , required=True ,metavar='--faa_species1', help='Protein FASTA from RefSeq species 1' )
    parser.add_argument('-fa2',type=str , required=True ,metavar='--faa_species2', help='Protein FASTA from RefSeq species 2')
    parser.add_argument('-perc1',type=str , required=True ,metavar='--PERC1', help='Percentage species 1')
    parser.add_argument('-perc2',type=str , required=True ,metavar='--PERC2', help='Percentage species 2')
    parser.add_argument('-ofa1', type=str, required = True, metavar='--ODB_faa_species1', help='ODB Protein FASTA species1' )
    parser.add_argument('-ofa2', type=str, required = True, metavar='--ODB_faa_species2', help='ODB Protein FASTA species2' )
    parser.add_argument('-sw1', type=bool,default=False, required = False, metavar='--switch1', help='True if you want to switch the sequences of RefSeq with the ODB ones for species1' )
    parser.add_argument('-sw2', type=bool,default=False, required = False, metavar='--switch2', help='True if you want to switch the sequences of RefSeq with the ODB ones for species2' )
    args = parser.parse_args()
    params = vars(args)
    return params
