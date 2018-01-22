#!/usr/bin/python
## Decompress .gz file in subdirectory!!
import subprocess,os,time,argparse,fnmatch,random
parser=argparse.ArgumentParser()
parser.add_argument('--lib',nargs='*')
parser.add_argument('--mei',nargs='*')
parser.add_argument('--r1',nargs='*')
parser.add_argument('--r2',nargs='*')
parser.add_argument('--path',nargs='*')
args=parser.parse_args()

Library=''.join(args.lib)
MEI=''.join(args.mei)
read1=''.join(args.r1)
read2=''.join(args.r2)
file_path=''.join(args.path)

ap="'"
sl='\\'
path_current=os.getcwd()+'/'
path_each_lib=path_current+'Sample_'+Library+'/'


f_path=open(file_path,'r')

for row_path in f_path.readlines():
	columns_path = row_path.split('=')
	if columns_path[0] == "path_mescan":
		path_mescan = columns_path[1]
		path_mescan = path_mescan.rstrip('\n')
	elif columns_path[0] == "path_samtools":
		path_samtools = columns_path[1]
		path_samtools = path_samtools.rstrip('\n')
	elif columns_path[0] == "path_bwa":
		path_bwa = columns_path[1]
		path_bwa = path_bwa.rstrip('\n')
	elif columns_path[0] == "path_blast":
		path_blast = columns_path[1]
		path_blast = path_blast.rstrip('\n')
path_ref_blast=path_mescan+'ref_blast/'

# BWA mapping of read2 running

subprocess.call(''.join([ path_bwa+'bwa mem '+path_ref_blast+'human_g1k_v37.fasta '+read2+'.fastq > '+read2+'_BB.sam' ]),shell=True)
############## Jui Wan modified 5/31/16 ###########################################################################################################################################################
### To remove non-unique read in BB.sam, choosing based on largest MAPQ score
headers = subprocess.Popen("cat "+read2+"_BB.sam |grep '@SQ' > "+read2+"_temp_header",shell=True).wait()
subprocess.Popen("samtools sort -n -@8 "+read2+"_BB.sam > "+read2+"_temp_samtools_sort.bam",shell=True).wait()
body = subprocess.Popen("samtools view "+read2+"_temp_samtools_sort.bam > "+read2+"_temp_body",shell=True).wait()

fk = open(read2+"_temp_body","r")
sam = fk.readlines()
fk.close()
out_R2 = open(read2+"_unique_BB.sam","w")
out_mapq = open(read2+"_having_same_MAPQ_readID_BB_sam.temp","w")
first_sam = sam[0].strip().split("\t")
for row in range(1,len(sam),1):
	temp_sam = sam[row].strip().split("\t")
	if temp_sam[0] == first_sam[0]:
		if first_sam[4] > temp_sam[4]:
			continue
		elif first_sam[4] < temp_sam[4]:
			first_sam = temp_sam
		else:
			out_mapq.write("\t".join(first_sam)+"\n")
			out_mapq.write("\t".join(temp_sam)+"\n")
			continue
	else:
		out_R2.write("\t".join(first_sam)+"\n")
		first_sam = temp_sam
out_R2.write("\t".join(first_sam)+"\n")
out_R2.close()
out_mapq.close()
p1 = subprocess.Popen("cat "+read2+"_temp_header "+read2+"_unique_BB.sam > "+read2+"_filtered_BB.sam",shell=True).wait()
subprocess.Popen("rm "+read2+"_unique_BB.sam",shell=True)
subprocess.Popen("rm "+read2+"_temp_samtools_sort.bam",shell=True)
subprocess.Popen("rm "+read2+"_temp_header",shell=True)
subprocess.Popen("rm "+read2+"_temp_body",shell=True)
###################################################################################################################################################################################################

subprocess.call(''.join([ path_samtools+'samtools view -bS '+read2+'_filtered_BB.sam > '+read2+'_BB.bam']),shell=True)
subprocess.call(''.join([ path_samtools+'samtools sort '+read2+'_BB.bam '+read2+'_BB_sorted']),shell=True)
print("\n\n")
time.sleep(5)
subprocess.call(''.join([ path_samtools+'samtools index '+read2+'_BB_sorted.bam']),shell=True)
subprocess.call(''.join([ path_samtools+'samtools idxstats '+read2+'_BB_sorted.bam ']),shell=True)
print("\n\n-----"+Library+", BWA mapping is completed-----\n")


# Making fasta file from read1
subprocess.call(''.join([ 'cat '+read1+'.fastq | perl -e '+ap+'$i=0;while(<>){if(/^\@/&&$i==0){s/^\@/\>/;print;}elsif($i==1){print;$i=-3}$i++;}'+ap+\
 						'|awk '+ap+' {if(NR%2==0)print $0; else if(NR%2==1) print $1}'+ap+'> '+read1+'.fasta']),shell=True) 

# Blast running 
## makedb command to bash script.
subprocess.call(''.join([ path_blast+'blastn -task blastn-short -db '+path_ref_blast+MEI+'_primer.fasta -query '+read1+'.fasta -outfmt 6 -out '+read1+'_'+MEI+'_blast.out']),shell=True)

subprocess.call(''.join([ 'sort -k 1b,1 '+read1+'_'+MEI+'_blast.out >'+read1+'_'+MEI+'_blast.filter']),shell=True)
############## Jui Wan modified 5/31/16 ##########################################################################################################################################################
### To remove non-unique read in blast.filter, choosing based on largest bitscore
fh = open(read1+"_"+MEI+"_blast.filter","r")
data = fh.readlines()
fh.close()

out_bitscore = open(read1+"_"+MEI+"_having_same_bitscore_readID_blast_filter.temp","w")
out_R1 = open(read1+"_"+MEI+"_unique_blast.filter","w")
first = data[0].strip().split("\t")
for row in range(1,len(data),1):
	temp=data[row].strip().split("\t")
	if first[0] == temp[0]:
		if first[11] > temp[11]:
			continue
		elif first[11] < temp[11]:
			first = temp
		else:
			out_bitscore.write("\t".join(first)+"\n")
			out_bitscore.write("\t".join(temp)+"\n")
			continue
	else:
		out_R1.write("\t".join(first)+"\n")
		first = temp
out_R1.write("\t".join(first)+"\n")
out_bitscore.close()
out_R1.close()
p2 = subprocess.Popen("mv "+read1+"_"+MEI+"_unique_blast.filter "+read1+"_"+MEI+"_blast.filter",shell=True).wait()
###################################################################################################################################################################################################
