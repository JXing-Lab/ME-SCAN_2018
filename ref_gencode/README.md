### This folder contains the human reference genome gene annotation file used for pMEI annotation.

1. Download gencode.v19.annotation.gtf from <http://www.gencodegenes.org/releases/19.html>
2. Generate the file "gencode.v19.protein_coding.bed":

`cat gencode.v19.annotation.gtf|grep protein_coding|awk '{print $1"\t"$4"\t"$5"\t"$3"\t"$10"\t"$18}'> gencode.v19.protein_coding.bed`

3. The file "gencode.v19.protein_coding.bed" will be used by the pipeline `MEScaner.sh` in step D7
