#!/usr/bin/python

import subprocess,os,time,argparse,fnmatch

parser=argparse.ArgumentParser()
parser.add_argument('--lib',nargs='*')
parser.add_argument('--mei',nargs='*')
parser.add_argument('--mapq',nargs='*')
parser.add_argument('--blast',nargs='*')
parser.add_argument('--r1',nargs='*')
parser.add_argument('--r2',nargs='*')
parser.add_argument('--option_tag',nargs='*')
parser.add_argument('--repeatcover',nargs='*')
parser.add_argument('--path',nargs='*')

args=parser.parse_args()
Library=''.join(args.lib)
MEI=''.join(args.mei)
Mapq_cutoff=''.join(args.mapq)
Blast_cutoff1=''.join(args.blast)
read1=''.join(args.r1)
read2=''.join(args.r2)
option_tag=''.join(args.option_tag)
repeatcover=''.join(args.repeatcover)
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
	if columns_path[0] == "path_sort_temporary_directory":
		path_sort_temporary_directory = columns_path[1]
		path_sort_temporary_directory = path_sort_temporary_directory.rstrip('\n')

path_ref_mescan=path_mescan+'ref_mescan/'

# Filtered by read1 including target MEI fragments
# Cutoff MAPQ and make read2 bed format
subprocess.call(''.join([ 'bamToBed -i '+read2+'_BB_sorted.bam|awk '+ap+'$5>='+Mapq_cutoff+'{print "chr"$1"'+sl+'t'+'"$2"'+sl+'t'+'"$3"'+sl+'t'+'"$4"'+sl+'t'+'"$5"'+sl+'t'+'"$6}'+ap+'|coverageBed -a '+path_ref_mescan+'hg19.fa.bed'+' -b stdin > '+read2+option_tag+'repeatcover.temp' ]),shell=True)

if repeatcover=="on":
        subprocess.call(''.join([ 'cat '+read2+option_tag+'repeatcover.temp|awk '+ap+'$6=="+" && $10!=1 {print $1"'+sl+'t'+'"$2"'+sl+'t'+'"$3"'+sl+'t'+'"$4"'+sl+'t'+'"$5"'+sl+'t'+'"$6} $6=="-" && $10!=1 {print $1"'+sl+'t'+'"$3"'+sl+'t'+'"$2"'+sl+'t'+'"$4"'+sl+'t'+'"$5"'+sl+'t'+'"$6}'+ap+'|awk '+ap+'{print $4"'+sl+'t'+'"$1"'+sl+'t'+'"$2"'+sl+'t'+'"$3"'+sl+'t'+'"$5"'+sl+'t'+'"$6}'+ap+'|grep -v "GL"|sort -T '+path_sort_temporary_directory+' -k 1b,1 >'+read2+'.rm_unplaced'+option_tag+'temp' ]),shell=True)

elif repeatcover=="off":
        subprocess.call(''.join([ 'cat '+read2+option_tag+'repeatcover.temp|awk '+ap+'$6=="+"{print $1"'+sl+'t'+'"$2"'+sl+'t'+'"$3"'+sl+'t'+'"$4"'+sl+'t'+'"$5"'+sl+'t'+'"$6} $6=="-"{print $1"'+sl+'t'+'"$3"'+sl+'t'+'"$2"'+sl+'t'+'"$4"'+sl+'t'+'"$5"'+sl+'t'+'"$6}'+ap+'|awk '+ap+'{print $4"'+sl+'t'+'"$1"'+sl+'t'+'"$2"'+sl+'t'+'"$3"'+sl+'t'+'"$5"'+sl+'t'+'"$6}'+ap+'|grep -v "chrGL"|sort -T '+path_sort_temporary_directory+' -k 1b,1 >'+read2+'.rm_unplaced'+option_tag+'temp' ]),shell=True)


subprocess.call(''.join([ 'join '+read2+'.rm_unplaced'+option_tag+'temp '+read1+'_'+MEI+'_blast.filter|awk '+ap+'{print $2"'+sl+'t'+\
                                                '"$3"'+sl+'t'+'"$4"'+sl+'t'+'"$1"'+sl+'t'+'"$5"'+sl+'t'+'"$6"'+sl+'t'+'"$17"'+sl+'t'+'"$16}'+ap+\
                                                '|sed '+ap+'s/chrX/23/g'+ap+'|sed '+ap+'s/chrY/24/g'+ap+'|sed '+ap+'s/^chr//g'+ap+'|sort -T '+path_sort_temporary_directory+' -k1n -k2n|sed '+\
                                                ap+'s/^/chr/g'+ap+'|sed '+ap+'s/chr23/chrX/g'+ap+'|sed '+ap+'s/chr24/chrY/g'+ap+'> '+read2+'.pre_target.filtered'+option_tag+'temp']),shell=True)
subprocess.call(''.join(['cat '+read2+'.pre_target.filtered'+option_tag+'temp|awk '+ap+'$7>='+Blast_cutoff1+'{print $0}'+ap+'> '+read2+'.target.filtered'+option_tag+'temp']),shell=True)


subprocess.call(''.join(['cat '+read2+'.target.filtered'+option_tag+'temp|awk '+ap+'$6=="-"{print $1"'+sl+'t'+'"$2"'+sl+'t'+'"$3}'+ap+'|uniq -c|awk '+ap+'{print $2"'+sl+'t'+'"$3"'+sl+'t'+'"$4"'+sl+'t'+'"$1}'+ap+'|sed -n 1,1p > '+read2+'.initial_minus'+option_tag+'temp']),shell=True)
subprocess.call(''.join(['cat '+read2+'.target.filtered'+option_tag+'temp|awk '+ap+'$6=="-"{print $1"'+sl+'t'+'"$2"'+sl+'t'+'"$3}'+ap+'|uniq -c|awk '+ap+'{print $2"'+sl+'t'+'"$3"'+sl+'t'+'"$4"'+sl+'t'+'"$1}'+ap+' > '+read2+'.mapping_minus'+option_tag+'temp']),shell=True)
subprocess.call(''.join(['cat '+read2+'.target.filtered'+option_tag+'temp|awk '+ap+'$6=="+"{print $1"'+sl+'t'+'"$2"'+sl+'t'+'"$3}'+ap+'|uniq -c|awk '+ap+'{print $2"'+sl+'t'+'"$3"'+sl+'t'+'"$4"'+sl+'t'+'"$1}'+ap+'|sed -n 1,1p > '+read2+'.initial_plus'+option_tag+'temp']),shell=True)
subprocess.call(''.join(['cat '+read2+'.target.filtered'+option_tag+'temp|awk '+ap+'$6=="+"{print $1"'+sl+'t'+'"$2"'+sl+'t'+'"$3}'+ap+'|uniq -c|awk '+ap+'{print $2"'+sl+'t'+'"$3"'+sl+'t'+'"$4"'+sl+'t'+'"$1}'+ap+' > '+read2+'.mapping_plus'+option_tag+'temp']),shell=True)


