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
		if row == s[0][0]:
			row_action = "start row"
		if row == s[0][1]:
			row_action = "end row"
		if row >= s[0][0] and row <= s[0][1] and col == s[1][0]:
			col_action = "start col"
		if row >= s[0][0] and row <= s[0][1] and col == s[1][1]:
			col_action = "end col"
	return [row_action, col_action]

def getclines(row):
	start_row_string = ""
	end_row_string = ""
	i = 1
	for c in row:
		if c[0] == "start row" and c[1] == "start col":
			start_row_string = start_row_string + r"\cline{" + str(i) + "-"
		if c[0] == "start row" and c[1] == "end col":
			start_row_string = start_row_string + str(i) +"}"
		if c[0] == "end row" and c[1] == "start col":
			end_row_string = end_row_string + r"\cline{" + str(i) + "-"
		if c[0] == "end row" and c[1] == "end col":
			end_row_string = end_row_string + str(i) +"}"
		i += 1
	return start_row_string, end_row_string

#rows = number of rows in main table
#cols = number of columns in main table
#sub_tables: [[row_start, row_end], [col_start, cold_end]]
def makeDRS3(rows, cols, sub_tables=[]):
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
	for row in tablegrid:
		start_row_string, end_row_string = getclines(row)
		if len(start_row_string) > 1:
			print start_row_string
		row_string = ""
		i = 1
		for c in row:
			if i > 1:
				if c[1] != "start col" and c[1] != "end col":
					row_string = row_string + "& "
				if c[1] == "start col":
					row_string = row_string + r"& \multicolumn{1}{|c}{}"
				if c[1] == "end col":
					row_string = row_string + r"& \multicolumn{1}{c|}{}"
			i += 1
		row_string = row_string + r"\\"
		print row_string
		if len(end_row_string) > 1:
			print end_row_string
	print "\\hline"
	print "\\end{tabular}"


sub_tables = []

#cols = 5
#rows = 9
#sub_tables = [[[2, 4],[2,4]], [[6,8],[2,4]]]

#print args

cols = int(args.cols)
rows = int(args.rows)
try:
	sub_tables = eval(args.subtables)
except:
	print "ERROR: improper format sub table"

makeDRS3(rows, cols, sub_tables)




