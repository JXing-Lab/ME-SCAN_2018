#!/usr/bin/env python
import argparse,os
from matplotlib import cm
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

fig = Figure()
canvas = FigureCanvas(fig)

parser=argparse.ArgumentParser()
parser.add_argument('--input',nargs='*')
parser.add_argument('--output',nargs='*')

args=parser.parse_args()

input_file=''.join(args.input)

f = open(input_file, 'r')

output=''.join(args.output)

values1=[]
#values2=[]
cs=cm.Set1(np.arange(10)/10.)

for row in f.readlines():
	columns = row.split("=")
	if columns[0]=="CDS":
		values1.append(columns[1])
		nCDS=columns[1]
	elif columns[0]=="UTR":
		values1.append(columns[1])
		nUTR=columns[1]
	elif columns[0]=="CDS_UTR":
		values1.append(columns[1])
		nCDS_UTR=columns[1]
	elif columns[0]=="Undefined_exon":
		values1.append(columns[1])
		nUndefined_exon=columns[1]
	elif columns[0]=="Intron":
		values1.append(columns[1])
		nIntron=columns[1]
	elif columns[0]=="Intergenic":
		values1.append(columns[1])
		nIntergenic=columns[1]

#	elif columns[0]=="start_codon":
#		start_codon=columns[1]
#	elif columns[0]=="stop_codon":
#		stop_codon=columns[1]		
#	elif columns[0]=="lncRNA_exonic":
#		values2.append(columns[1])
#	elif columns[0]=="lncRNA_intronic":
#		values2.append(columns[1])
	else:
		print("The report file has unnecessary factor.")

nSum=int(nCDS)+int(nUTR)+int(nCDS_UTR)+int(nUndefined_exon)+int(nIntron)+int(nIntergenic)
pCDS= "{:.1%}".format(int(nCDS)/nSum)
pUTR= "{:.1%}".format(int(nUTR)/nSum)
pCDS_UTR= "{:.1%}".format(int(nCDS_UTR)/nSum)
pUndefined_exon= "{:.1%}".format(int(nUndefined_exon)/nSum)
pIntron= "{:.1%}".format(int(nIntron)/nSum)
pIntergenic= "{:.1%}".format(int(nIntergenic)/nSum)


values1= [int(v) for v in values1]
#values1= [int(v) for v in values1]

labels1=["CDS "+nCDS.rstrip('\n')+",  "+pCDS,"UTR "+nUTR.rstrip('\n')+",  "+pUTR,"CDS_UTR "+nCDS_UTR.rstrip('\n')+",  "+pCDS_UTR,"Undefined_exon "+nUndefined_exon.rstrip('\n')+",  "+pUndefined_exon,"Intron "+nIntron.rstrip('\n')+",  "+pIntron,"Intergenic "+nIntergenic.rstrip('\n')+",  "+pIntergenic]
#labels2=["lncRNA_exonic","lncRNA_intronic"]

explode = (0, 0, 0, 0, 0, 0)

ax = fig.add_subplot(111)
patches, texts =ax.pie(values1, colors=cs, startangle=90)
#explode=explode, labels=labels1,autopct='%1.1f%%', shadow=True, 
ax.legend(patches, labels1, loc="best")

#ax = fig.add_subplot(222) ## when we use this, we should change  above  "ax = fig.add_subplot(111)"to "ax = fig.add_subplot(121)"
#ax.pie(values2, labels=labels2, colors=cs, autopct='%1.1f%%', shadow=True, startangle=90)

canvas.print_figure(output)