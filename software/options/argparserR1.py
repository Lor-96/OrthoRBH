import argparse

def argparserR1():
    parser = argparse.ArgumentParser()
    parser.add_argument('-mgi',type=str , required=True ,metavar='MGI', help='Orthologs predicted by MGI (genenames)')
    parser.add_argument('-odb',type=str , required=True ,metavar='ODB', help='Orthologs predicted by ODB (genenames)')
    parser.add_argument('-bio',type=str , required=True ,metavar='', help='Orthologs predicted by Biomart (genenames)')
    parser.add_argument('-exa',type=str , required=True ,metavar='', help='Exalign orthologs not common with the protein RBH')
    parser.add_argument('-cds', type = str, required=True, metavar='--CDS',  help= 'CDS orthologs not common with the protein RBH')
    args = parser.parse_args()
    params = vars(args)
    return params
