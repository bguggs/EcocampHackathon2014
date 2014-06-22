#!/usr/bin/python

import csv
import time
import random
"""
This library contains some functions you may find useful when working with the
given data.  Feel free to modify this to be more general and/or to point to 
other data you're looking at.  Or feel free not to use these at all if you don't
 find them useful.
"""

DATA_FILENAME = "partialNameClean2.csv"

def get_data_list_of_dicts():
    list = []
    counter = 0
    partial = False
    with open(DATA_FILENAME) as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
	    if partial:
		tmp = random.randrange(20)
		if tmp == 13:    
		    list.append(row)
		    counter += 1
	    else:    
		list.append(row)
    return list

def get_headers():
    with open(DATA_FILENAME) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
    return headers

def write_data_dicts(filename, headers, rows_list_of_dicts):
    with open(filename,'w') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(rows_list_of_dicts)

def write_data(filename, headers, rows_list_of_lists):
    with open(filename,'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows_list_of_lists)

def get_data_slice(column_name, list_of_dicts):
    list = []
    for dict in list_of_dicts:
        list.append(dict[column_name])
    return list

def get_data_slice_replace(column_name, list_of_dicts, avg):
    list = []
    for dict in list_of_dicts:
	if dict[column_name] == "":
	    list.append(avg)
	else:
	    list.append(dict[column_name])
    return list


def date_convert(date_string):
    date = time.strptime(date_string, "%d/%m/%Y %H:%M:%S") 
    return time.mktime(date)
   
# make doctest work:
def _test():
    import doctest
    result = doctest.testmod()
    if result[0] == 0:
        print "Wahoo! Passed all", result[1], __file__.split('/')[-1], "tests!"
    else:
       print "Rats!"

if __name__ == "__main__": _test()    
