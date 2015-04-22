#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description='Generate Latex DRS tabulars from command line')
parser.add_argument('--cols',
    help="Number of cols in main table")
parser.add_argument('--rows',
    help="Number of cols in main table")
parser.add_argument('--subtables',
    help="subtabes in main table e.g. (no spaces) [[[2, 4],[2,4]],[[6,8],[2,4]]]")


args = parser.parse_args()

def check_subtables(row, col, sub_tables):
	row_action = ""
	col_action = ""
	for s in sub_tables:
		#if row == s[0][0]:
		#	row_action = "start row"
		if row >= s[0][0] and row <= s[0][1] and col == s[1][0]:
			col_action = "start col"
			if row == s[0][0]:
				row_action = "start row"
			if row == s[0][1]:
				row_action = "end row"
		if row >= s[0][0] and row <= s[0][1] and col == s[1][1]:
			col_action = "end col"
			if row == s[0][0]:
				row_action = "start row"
			if row == s[0][1]:
				row_action = "end row"
	return [row_action, col_action]

def getclines(row):
	start_row_string = ""
	end_row_string = ""
	started = False
	i = 1
	#print row
	for c in row:
		if c[0] == "start row" and c[1] == "start col" and started == False:
			start_row_string = start_row_string + r"\cline{" + str(i) + "-"
			started = True
		if c[0] == "start row" and c[1] == "end col" and started == True:
			start_row_string = start_row_string + str(i) +"}"
			started = False
		if c[0] == "end row" and c[1] == "start col" and started == False:
			end_row_string = end_row_string + r"\cline{" + str(i) + "-"
			started = True
		if c[0] == "end row" and c[1] == "end col" and started == True:
			end_row_string = end_row_string + str(i) +"}"
			started = False
		i += 1
	return start_row_string, end_row_string

#rows = number of rows in main table
#cols = number of columns in main table
#sub_tables: [[row_start, row_end], [col_start, col_end]]
def makeDRS3(rows, cols, sub_tables=[], index=True):
	r = 1
	header_cols = "".join(["c " for i in range(0, cols+1)]).strip()
	header_line = "\\begin{tabular}{|" + header_cols + "|}"
	tablegrid = []
	for rownum in range(0, rows+1):
		row = []
		for colnum in range(0, cols+1):
			row.append(check_subtables(rownum, colnum, sub_tables))
		tablegrid.append(row)
	print tablegrid
	print header_line
	print "\\hline"
	print "\multicolumn{" + str(len(tablegrid[0])) + "}{|c|}{} \\\\"
	print "\\hline"
	j = 0
	for row in tablegrid:
		j += 1
		start_row_string, end_row_string = getclines(row)
		if len(start_row_string) > 1:
			print start_row_string
		row_string = ""
		i = 1
		lastc = ["", ""]
		for c in row:
			if i > 1:
				if c[1] != "start col" and c[1] != "end col":
					if index == True and j == rows + 1:
						row_string = row_string + "& " + str(i) + " " 
					else:
						row_string = row_string + "& " 
				if c[1] == "start col":
					row_string = row_string + r"& \multicolumn{1}{|c}{}"
				if lastc[1] == "end col" and i == len(row):
					row_string = row_string + r"& \multicolumn{1}{|c|}{}"
				elif lastc[1] == "end col":
					row_string = row_string + r"& \multicolumn{1}{|c}{}"
				lastc = c
			i += 1
		row_string = row_string + r"\\"
		print row_string
		if len(end_row_string) > 1:
			print end_row_string
	print "\\hline"
	print "\\end{tabular}"


sub_tables = []

#cols = 9
#rows = 18
#sub_tables = [[[2, 14],[2,8]], [[5,8],[4,6]], [[10,13],[4,6]]]

#print args

cols = int(args.cols)
rows = int(args.rows)
try:
	sub_tables = eval(args.subtables)
except:
	print "ERROR: improper format sub table"

makeDRS3(rows, cols, sub_tables)




