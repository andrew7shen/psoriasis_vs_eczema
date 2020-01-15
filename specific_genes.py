#Andrew Shen
import sys
import re

###To run this program, go to the command line and specify five parameters:
###python specific_genes.py comparison.txt combined_genes.txt final.txt

###Sets the two input files to different variables: "comparison" and "combined".
input_file = sys.argv[1]
read = open(input_file, "r")
comparison_initial = read.read()

input_file = sys.argv[2]
read = open(input_file, "r")
combined_initial = read.read()

###Changes "comparison" to a list of gene names.
comparison_newline = comparison_initial.splitlines()
comparison_tab = []
for item in comparison_newline:
	comparison_tab.append(item.split("\t"))
del comparison_tab[0]
comparison_space = []
for item in comparison_tab:
	for value in item:
		comparison_space.append(value.split(" "))
comparison_space = [x for x in comparison_space if x != ["."]]
comparison = []
for item in comparison_space:
	if len(item) == 1:
		comparison.append(item)
	else:
		comparison.append(item[0])
genelist = []
for item in comparison:
	if type(item) is list:
		genelist.append(item[0])
	else:
		genelist.append(item)

###Matches "genelist" with the normalized data in "combined"
combined_newline = combined_initial.splitlines()
combined_tab = []
for item in combined_newline:
	combined_tab.append(item.split("\t"))
heading1 = combined_tab[0]
heading2 = combined_tab[1]
combined_dict = {}
for item in combined_tab:
	combined_dict[item[0]] = item[1:len(item)]
final = []
for item in genelist:
	for key in combined_dict:
		if item == key:
			final.append([item, combined_dict[key]])
for item in final:
	for value in item[1]:
		item.append(value)
	del item[1]
final.insert(0, heading1)
final.insert(1, heading2)

final_printed = ""
for item in final:
	for value in item:
		final_printed += str(value) + "\t"
	final_printed += "\n"

###Writes to the output file.
output_file = sys.argv[3]
write = open(output_file, "w")
write.write(final_printed)
write.close()

