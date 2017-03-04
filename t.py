from lxml import etree


def printnodeinfo(alleleid):
    '''printing some info about what xpath returns'''
    path='//hla:allele[@id="' + alleleid + '"]' 
    allelenodes = TREE.xpath(path, namespaces=NSMAP)
    print(type(allelenodes))
    print('# of alleles with an id of', alleleid, '=', len(allelenodes))

def printnodeinfo2(allelename):
    '''printing some info about what xpath returns'''
    path='//hla:allele[@name="' + allelename + '"]' 
    allelenodes = TREE.xpath(path, namespaces=NSMAP)
    print(type(allelenodes))
    print('# of alleles with a name  of', allelename, '=', len(allelenodes))

def printA():
    ''' prints all alleles that have hugogenename of HLA-A, 
    then prints the number of HLA-A alelles '''
    path = '//hla:allele[hla:locus/@hugogenename="HLA-A"]' 
    allelenodes = TREE.xpath(path, namespaces=NSMAP)
    for node in allelenodes:
        print(node.get('name'))
    print('# of HLA-A alleles =', len(allelenodes))

def countnodes(alleleid):
    ''' prints the number of nodes with a particular alleleid 
    using count() function in xpath, and its type'''
    numnodes = TREE.xpath('count(//hla:allele[@id=$s])', 
            s=alleleid, namespaces=NSMAP)
    print(type(numnodes))
    print(numnodes)

def countloci():
    '''count number of nodes with locusname attribute'''
    name = 'locusname'
    path = '//hla:locus[@'+name+']'
    loci = TREE.xpath(path, namespaces=NSMAP)
    return len(loci)

def featurestatus(status):
    '''lists the alleles containing a feature with the indicated status;
    usually Partial or Complete'''
    #path = '//hla:allele[hla:sequence/hla:feature/@status="' + status + '"]'
    path = '//hla:allele[hla:sequence/hla:feature/@status="' + status + '"]'
    #status='no status'
    #path = '//hla:allele[not(hla:sequence/hla:feature/@status)]'
    alleles = TREE.xpath(path, namespaces=NSMAP)
    for allele in alleles:
        print(allele.get('name'))
    print('# of alleles with '+status+' features =', len(alleles))

    
def listfeatures():
    path = '//hla:feature'
    features = TREE.xpath(path, namespaces=NSMAP)
    featurestatuses = set()
    for feature in features:
        featurestatuses.add(feature.get('status'))
    print(featurestatuses)
    
def getnames(nametype):
    ''' returns a set of all names of loci with attribute of nametype 
    (usually either locusname or hugogenename)'''
    path = '//hla:locus[@' + nametype + ']'
    loci = TREE.xpath(path, namespaces=NSMAP)
    names = set()
    for locus in loci:
        names.add(locus.get(nametype))
    # print('names of', nametype, '=', names)
    # print('# of ', nametype, '=', len(names))
    return names

def listnumalleles():
    '''prints # of alleles for each locus'''
    names=getnames('locusname')
    totalalleles=0
    print('# of alleles:')
    for name in sorted(names):
        path = '//hla:allele[hla:locus/@locusname="' + name + '"]'
        alleles = TREE.xpath(path, namespaces=NSMAP)
        print('\t', name, '=', len(alleles))
        totalalleles=totalalleles+len(alleles)
    print('sum of all alleles:', totalalleles)

def testglobal():
    print(NSMAP.get('hla'))

def main():
    #tree = etree.parse('hlax.xml')
    root = TREE.getroot()
    alleleid = 'HLA00001'
    allelename = 'HLA-A*01:01:01:01'
    printnodeinfo(alleleid)
    printnodeinfo2(allelename)
    # print('number of nodes with locusname attribute:', countloci())
    listnumalleles()
    #printA()
    # testglobal()
    #print('alleles with partial status features') 
    #featurestatus('Partial')
    #listfeatures()

if __name__ == "__main__":
    TREE  = etree.parse('hla_3220.xml')
    NSMAP = {'hla' : 'http://hla.alleles.org/xml'}
    main()
