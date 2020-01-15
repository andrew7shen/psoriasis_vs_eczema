#Andrew Shen
import sys
import re

###To run this program, go to the command line and specify five parameters:
###python psoriasis_eczema.py (comparison file 1) (comparison file 2) (output file)
###For this program, (comparison file 1) is the file with the eczema data and (comparison file 2) is the file with the psoriasis data.

###Sets the two input files to different variables: "eczema_input" and "psoriasis_input"
input_file = sys.argv[1]
read = open(input_file, "r")
eczema_input = read.read()

input_file = sys.argv[2]
read = open(input_file, "r")
psoriasis_input = read.read()

###Cleans up the eczmema input file into a format with the values of the data file in a list of lists.
eczema_lines = eczema_input.splitlines()
del eczema_lines[0:17]
eczema_tabs = []
for item in eczema_lines:
	eczema_tabs.append(item.split("\t"))
del eczema_tabs[len(eczema_tabs)-5:len(eczema_tabs)]
for item in eczema_tabs:
	item[0] = re.sub('<[^>]+>', '', item[0])
	item[1] = re.sub('<[^>]+>', '', item[1])
	item[2] = re.sub('<[^>]+>', '', item[2])
	item[3] = re.sub('<[^>]+>', '', item[3])
	item[4] = re.sub('<[^>]+>', '', item[4])
	item[5] = re.sub('<[^>]+>', '', item[5])
	item[6] = re.sub('<[^>]+>', '', item[6])
	item[7] = re.sub('<[^>]+>', '', item[7])
eczema_strings = []
for item in eczema_tabs:
	for value in item:
		eczema_strings.append(value.replace('"', ''))
eczema_split = [eczema_strings[x:x+8] for x in range(0, len(eczema_strings),8)]

###Filters out data values with an adjusted P-value of over .05
eczema_filtered =[]
for item in eczema_split:
	item[1] = float(item[1])
	if item[1] < .05:
		eczema_filtered.append(item) ###There are 575 genes with an adj.P.value less than 0.05

###Creates a dictionary with the gene name as the key and the logFC as the value.
eczema_dict = {}
for item in eczema_filtered:
	eczema_dict[item[6]] = float(item[5])

###Cleans up the psoriasis input file into a format with the values of the data file in a list of lists.
psoriasis_lines = psoriasis_input.splitlines()
del psoriasis_lines[0:17]
psoriasis_tabs = []
for item in psoriasis_lines:
	psoriasis_tabs.append(item.split("\t"))
del psoriasis_tabs[len(psoriasis_tabs)-5:len(psoriasis_tabs)]
for item in psoriasis_tabs:
	item[0] = re.sub('<[^>]+>', '', item[0])
	item[1] = re.sub('<[^>]+>', '', item[1])
	item[2] = re.sub('<[^>]+>', '', item[2])
	item[3] = re.sub('<[^>]+>', '', item[3])
	item[4] = re.sub('<[^>]+>', '', item[4])
	item[5] = re.sub('<[^>]+>', '', item[5])
	item[6] = re.sub('<[^>]+>', '', item[6])
	item[7] = re.sub('<[^>]+>', '', item[7])
psoriasis_strings = []
for item in psoriasis_tabs:
	for value in item:
		psoriasis_strings.append(value.replace('"', ''))
psoriasis_split = [psoriasis_strings[x:x+8] for x in range(0, len(psoriasis_strings),8)]

###Filters out data values with an adjusted P-value of over .05
psoriasis_filtered =[]
for item in psoriasis_split:
	item[1] = float(item[1])
	if item[1] < .05:
		psoriasis_filtered.append(item) ###There are 3729 genes with an adj.P.value less than 0.05

###Creates a dictionary with the gene name as the key and the logFC as the value.
psoriasis_dict = {}
for item in psoriasis_filtered:
	psoriasis_dict[item[6]] = float(item[5])

###Creates four lists after comparing the logFC (log fold change) of the eczema data set and the psoriasis data set:
###1. Genes that overlap with the same direction (overlap_same)
###2. Genes that overlap with the opposite direction (overlap_oppo)
###3. Genes that are unique to psoriasis (psor_only)
###4. Genes that are unique to eczema (ecze_only)
overlap_same = []
overlap_oppo = []
ecze_only = []
psor_only = []
overlap_dict = {}
for key in eczema_dict:
	if key in psoriasis_dict:
		overlap_dict[key] = [eczema_dict[key], psoriasis_dict[key]]

for key in overlap_dict:
	if overlap_dict[key][0] > 0 and overlap_dict[key][1] > 0 or overlap_dict[key][0] < 0 and overlap_dict[key][1] < 0:
		overlap_same.append(key)
	else:
		overlap_oppo.append(key)
del overlap_same[0]
for key in eczema_dict:
	if key not in overlap_dict:
		ecze_only.append([key,eczema_dict[key]])
for key in psoriasis_dict:
	if key not in overlap_dict:
		psor_only.append([key, psoriasis_dict[key]])

###Formats the data into a text file with four columns: one for each of the different lists.
for item in ecze_only:
	if item[1] > 0:
		item[1] = " up"
	else:
		item[1] = " down"
ecze_final = []
for item in ecze_only:
	ecze_final.append("".join(item))
for item in psor_only:
	if item[1] > 0:
		item[1] = " up"
	else:
		item[1] = " down"
psor_final = []
for item in psor_only:
	psor_final.append("".join(item))
for i in range(2804 - len(overlap_same)):
	overlap_same.append(".")
for i in range(2804 - len(overlap_oppo)):
	overlap_oppo.append(".")
for i in range(2804 - len(ecze_only)):
	ecze_only.append(".")
for i in range(2804 - len(psor_only)):
	psor_only.append(".")
final = 0
final = [overlap_same, overlap_oppo, ecze_final, psor_final]
printed_list = []
for item in zip(*final):
	printed_list.append(item)
printed_list.insert(0, ["Overlap with Same Direction", "Overlap with Opposite Direction", "Unique to Eczema", "Unique to Psoriasis"])
printed = ""
for item in printed_list:
	printed += item[0] + "\t" + item[1] + "\t" + item[2] + "\t" + item[3] + "\n"

###Writes to the output file.
output_file = sys.argv[3]
write = open(output_file, "w")
write.write(printed)
write.close()