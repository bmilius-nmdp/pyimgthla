#! /bin/bash
# download IMGT/HLA xml and fasta files

for i in 300 310 3100 3110 3120 3130 3140 3150 3160 3170 3180 3190 320 3200 3210 3220 3230 3240 3250 3260 330 340 350 360 370 380 390; do
    cd $i
#    svn checkout https://github.com/ANHIG/IMGTHLA/branches/${i}/xml
    svn checkout https://github.com/ANHIG/IMGTHLA/branches/${i}/fasta --depth empty
    cd fasta
    svn up hla_gen.fasta hla_nuc.fasta hla_prot.fasta
#    svn up hla_nuc.fasta
#    svn up hla_prot.fasta
    cd ../..
done

