# This folder contains human reference genome files and pMEI identified from other databases used for generating novel variants in step C

To generate human reference genome files:
1. Download chromOut.tar.gz from <http://hgdownload.soe.ucsc.edu/goldenPath/hg19/bigZips/>
2. zcat chromOut.tar.gz >hg19.fa.out
3. awk '{print $5"\t"$6"\t"$7"\t"$9"\t"$10"\t"$11}' hg19.fa.out > hg19.fa.bed

To generate variants files from Stewart et al. 2011 dataset:
1. Download Table S1. from <http://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1002236#s5>
2. Open Excel file and Save as Tab Delimited (.txt) "journal.pgen.1002236.s019.txt"

To generate variants files from 1000 genome project phase 3:
1. Download <ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/integrated_sv_map/ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.vcf.gz>
2. gzip -d ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.vcf.gz

The files "dbrip_Alu_hg19_v2h.txt" and "dbrip_SVA_hg19_v2h.txt" will be used to remove variants identified in dbRIP

The file "ALL.wgs.integrated_sv_map_v2.20130502.svs.genotypes.individuals.list" will be used to provide list of individuals in 1000 genome project

The file "Reference_*_blastn-short.bed" will be used to generate reference MEI in step A
