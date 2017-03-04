from lxml import etree
import os
import zipfile

if __name__ == "__main__":

    # namespace from the xml file
    NSMAP = {'hla' : 'http://hla.alleles.org/xml'}
    #    NSMAP = {'hla': 'http://hla.alleles.org/xml'}

#    parser = argparse.ArgumentParser()
#    group = parser.add_mutually_exclusive_group()
#    group.add_argument("-a", "--acc",
#                       help="Accession # of HLA allele",
#                       type=str)
#    group.add_argument("-n", "--name",
#                       help="IMGT/HLA allele name",
#                       type=str)
#    parser.add_argument("-d", "--database",
#                        help="IMGT/HLA version",
#                        type=str,
#                        default="3250")

#    args = parser.parse_args()
#    if args.acc is None and args.name is None:
#        parser.error("at least one of --acc or --name required")

    hlaxmlzip = os.environ['HOME']+'/src/imgthla/'+'3250'+'/xml/hla.xml.zip'
#    print(hlaxmlzip)
#    hlaxmlzip = os.environ['HOME']+'/src/imgthla/'+args.database+'/xml/hla.xml.zip'
#   with zipfile.ZipFile('hlaxmlzip') as myzip:
#   myzip.open('hla.xml') as hlaxml

    zf = zipfile.ZipFile(hlaxmlzip, 'r')
    print(zf.namelist())

    for filename in [ 'hla.xml' ]:
        try:
            data = zf.open(filename)
        except KeyError:
            print('ERROR: Did not find %s in zip file' % filename)
        else:
            print(filename, ':')
        print()

#    hlaxml = 'hla_'+args.database+'.xml'
    tree = etree.parse(data)
    root = tree.getroot() 

