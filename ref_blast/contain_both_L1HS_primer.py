#!/usr/bin/python

fh = open("/lab01/Projects/MEScan/Analysis_SVA_Mar022015/juiwan/ME-Scan_tools/ME-SCAN-SVA/ref_blast/sorted_reference_L1HS_1st_blastn-short.bed","r")
primer_1st = fh.readlines()
fh.close()

fk = open("/lab01/Projects/MEScan/Analysis_SVA_Mar022015/juiwan/ME-Scan_tools/ME-SCAN-SVA/ref_blast/sorted_reference_L1HS_Ewing_2010_blastn-short.bed","r")
primer_2nd = fk.readlines()
fk.close()

d_1st = {} #chr as key, [(start, strand)] as value
for row in primer_1st:
	row=row.strip().split("\t")
	if row[0][3:5] != "GL" and row[0][3:5] != "MT":
		if row[0] not in d_1st.keys():
			d_1st[row[0]]=[(row[1],row[5])]
		else:
			d_1st[row[0]].append((row[1],row[5]))

d_2nd = {}	# chr as key, [(start,end,bitscore,evalue)] as value
for row in primer_2nd:
	row=row.strip().split("\t")
	if row[0][3:5] != "GL" and row[0][3:5] != "MT":
		if row[0] not in d_2nd.keys():
			d_2nd[row[0]]=[(row[1],row[2],row[3],row[4])]
		else:
			d_2nd[row[0]].append((row[1],row[2],row[3],row[4]))

out = open("/lab01/Projects/MEScan/Analysis_SVA_Mar022015/juiwan/ME-Scan_tools/ME-SCAN-SVA/ref_mescan/Reference_L1HS_blastn-short.bed","w") #Ewing that has 1st primer
for each_chr in d_1st.keys():
	f_point = 0
	s_point = 0
	while (f_point < len(d_1st[each_chr]) and s_point < len(d_2nd[each_chr])):
		temp_f = d_1st[each_chr][f_point]
		temp_s = d_2nd[each_chr][s_point]
		if temp_f[1] == "plus":
			diff = int(temp_s[0])-int(temp_f[0])
			if diff < 50:
				s_point += 1
			elif diff >= 50 and diff <= 105:
				f_point += 1
				s_point += 1
				out.write(each_chr+"\t"+"\t".join(temp_s)+"\n")
			else:
				f_point += 1
		else:
			diff = int(temp_f[0])-int(temp_s[0])
			if diff < 50:
				f_point += 1
			elif diff >= 50 and diff <= 105:
				f_point += 1
				s_point += 1
				out.write(each_chr+"\t"+"\t".join(temp_s)+"\n")
			else:
				s_point += 1
#		print diff
#		if diff == 49 :
#			print each_chr, temp_f[0], temp_s[0]

out.close()
