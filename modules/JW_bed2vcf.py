#!/usr/bin/python

import subprocess as sp, argparse,re, sys

parser=argparse.ArgumentParser()
parser.add_argument('--input_file',nargs='*')
parser.add_argument('--primer_pos',nargs='*')

args=parser.parse_args()
input_f=args.input_file
primer_end=args.primer_pos[0]
#print input_f

all_ind = []         # used for header
loci = {}            #(chr,pos,strand,ME_type) as key, [(ind,TPM,UR)] as value
for input in input_f:
	type = re.search(r'SVA|AluYb8|L1HS',input)
	ME_type = ""
	if type:
		ME_type = "INS:ME:"+input[type.start():type.end()]
	else:
		print "No mobile element type being identified."
		sys.exit()

	fh = open(input,"r")
	data = fh.readlines()
	fh.close()
	
	for row in data:
		row=row.strip().split("\t")
		if len(row) != 10:
			print "The format of bed file is not correct. It needs to have TPM and unique read in it."
			sys.exit()
		if row[0] == "chrMT" or row[0] == "chrX" or row[0] == "chrY":
			continue
		if row[6][0] == "m":
			pos = row[2]
			if primer_end == "5":
				strand = "-"
			else:
				strand = "+"
		elif row[6][0] == "p":
			pos = row[1]
			if primer_end == "5":
				strand = "+"
			else:
				strand = "-"
		temp_ind = row[7].split(",")
		temp_TPM = row[8].split(",")
		temp_UR = row[9].split(",")

		for x in range(0,len(temp_ind),1):
			if temp_ind[x] not in all_ind:
				all_ind.append(temp_ind[x])
			if (row[0],pos,strand,ME_type) not in loci.keys():
				loci[(row[0],pos,strand,ME_type)] = [(temp_ind[x],"%s"%("%.1f"%(float(temp_TPM[x]))),temp_UR[x])]
			else:
				loci[(row[0],pos,strand,ME_type)].append((temp_ind[x],"%s"%("%.1f"%(float(temp_TPM[x]))),temp_UR[x]))

#print all_ind, len(all_ind)
	
match = re.search(r'_minus|_plus',input)
temp_input = ""
if match:
	temp_input = input[0:match.start()]+input[match.end():] 
else:
	temp_input = input
output = temp_input.split(".")[:-1]
file = ".".join(output)
out = open(file+".vcf","w")

#printing header of vcf file
out.write("##fileformat=VCFv4.2\n")
out.write("##source=MEScan\n")
out.write("##reference=hg19\n")
out.write("##INFO=<ID=SVTYPE,Number=1,Type=String,Description=\"Type of structural variant\">\n")
out.write("##INFO=<ID=POLARITY,Number=1,Type=String,Description=\"Orientation of insertion\">\n")
out.write("##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n")            
out.write("##FORMAT=<ID=TPM,Number=1,Type=Float,Description=\"Tag Per Million read\">\n")         
out.write("##FORMAT=<ID=UR,Number=1,Type=Integer,Description=\"Number of unique read\">\n")    
out.write("##ALT=<ID=INS:ME:SVA,Description=\"Insertion of SVA element\">\n")
out.write("##ALT=<ID=INS:ME:L1HS,Description=\"Insertion of L1HS element\">\n")
out.write("##ALT=<ID=INS:ME:AluYb8,Description=\"Insertion of AluYb8 element\">\n")
out.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT")
all_ind.sort()
for ind in all_ind:
	out.write("\t"+ind)
out.write("\n")

#sorting the chr pos into MT, autosome, X, y
sorted_loci = sorted(loci, key=lambda x: (int(x[0][3:]), int(x[1])))

#printing the content of vcf file
for each in sorted_loci:        #each is key
	loci[each].sort()
	p0 = sp.Popen(['wget','-qO-','http://genome.ucsc.edu/cgi-bin/das/hg19/dna?segment=%s:%s,%s'%(each[0],each[1],each[1])],stdout = sp.PIPE)
	p1 = sp.Popen(['grep','-v',r'^<'],stdin=p0.stdout,stdout=sp.PIPE)
	ref = p1.communicate()[0].strip().upper()
	out.write(each[0][3:]+"\t"+each[1]+"\t.\t"+ref+"\t"+each[3]+"\t.\tPASS\tSVTYPE="+each[3][7:]+";POLARITY="+each[2]+"\tGT:TPM:UR")
	found = 0
	for ind in all_ind:
		if found < len(loci[each]):
			temp_loc = loci[each][found]
		if ind == temp_loc[0]:
			out.write("\t1/.:"+temp_loc[1]+":"+temp_loc[2])
			found +=1
		else:
			out.write("\t./.")
	out.write("\n")
out.close()

