#!/usr/bin/python

import csv
import time

"""
This library contains some functions you may find useful when working with the
given data.  Feel free to modify this to be more general and/or to point to 
other data you're looking at.  Or feel free not to use these at all if you don't
 find them useful.
"""

DATA_FILENAME = "../py_scripts/no_litter.csv"

def get_data_list_of_dicts_for_scale(scale):
    list = []
    with open(DATA_FILENAME) as f:
        f_csv = csv.DictReader(f)
	for row in f_csv:
	    list.append(row)
            if len(list) == scale:
                break
    return list

def get_data_list_of_dicts():
    list = []
    with open(DATA_FILENAME) as f:
        f_csv = csv.DictReader(f)
	for row in f_csv:
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

def get_data_slice_final_tone(column_name, list_of_dicts):
    list = []
    for dict in list_of_dicts:
	if dict[column_name] == "None":
        	list.append(0)
	elif dict[column_name] == "D":
        	list.append(3.0/7)
    	elif dict[column_name] == "C":
        	list.append(4.0/7)
	elif dict[column_name] == "G":
        	list.append(1)
	elif dict[column_name] == "A":
        	list.append(6.0/7)
	elif dict[column_name] == "F":
        	list.append(1.0/7)
	elif dict[column_name] == "E":
        	list.append(2.0/7)
	elif dict[column_name] == "B-flat":
        	list.append(5.0/7)
	elif dict[column_name] == "":
        	list.append(0)
    return list


def get_data_slice_roles(column_name, list_of_dicts):
    list = []
    for dict in list_of_dicts:
	if dict[column_name] == "None":
	    list.append(0)
	elif dict[column_name] == "S":
	    list.append(1.0)
	elif dict[column_name] == "T":
	    list.append(0.5)
	elif dict[column_name] == "B":
	    list.append(0.25)
	elif dict[column_name] == "Ct":
	    list.append(0.75)
	elif dict[column_name] == "":
	    list.append(0)
	else:
	    list.append(0)
    return list

def get_data_slice_repeat_kind(column_name, list_of_dicts):
    list = []
    for dict in list_of_dicts:
	if dict[column_name] == "None":
	    list.append(0)
	elif dict[column_name] == "Final Repeat":
	    list.append(0.25)
	elif dict[column_name] == "Direct Repeat":
	    list.append(0.5)
	elif dict[column_name] == "Da Capo":
	    list.append(0.75)
	elif dict[column_name] == "Refrain":
	    list.append(1.0)
	elif dict[column_name] == "":
	    list.append(0)
    return list

def get_data_slice_cadence_type(column_name, list_of_dicts):
    list = []
    for dict in list_of_dicts:
	if dict[column_name] == "Plagal":
	    list.append(0.2)
	elif dict[column_name] == "Authentic":
	    list.append(0.4)
	elif dict[column_name] == "CadInCad":
	    list.append(0.6)
	elif dict[column_name] == "CAD NDLT":
	    list.append(0.8)
	elif dict[column_name] == "Phrygian":
	    list.append(1.0)
	elif dict[column_name] == "NoCadence":
	    list.append(0)
	elif dict[column_name] == "None":
	    list.append(0)
	elif dict[column_name] == "":
	    list.append(0)
    return list

def get_data_slice_text(column_name, list_of_dicts):
    list = []
    for dict in list_of_dicts:
	if dict[column_name] == "None":
	    list.append(0)
	elif dict[column_name] == "Text Pause":
	    list.append(0.2)
	elif dict[column_name] == "Text Overlap":
	    list.append(0.4)
	elif dict[column_name] == "Text Declamation":
	    list.append(0.6)
	elif dict[column_name] == "Text Representation":
	    list.append(0.8)
	elif dict[column_name] == "Text Enjabment":
	    list.append(1.0)
	elif dict[column_name] == "":
	    list.append(0)
	else:
	    list.append(0)
    return list

