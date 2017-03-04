#! /Users/bmilius/.virtualenvs/p3/bin/python3
from lxml import etree
import argparse


def getallelename(alleleid, hlaxml):
    #    tree = etree.parse(hlaxml)
    NSMAP = {'hla': 'http://hla.alleles.org/xml'}
    name = tree.xpath('//hla:allele[@id=$s]',
                      s=alleleid,
                      namespaces=NSMAP)[0].get('name')
    return name


def getalleleid(allelename, hlaxml):
    #    tree = etree.parse(hlaxml)
    NSMAP = {'hla': 'http://hla.alleles.org/xml'}
    id = tree.xpath('//hla:allele[@name=$s]',
                    s=allelename,
                    namespaces=NSMAP)[0].get('id')
    # the following line also works - disadvantage in that the
    # variable (%s) needs to be quoted
    # id = tree.xpath('//hla:allele[@name="%s"]'%allelename,
    #       namespaces=NSMAP)[0].get('id')
    return id


def getlocus(alleleid, hlaxml):
    #    tree = etree.parse(hlaxml)
    NSMAP = {'hla': 'http://hla.alleles.org/xml'}
    locus = tree.xpath('//hla:allele[@id=$s]/hla:locus',
                       s=alleleid,
                       namespaces=NSMAP)[0].get('hugogenename')
    return locus


def getnucseq(alleleid, hlaxml):
    #    tree = etree.parse(hlaxml)
    NSMAP = {'hla': 'http://hla.alleles.org/xml'}
    seq = tree.xpath('//hla:allele[@id=$s]/hla:sequence',
                     s=acc,
                     namespaces=NSMAP)[0]
    nucseq = seq.xpath('./hla:nucsequence/text()', namespaces=NSMAP)[0]
    return nucseq


if __name__ == "__main__":
    #    NSMAP = {'hla': 'http://hla.alleles.org/xml'}

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
    if args.acc is None and args.name is None:
        parser.error("at least one of --acc or --name required")

    hlaxml = 'hla_'+args.database+'.xml'
    tree = etree.parse(hlaxml)
#    root = tree.getroot()

    acc = args.acc
    name = args.name
    if name is None:
        name = getallelename(acc, hlaxml)
    if acc is None:
        acc = getalleleid(name, hlaxml)

    nseq = getnucseq(acc,hlaxml)

    print('IMGT/HLA XML file =', hlaxml)
    print('locus =', getlocus(acc, hlaxml))
    print('name =', name)
    print('acc =', acc)
    print('sequence length = ', len(nseq))
    print(nseq)

# for seq in tree.xpath('//hla:allele[@id=$s]/hla:sequence',
#        s=acc,
#        namespaces=NSMAP):
#    nseq = seq.xpath('./hla:nucsequence/text()', namespaces=NSMAP)[0]
#    print(nseq)

#    for f in seq.xpath('./hla:feature[@featuretype="Exon"]', namespaces=NSMAP):
# #    for f in seq.xpath('./hla:feature[@order]', namespaces=NSMAP):
#        print('exon =', f.get('id'), '\tname =',f.get('name'),'\torder =',f.get('order'),'\tstatus =',f.get('status'))
#        rank=f.get('name').split()[1]
#        if rank == args.exon:
#            print('exon =', f.get('id'), '\tname =',f.get('name'),'\torder =',f.get('order'),'\tstatus =',f.get('status'))
#            term=f.get('featuretype').lower()
#            print('\trank =',rank)
#            print('\tterm =',term)
#            for coor in f.xpath('./hla:SequenceCoordinates', namespaces=NSMAP):
#                seqstart=int(coor.get('start'))-1
#                seqend=int(coor.get('end'))
#    #            print('0-base [ )','\tstart =',seqstart,'\tend =', seqend)
#                print('0-base','\t[',seqstart,',',seqend,')')
#    #            print('1-base [ ]','\tstart =',coor.get('start'),'\tend =', coor.get('end'))
#                print('1-base','\t[',coor.get('start'),',',coor.get('end'),']')
#                sequence=nseq[seqstart:seqend]
#                print(nseq[seqstart:seqend])
#    #            print(sequence)
#                print('\n','...')

# for allele in etree.parse('hla_3230.xml').getroot().findall('hla:allele', NSMAP):
#    print(allele.get('name'))
