import argparse

def argparserextra4():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-gtf1',type=str , required=True ,metavar='--gtf_species1', help='FILE GTF FOR SPECIES 1' )
    parser.add_argument('-gtf2',type=str , required=True ,metavar='--gtf_species2', help='FILE GTF FOR SPECIES 2' )
    parser.add_argument('-t', type=str, required= True, metavar='--table', help='ODB-REFSEQ TABLE OBTAINED AS OUTPUT IN EXTRA SCRIPT 3 ')
    args = parser.parse_args()
    params = vars(args)
    return params