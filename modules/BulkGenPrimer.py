#!/usr/bin/env python
# python3 /path/BulkGenPrimer.py [-i] input_file [-g] reference_genome [-r] radius [-o] output_file_name_except_for_extention [-w] workplace
# /usr/local/ME-Scan_tools/modules/BulkGenPrimer.py -i test_genotyping.bed -g /lab01/DataSets/hg19/hg19_low_case.fa -r 500 -s 1000 -o primers
# requiremens:bedtools,primer3,python3
# PRIMER_PRODUCT_SIZE_RANGE should be larger then target length from bed file
# We suggest the reference genome including repeat region written in lower case

import subprocess,argparse,os,time

parser=argparse.ArgumentParser()

parser.add_argument('-i','--input_file',nargs='*')
parser.add_argument('-g','--reference_genome',nargs='*')
parser.add_argument('-r','--radius',nargs='*')
parser.add_argument('-s','--seqrange',nargs='*')
parser.add_argument('-o','--output_file',nargs='*')
parser.add_argument('-ot','--option_tag',nargs='*')
parser.add_argument('--path',nargs='*')
args=parser.parse_args()

input_file=''.join(args.input_file)
reference_genome=''.join(args.reference_genome)
radius=''.join(args.radius)
seqrange=''.join(args.seqrange)
output_file=''.join(args.output_file)
option_tag=''.join(args.option_tag)
file_path=''.join(args.path)
path_current=os.getcwd()+'/'
path_genotyping_primers=path_current+'genotyping_primers'+option_tag+'/'

print(option_tag)
f_path=open(file_path,'r')

for row_path in f_path.readlines():
	columns_path = row_path.split('=')
	if columns_path[0] == "path_primer3":
		path_primer3 = columns_path[1]
		path_primer3 = path_primer3.rstrip('\n')
	elif columns_path[0] == "path_bedtools":
		path_bedtools = columns_path[1]
		path_bedtools = path_bedtools.rstrip('\n')
	elif columns_path[0] == "path_mescan":
		path_mescan = columns_path[1]
		path_mescan = path_mescan.rstrip('\n')
	elif columns_path[0] == "path_primer_thermodynamic_parameters":
		path_primer_thermodynamic_parameters = columns_path[1]
		path_primer_thermodynamic_parameters = path_primer_thermodynamic_parameters.rstrip('\n')
input_Bed_file=path_genotyping_primers+"input_Bed_file.dat"
sequences_temp=path_genotyping_primers+"sequences_file.temp"
sequences_file=path_genotyping_primers+"sequences_file.dat"
option_file=path_mescan+"modules/option.opt"
customized_option_file=path_genotyping_primers+"customized_option.opt"
shell_file=path_current+"run.sh"

path_prithepa=path_primer_thermodynamic_parameters.replace('/','\/')

subprocess.call(''.join([ 'cat '+option_file+'|sed \'s/PATHTHERMOPARA/'+path_prithepa+'/g\' > '+customized_option_file]),shell=True)

fileName, fileExtension=os.path.splitext(input_file)
# Make bed file with radius  and delete "chr" words in first column
if fileExtension == ".bed" :
	subprocess.call(''.join([ 'awk \'{print $1"\\t"$2-'+str(seqrange)+'"\\t"$3+'+str(seqrange)+'}\' '+input_file+'|sed \'s/[Cc][Hh][Rr]//g\'>'+input_Bed_file]),shell=True)

elif fileExtension == ".vcf" :
	subprocess.call(''.join([ 'awk \'{print $1"\\t"$2-'+str(seqrange)+'"\\t"$2+'+str(seqrange)+'}\' '+input_file+'|sed \'s/[Cc][Hh][Rr]//g\'>'+input_Bed_file]),shell=True)

# Extract sequences from genome coordinates

subprocess.call(''.join([ "sudo "+path_bedtools+'bedtools getfasta -fi '+reference_genome+' -bed '+input_Bed_file+' -fo '+sequences_temp]),shell=True)
subprocess.call(''.join([ 'sed -n "H;$ {x;s/\\n/\\t/g;p;}" '+sequences_temp+'|\sed \'s/>/\\n/g\'|\sed \'s/:/\\t/g\'|\sed \'s/-/\\t/g\'>'+sequences_file]),shell=True)

# extract sequences from genome coordinates

f=open(sequences_file, 'r')
s=open(shell_file,'w')
s.write('#!/bin/sh'+'\n')#!/bin/sh
subprocess.call(''.join(['chmod 777 '+shell_file]),shell=True)
f.readline() # remove '\t\n' value in first line
i=0
co=open(customized_option_file, 'r')
option=co.readlines()
for row in f.readlines():
	column=row.split()
	i+=1
	chromosome=column[0]
	tstart=column[1]
	tend=column[2]
	sequences=column[3]
	o=open(output_file+str(i)+".dat", 'w')
	position=int(tstart)+int(seqrange)
	print(position)
	o.write('SEQUENCE_ID='+"chr"+str(chromosome)+":"+str(position)+'\n') #SEQUENCE_ID=example
	o.write('SEQUENCE_TEMPLATE='+sequences+'\n') #SEQUENCE_TEMPLATE=
	o.write('SEQUENCE_TARGET='+str(int(seqrange)-int(radius))+','+str(int(tend)-int(tstart)-2*int(seqrange)+2*int(radius))+'\n') #SEQUENCE_TARGET=start,length
	for op in option:
		o.write(op)

	## primer3_core [-format_output] [-default_version=1|-default_version=2] [-io_version=4] [-p3_settings_file=<file_path>] [-echo_settings_file] [-strict_tags] [-output=<file_path>] [-error=<file_path>] [input_file]

	cmd_primer3=path_primer3+'primer3_core -format_output -output '+output_file+str(i)+'.out <'+output_file+str(i)+'.dat'
	s.write(cmd_primer3+'\n')

s.close()

subprocess.call(''.join(['./run.sh&']),shell=True)

# in option_file
## PRIMER_TASK=pick_detection_primers
## PRIMER_PICK_LEFT_PRIMER=1
## PRIMER_PICK_INTERNAL_OLIGO=1
## PRIMER_PICK_RIGHT_PRIMER=1
## PRIMER_OPT_SIZE=18
## PRIMER_MIN_SIZE=15
## PRIMER_MAX_SIZE=21
## PRIMER_MAX_NS_ACCEPTED=1
## PRIMER_PRODUCT_SIZE_RANGE=75-100
## P3_FILE_FLAG=1
## SEQUENCE_INTERNAL_EXCLUDED_REGION=
## PRIMER_EXPLAIN_FLAG=1
## =

