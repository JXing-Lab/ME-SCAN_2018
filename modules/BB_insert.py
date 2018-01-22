#!/usr/bin/python
## Location: subdirectory
import subprocess,os,time,argparse,fnmatch

parser=argparse.ArgumentParser()
parser.add_argument('--lib',nargs='*')
parser.add_argument('--mei',nargs='*')
parser.add_argument('--option_tag',nargs='*')
parser.add_argument('--r1',nargs='*')
parser.add_argument('--r2',nargs='*')
parser.add_argument('--mfl',nargs='*')
parser.add_argument('--path',nargs='*')

args=parser.parse_args()
Library=''.join(args.lib)
MEI=''.join(args.mei)
option_tag=''.join(args.option_tag)
read1=''.join(args.r1)
read2=''.join(args.r2)
mean_frag_length=''.join(args.mfl)
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

path_ref=path_mescan+'ref_bwa/'

mapping_plus=read2+'.mapping_plus'+option_tag+'temp'
initial_plus=read2+'.initial_plus'+option_tag+'temp'

f = open(mapping_plus, 'r')
initial = open(initial_plus, 'r')
tag = 1

for initial_row in initial.readlines():
	initial_columns = initial_row.split()
for row in f.readlines():
	columns = row.split()
	if initial_columns[0]==columns[0] and int(columns[2])<=int(initial_columns[2])+int(mean_frag_length):
		print (columns[0],columns[1],columns[2],columns[3],"individual_plus"+str(tag))

	elif initial_columns[0]==columns[0] and int(columns[2])>int(initial_columns[2])+int(mean_frag_length):
		tag=tag+1
		print (columns[0],columns[1],columns[2],columns[3],"individual_plus"+str(tag))
		initial_columns=columns
	
	elif initial_columns[0]!=columns[0]:
		tag=tag+1
		print (columns[0],columns[1],columns[2],columns[3],"individual_plus"+str(tag))
		initial_columns=columns		
		

del f,initial,tag 

mapping_minus=read2+'.mapping_minus'+option_tag+'temp'
initial_minus=read2+'.initial_minus'+option_tag+'temp' 

f = open(mapping_minus, 'r')
initial = open(initial_minus, 'r')
tag = 1

for initial_row in initial.readlines():
	initial_columns = initial_row.split()
for row in f.readlines():
	columns = row.split()
	if initial_columns[0]==columns[0] and int(columns[2])<=int(initial_columns[2])+int(mean_frag_length):
		print (columns[0],columns[1],columns[2],columns[3],"individual_minus"+str(tag))
	elif initial_columns[0]==columns[0] and int(columns[2])>int(initial_columns[2])+int(mean_frag_length):
		tag=tag+1
		print (columns[0],columns[1],columns[2],columns[3],"individual_minus"+str(tag))
		initial_columns=columns
	elif initial_columns[0]!=columns[0]:
		tag=tag+1
		print (columns[0],columns[1],columns[2],columns[3],"individual_minus"+str(tag))
		initial_columns=columns
