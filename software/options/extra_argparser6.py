import argparse

def argparserextra6():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-mgi',type=str , required=True ,metavar='--mgi_homologs', help='Homologous table from MGI site' )
    parser.add_argument('-t1',type=str , required=True ,metavar='--Tab_sp1', help='Species 1 table from extra_2')
    parser.add_argument('-t2',type=str , required=True , metavar='--Tab_sp2', help='Species 2 table from extra_2')    
    args = parser.parse_args()
    params = vars(args)
    return params