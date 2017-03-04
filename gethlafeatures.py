from lxml import etree
import argparse
import sys
import os
import zipfile

# namespace from the xml file
NSMAP = {'hla' : 'http://hla.alleles.org/xml'}

def getallelename(alleleid, tree):
    name = tree.xpath('//hla:allele[@id=$s]',
            s=alleleid,
            namespaces=NSMAP)[0].get('name')
    return name


def getalleleid(allelename, tree):
    alleleid = tree.xpath('//hla:allele[@name=$s]',
            s=allelename,
            namespaces=NSMAP)[0].get('id')
    return alleleid

def get_exons(alleleid, tree):
    pass

def get_feature(alleleid, feature, tree):
    pass

def total_num_of_alleles(tree):
    pass

def count_loci(tree):
    pass


def count_alleles(tree):
    pass

def count_alleles_per_locus(tree):
    pass




def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a", "--acc",
                       help="Accession # of HLA allele",
                       type=str)
    group.add_argument("-n", "--name",
                       help="IMGT/HLA allele name",
                       type=str)
    parser.add_argument("-d", "--database",
                        help="IMGT/HLA version",
                        type=str,
                        default="3250")

    args = parser.parse_args()
    if (args.acc is None) and (args.name is None):
        parser.error("at least one of --acc or --name required")

    hlaxmlzip = os.environ['HOME']+'/src/imgthla/'+args.database+'/xml/hla.xml.zip'

    zf = zipfile.ZipFile(hlaxmlzip, 'r')
    for filename in [ 'hla.xml' ]:
        try:
            hlaxml = zf.open(filename)
        except KeyError:
            print('ERROR: Did not find %s in zip file' % filename)
#        else:
#            print(filename)
        print()

    tree = etree.parse(hlaxml)
    acc = args.acc
    name = args.name
    if name is None:
        name = getallelename(acc, tree)
    if acc is None:
        acc = getalleleid(name, tree)

    print('....')
    locus = tree.xpath('//hla:allele[@id=$s]/hla:locus',
            s=acc,
            namespaces=NSMAP)[0].get('hugogenename')
    print('locus =', locus)
    print('acc = ', acc)
    print('name = ', name)
    for seq in tree.xpath('//hla:allele[@id=$s]/hla:sequence',
            s=acc,
            namespaces=NSMAP) :
        nseq = seq.xpath('./hla:nucsequence/text()', namespaces=NSMAP)[0]
        print(nseq)
        for f in seq.xpath('./hla:feature[@order]', namespaces=NSMAP) :
            print('exon =', f.get('id'), '\tname =',f.get('name'),'\torder =',f.get('order'),'\tstatus =',f.get('status'))
            rank=f.get('name').split()[1]
            term=f.get('featuretype').lower()
            print('\trank =',rank)
            print('\tterm =',term)
            for coor in f.xpath('./hla:SequenceCoordinates', namespaces=NSMAP) :
                seqstart=int(coor.get('start'))-1
                seqend=int(coor.get('end'))
    #            print('0-base [ )','\tstart =',seqstart,'\tend =', seqend)
                print('0-base','\t[',seqstart,',',seqend,')')
    #            print('1-base [ ]','\tstart =',coor.get('start'),'\tend =', coor.get('end'))
                print('1-base','\t[',coor.get('start'),',',coor.get('end'),']')
                sequence=nseq[seqstart:seqend]
                print(nseq[seqstart:seqend])
    #            print(sequence)
                print('\n','...')

if __name__ == "__main__":

