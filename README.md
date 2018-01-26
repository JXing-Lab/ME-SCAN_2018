
# ME-Scan analysis codes for the Alu, LINE, and SVA libraries.

MEScanner is an intergrated tool for identifying polymorphic mobile element insertions (MEIs) using targeted high throughput sequencing.
* Author: Hongseok Ha, JuiWan Loh, Jinchuan Xing
* Current version : 1.2
* Last update date : 10 April 2016
* Homepage: <http://xinglab.genetics.rutgers.edu/>
* Programmer's contact: <hha@hotmail.com>
* PI's contact: <xing@biology.rutgers.edu>

### Requirements: BWA, Blast, LiftOver, Samtools, Bedtools, Primer3

### To run the code:
1. Download whole code and source the main command `source software_path/ME-SCAN.sh`.
2. Download and modify reference files based on the README in each "ref_\*" subdirectories.
3. Creat a pathfile named as "ME-Scan.path" and a parameter file with ".parameters" as the extension in the working directory. 
4. The working directory should include subdirectories named as "Sample_...\*" that contain Fastq files in pair-end format.
5. Running the main command `ME-SCAN.sh`. 

### Folders:
* example_family_list: example pedigree file 
* example_parameters: example parameters files
* modules: individual analysis modules
* ref_blast 
* ref_encode
* ref_gencode
* ref_mescan

### The .parameters file includes the following parameters:
\<parameter\>
* MEI_ref_RM  ==> Name of the MEI to be used in the reference genome RepeatMasker annotation
* MEI_known_stewart ==> Name of the pMEIs to be extracted from Stewart et al. 2011
* MEI_known_dbrip ==> Name of the pMEIs to be extracted from dbRIP (dbrip.org) 
* MEI_known_1kproject ==> Name of the pMEIs to be extracted from Sudmant et al. 2015
* window_size  ==> The range to consider from the mapping site
* mapq_bwa  ==> bwa mapping quality cutoff 
* blast_score_R1 ==> Blast bit score cutoff for Read1
* blast_score_ref ==> Blast bit score cutoff for reference MEIs
* primer_position ==> [5|3], if the ME-specific primer is located on the 5' of the ME, input `5`, if the ME-specific primer is located on the 3' of the ME, input `3`. 
* ME_fragment ==> the ME sequence that will be used for blast. xxx when file name is xxx_primer.fasta
  Caution: direction primer binding site to end of ME
* repeatcover ==> [on|off], if `on` is specified, Read2s which are 100% covered by known MEs will be removed. 
* clustering_type ==> [fixed|flexible], clustering methods allowing fixed or flexible window
  note: ==> MEI_ref_RM, MEI_known_stewart, MEI_known_dbrip can allow multiple terms using regular expression e.g., `MEI_ref_RM=AluYb8|AluYb9`

\<path\>
* path_mescan ==> the location of ME-Scan tool
* path_samtools ==> the location of samtools for coverting bam to sam
* path_bwa ==> the location of bwa for mapping Read2 against the genome
* path_blast ==> the location of blast for filtering Read1
* path_liftover ==> the location of liftover for lifting previous known polymorphic loci (from hg18 to hg19)
* path_sort_temporary_directory ==> the location for temporary files
* path_python3 ==> the location of python3
* path_primer3 ==> the location of primer3 
* path_bedtools ==> the location of bedtools
* path_primer_thermodynamic_parameters  ==> the location of the parameter file for Primer3
