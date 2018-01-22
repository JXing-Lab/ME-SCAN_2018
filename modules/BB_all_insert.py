#!/usr/bin/python
## Location: subdirectory
import subprocess,os,time,argparse,fnmatch

parser=argparse.ArgumentParser()

parser.add_argument('--mei',nargs='*')
parser.add_argument('--mfl',nargs='*')
parser.add_argument('--option_tag',nargs='*')
parser.add_argument('--path_output',nargs='*')

args=parser.parse_args()
MEI=''.join(args.mei)
mean_frag_length=''.join(args.mfl)
option_tag=''.join(args.option_tag)
path_output=''.join(args.path_output)

ap="'"
sl='\\'

mapping_plus=path_output+MEI+'_all.mapping_plus'+option_tag+'temp'
initial_plus=path_output+MEI+'_all.initial_plus'+option_tag+'temp'

f = open(mapping_plus, 'r')
initial = open(initial_plus, 'r')
tag = 1

for initial_row in initial.readlines():
	initial_columns = initial_row.split()
for row in f.readlines():
	columns = row.split()
	if initial_columns[0]==columns[0] and int(columns[2])<=int(initial_columns[2])+int(mean_frag_length):
		print (columns[0],columns[1],columns[2],columns[3],columns[4],"plus"+str(tag))

	elif initial_columns[0]==columns[0] and int(columns[2])>int(initial_columns[2])+int(mean_frag_length):
		tag=tag+1
		print (columns[0],columns[1],columns[2],columns[3],columns[4],"plus"+str(tag))
		initial_columns=columns
	
	elif initial_columns[0]!=columns[0]:
		tag=tag+1
		print (columns[0],columns[1],columns[2],columns[3],columns[4],"plus"+str(tag))
		initial_columns=columns		
	

del f,initial,tag

mapping_minus=path_output+MEI+'_all.mapping_minus'+option_tag+'temp'
initial_minus=path_output+MEI+'_all.initial_minus'+option_tag+'temp'


f = open(mapping_minus, 'r')
initial = open(initial_minus, 'r')
tag = 1

for initial_row in initial.readlines():
	initial_columns = initial_row.split()
for row in f.readlines():
	columns = row.split()
	if initial_columns[0]==columns[0] and int(columns[2])<=int(initial_columns[2])+int(mean_frag_length):
		print (columns[0],columns[1],columns[2],columns[3],columns[4],"minus"+str(tag))
	elif initial_columns[0]==columns[0] and int(columns[2])>int(initial_columns[2])+int(mean_frag_length):
		tag=tag+1
		print (columns[0],columns[1],columns[2],columns[3],columns[4],"minus"+str(tag))
		initial_columns=columns
	elif initial_columns[0]!=columns[0]:
		tag=tag+1
		print (columns[0],columns[1],columns[2],columns[3],columns[4],"minus"+str(tag))
		initial_columns=columns