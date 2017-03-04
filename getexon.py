#! /Users/bmilius/.virtualenvs/p3/bin/python3
from lxml import etree
import uuid
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--acc", help="Accession # of HLA allele", type=str)
parser.add_argument("-e", "--exon", help="Exon rank", type=str)

args = parser.parse_args()

hlaxml = 'hla_3250.xml'
tree = etree.parse(hlaxml)
root = tree.getroot()

#acc = 'HLA00381'
acc = args.acc

# namespace from the xml file 
NSMAP = {'hla' : 'http://hla.alleles.org/xml'}

def getallelename(alleleid, hlaxml):
    tree = etree.parse(hlaxml)
    NSMAP = {'hla' : 'http://hla.alleles.org/xml'}
    name = tree.xpath('//hla:allele[@id=$s]', 
            s=alleleid, 
            namespaces=NSMAP)[0].get('name')
    return name

def getalleleid(allelename, hlaxml):
    tree = etree.parse(hlaxml)
    NSMAP = {'hla' : 'http://hla.alleles.org/xml'}
    id = tree.xpath('//hla:allele[@name=$s]', 
            s=allelename, 
            namespaces=NSMAP)[0].get('id')
    # the following line also works - disadvantage in that the 
    # variable (%s) needs to be quoted 
    # id = tree.xpath('//hla:allele[@name="%s"]'%allelename, 
    #       namespaces=NSMAP)[0].get('id')
    return id


print('....')
locus = tree.xpath('//hla:allele[@id=$s]/hla:locus', 
        s=acc,
        namespaces=NSMAP)[0].get('hugogenename')
#print('locus =', locus)
print('name =', getallelename(acc, hlaxml))
for seq in tree.xpath('//hla:allele[@id=$s]/hla:sequence',
        s=acc,
        namespaces=NSMAP) :
    nseq = seq.xpath('./hla:nucsequence/text()', namespaces=NSMAP)[0]
#    print(nseq)
    for f in seq.xpath('./hla:feature[@featuretype="Exon"]', namespaces=NSMAP) :
#    for f in seq.xpath('./hla:feature[@order]', namespaces=NSMAP) :
#        print('exon =', f.get('id'), '\tname =',f.get('name'),'\torder =',f.get('order'),'\tstatus =',f.get('status'))
        rank=f.get('name').split()[1]
        if rank == args.exon : 
            print('exon =', f.get('id'), '\tname =',f.get('name'),'\torder =',f.get('order'),'\tstatus =',f.get('status'))
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

# for allele in etree.parse('hla_3230.xml').getroot().findall('hla:allele', NSMAP):
#    print(allele.get('name'))
    
# print(getalleleid("HLA-A*01:01:01:01", hlaxml))
