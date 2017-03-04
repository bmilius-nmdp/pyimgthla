from lxml import etree
import argparse
import sys
import os
import zipfile

NSMAP = {'hla' : 'http://hla.alleles.org/xml'}

def getallelename(alleleid, tree):
#    tree = etree.parse(hlaxml)
    name = tree.xpath('//hla:allele[@id=$s]', 
            s=alleleid, 
            namespaces=NSMAP)[0].get('name')
    return name

def getalleleid(allelename, tree):
#    tree = etree.parse(hlaxml)
    id = tree.xpath('//hla:allele[@name=$s]', 
            s=allelename, 
            namespaces=NSMAP)[0].get('id')
    # the following line also works - disadvantage in that the 
    # variable (%s) needs to be quoted 
    # id = tree.xpath('//hla:allele[@name="%s"]'%allelename, 
    #       namespaces=NSMAP)[0].get('id')
    return id

if __name__ == "__main__":

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
#    with zipfile.ZipFile('hlaxmlzip') as myzip:
#        myzip.open('hla.xml') as hlaxml


    zf = zipfile.ZipFile(hlaxmlzip, 'r')
    for filename in [ 'hla.xml' ]:
        try:
            hlaxml = zf.open(filename)
#            print(hlaxml.read())
        except KeyError:
            print('ERROR: Did not find %s in zip file' % filename)
        else:
            print(filename)
        print()

#    hlaxml = 'hla_'+args.database+'.xml'
    tree = etree.parse(hlaxml)
#    root = tree.getroot()
    acc = args.acc
    name = args.name
    if name is None:
#        name = getallelename(acc, hlaxml)
        name = getallelename(acc, tree)
    if acc is None:
#        acc = getalleleid(name, hlaxml)
        acc = getalleleid(name, tree)

    print('....')
    locus = tree.xpath('//hla:allele[@id=$s]/hla:locus', 
            s=acc,
            namespaces=NSMAP)[0].get('hugogenename')
    print('locus =', locus)
    for seq in tree.xpath('//hla:allele[@id=$s]/hla:sequence',
            s=acc,
            namespaces=NSMAP) :
        nseq = seq.xpath('./hla:nucsequence/text()', namespaces=NSMAP)[0]
        print(nseq)
        for f in seq.xpath('./hla:feature[@featuretype="Exon"]', namespaces=NSMAP) :
    #    for f in seq.xpath('./hla:feature[@order]', namespaces=NSMAP) :
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

    # for allele in etree.parse('hla_3230.xml').getroot().findall('hla:allele', NSMAP):
    #    print(allele.get('name'))
        
    # print(getalleleid("HLA-A*01:01:01:01", hlaxml))
