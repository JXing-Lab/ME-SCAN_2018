# This folder contains the 1000 genomes reference and outputs of blast results used for mapping reads

To generate the 1000 genomes reference:

1. Download human_g1k_v37.fasta.gz from <ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/>
2. gzip -d human_g1k_v37.fasta.gz

Fasta files needed for mapping:

1. L1HS_primer.fasta (for L1 analysis)
2. AluYb8_primer.fasta (for Alu analysis)
3. SVA_primer.fasta (for SVA analysis)
4. SVA_Alu_L1_primer.fasta (for pooled analysis of Alu, L1, and SVA analysis) 