def get_data_slice_exact_or_varied(column_name, list_of_dicts):
    list = []
    for dict in list_of_dicts:
	if dict[column_name] == "Varied":
	    list.append(0.5)
	elif dict[column_name] == "Exact":
	    list.append(1.0)
	elif dict[column_name] == "None":
	    list.append(0)
	elif dict[column_name] == "":
	    list.append(0)
	else:
	    list.append(0)
    return list

def get_data_slice_cadence(column_name, list_of_dicts):
    list = []
    for dict in list_of_dicts:
	if dict[column_name] == "True":
	    list.append(1)
	elif dict[column_name] == "False":
	    list.append(0)
	elif dict[column_name] == "None":
	    list.append(0)
	elif dict[column_name] == "":
	    list.append(0)
	elif dict[column_name] == "Yes":
	    list.append(1)
    return list	

def get_data_slice_numbers(column_name, list_of_dicts):
    list = []
    for dict in list_of_dicts:
	if dict[column_name] == "None":
	    list.append(0)
	elif dict[column_name] == "":
	    list.append(0)
	else:
	    list.append(dict[column_name])
    return list	

def get_data_slice_pres(column_name, list_of_dicts):
    list = []
    for dict in list_of_dicts:
	if dict[column_name] == "HR Simple":
	    list.append(0.10)
	elif dict[column_name] == "HR Stagger":
	    list.append(0.15)
	elif dict[column_name] == "None":
	    list.append(0)
	elif dict[column_name] == "":
	    list.append(0)
	elif dict[column_name] == "FI":
	    list.append(0.3)
	elif dict[column_name] == "HR Fauxbourdon":
	    list.append(0.05)
	elif dict[column_name] == "PEn":
	    list.append(0.4)
	elif dict[column_name] == "PEn Tonal":
	    list.append(0.45)
	elif dict[column_name] == "NIM":
	    list.append(0.6)
	elif dict[column_name] == "HR Dance":
	    list.append(0.25)
	elif dict[column_name] == "PEn Stacked":
	    list.append(0.5)
	elif dict[column_name] == "ID":
	    list.append(0.7)
	elif dict[column_name] == "HR Dactyll":
	    list.append(.20)
	else:
	    list.append(0)
    return list

def get_data_slice_phrase_num(column_name, list_of_dicts):
    list = []
    for dict in list_of_dicts:
	if dict[column_name] == "HR Simple":
	    list.append(.9)
	elif dict[column_name] == "HR Stagger":
	    list.append(8)
	elif dict[column_name] == "None":
	    list.append(0)
	elif dict[column_name] == "":
	    list.append(0)
	elif dict[column_name] == "FI":
	    list.append(0.7)
	elif dict[column_name] == "HR Fauxbourdon":
	    list.append(0.6)
	elif dict[column_name] == "PEn":
	    list.append(0.5)
	elif dict[column_name] == "PEn Tonal":
	    list.append(0.4)
	elif dict[column_name] == "NIM":
	    list.append(0.3)
	elif dict[column_name] == "HR Dance":
	    list.append(0.2)
	elif dict[column_name] == "PEn Stacked":
	    list.append(0.1)
	else:
	    list.append(0)
    return list



def get_data_slice(column_name, list_of_dicts):
    list = []
    for dict in list_of_dicts:
        list.append(dict[column_name])
    return list

def date_convert(date_string):
    date = time.strptime(date_string, "%d/%m/%Y %H:%M:%S") 
    return time.mktime(date)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def column_to_numbers(column_data):
    new_column = []
    for i in range(len(column_data)):
	new_column.append(float(column_data[i]))
    return new_column
  
# make doctest work:
def _test():
    import doctest
    result = doctest.testmod()
    if result[0] == 0:
        print "Wahoo! Passed all", result[1], __file__.split('/')[-1], "tests!"
    else:
       print "Rats!"

if __name__ == "__main__": _test()	
