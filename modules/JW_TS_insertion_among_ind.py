#!/usr/bin/python

import subprocess as sp, argparse,re, sys

parser=argparse.ArgumentParser()
parser.add_argument('--input_file',nargs='*')

args=parser.parse_args()
input_f=args.input_file
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
			strand = "-"
		elif row[6][0] == "p":
			pos = row[1]
			strand = "+"
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

print all_ind, len(all_ind)

match = re.search(r'_minus|_plus',input)
temp_input = ""
if match:
	temp_input = input[0:match.start()]+input[match.end():] 
else:
	temp_input = input
output = temp_input.split(".")[:-1]
file = ".".join(output)

indID = {}	#{21:[21-cell,21-iPSC,21-NSC,21-neurons],...}
for each in all_ind:
	name=each.split("-")
	if name[0] not in indID.keys():
		indID[name[0]] = [each]
	else:
		indID[name[0]].append(each)

for each_ind in indID.keys():
	out = open(file+"_across_ind_%s.vcf"%each_ind,"w")
	
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
	indID[each_ind].sort()
	for ind in indID[each_ind]:
		out.write("\t"+ind)
	out.write("\n")
	
	#sorting the chr pos
	sorted_loci = sorted(loci, key=lambda x: (int(x[0][3:]), int(x[1])))
	
	#printing the content of vcf file
	for each in sorted_loci:        #each is key
		loci[each].sort()
		flag_ind = False	#print out only those insertion positions that are found in this individual (with any 4 cell types)
		for ins in loci[each]:
			if ins[0] in indID[each_ind]:
				flag_ind = True
				break
		if not flag_ind:
			continue
		p0 = sp.Popen(['wget','-qO-','http://genome.ucsc.edu/cgi-bin/das/hg19/dna?segment=%s:%s,%s'%(each[0],each[1],each[1])],stdout = sp.PIPE)
		p1 = sp.Popen(['grep','-v',r'^<'],stdin=p0.stdout,stdout=sp.PIPE)
		ref = p1.communicate()[0].strip().upper()
		out.write(each[0][3:]+"\t"+each[1]+"\t.\t"+ref+"\t"+each[3]+"\t.\tPASS\tSVTYPE="+each[3][7:]+";POLARITY="+each[2]+"\tGT:TPM:UR")

		for ind in indID[each_ind]:
			found = False
			for each_ins in loci[each]:
				if each_ins[0] == ind:
					out.write("\t1/.:"+each_ins[1]+":"+each_ins[2])
					found = True
					break
			if not found:
				out.write("\t./.")
		out.write("\n")
	out.close()

