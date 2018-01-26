
# ME-Scan analysis codes for the Alu, LINE, and SVA libraries.

MEScanner is an intergrated tool for identifying polymorphic mobile element insertions (MEIs) using targeted high throughput sequencing.
* Author: Hongseok Ha, JuiWan Loh, Jinchuan Xing
* Current version : 1.2
* Last update date : 10 April 2016
* Homepage: <http://xinglab.genetics.rutgers.edu/>
* Programmer's contact: <hha@hotmail.com>
* PI's contact: <xing@biology.rutgers.edu>

### Requireements: BWA, Blast, LiftOver, Samtools, Bedtools, Primer3

### To run the code:
1. Download whole code and source the main command `source /"software_path"/ME-SCAN.sh`.
2. Download and modify reference file based on their own README in each "ref_\*" subdirectories.
3. Creat a pathfile named as "ME-Scan.path" and parameterfile with ".parameters" as extension in the working directory. 
4. The working directory should include subdirectories named as "Sample_...\*", which contain Fastq files in pair-end format.
5. Running the main command `ME-SCAN.sh`. 

### Folders:
* example_family_list: contains an example named "family_list.ped" 
* example_parameters: contains examples of .parameters files
* modules: individual analysis modules
* ref_blast 
* ref_encode
* ref_gencode
* ref_mescan

### The .parameters file includes the following parameters:
\<parameter\>
* MEI_ref_RM  #==> when we make reference MEI dataset, alow this terms based on the interection with RepeatMasker
* MEI_known_stewart #==> this term is for extracting pMEI dataset from previous study, Stewart et al. 2011
* MEI_known_dbrip #==> this term is used for file name of pMEI dataset from dbRIP (dbrip.org) / for extracting, MEI was used.
* MEI_known_1kproject #==> this term is for extracting pMEI dataset from previous study, Sudmant et al. 2015
* window_size  #==> The range from mapping site
* mapq_bwa  #==> bwa mapping quality
* blast_score_R1 #==> Blast bit score for Read 1
* blast_score_ref #==> Blast bit score for reference MEIs
* primer_position #==> if the ME-specific primer is located on the 5' of the ME, input 5
* ME_fragment  #==>this will be used for blast. xxx when file name is xxx_primer.fasta, it can include additional infor mation)
  Caution: direction primer binding site to end of ME
* repeatcover #==> 'on' will be choosed for removing read2s which are 100% covered by known MEs. If you choose 'off', the option is not available
* clustering_type #==> 'fixed' or 'flexible' clustering method can be choosed
  note: ==> MEI_ref_RM, MEI_known_stewart, MEI_known_dbrip can allow multiple terms using regular expression e.g. MEI_ref_RM=AluYb8\|AluYb9

\<path\>
* path_mescan #==> the location of ME-Scan tools
* path_samtools #==> the location of samtools for coverting bam to sam
* path_bwa #==> the location of bwa for mapping Read2 against the genome
* path_blast #==> the location of blast for filtering of Read1
* path_liftover #==> the location of liftover for lifting previous known polymorphic loci (from hg18 to hg19)
* path_sort_temporary_directory
* path_python3 #==> the location of python3
* path_primer3 #==> the location of primer3 
* path_bedtools #==> the location of bedtools
* path_primer_thermodynamic_parameters
