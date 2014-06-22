import get_data as gd
import get_data2 as gd2
import get_data3 as gd3

list_of_dicts = gd.get_data_list_of_dicts()
full = gd2.get_data_list_of_dicts()
full_headers = gd2.get_headers()
headers = gd.get_headers()
headers_income = gd3.get_headers()

codes = {}
full_clean = []
final_headers = []

for h in headers:
    h = h.split(" - ")
    code = h[0]
    try:
	name = h[1]
	codes[code] = name
    except:
	print h

for h2 in headers_income:
    h2 = h2.split(" - ")
    code = h2[0]
    try:
	if not "Error" in h2[1]:
	    name = h2[1]
	    codes[code] = name
    except:
	print h2

for entry in full:
    temp = {}
    for h1 in full_headers:
	try:
	    temp[codes[h1]] = entry[h1]
	    if not codes[h1] in final_headers:
		final_headers.append(codes[h1])
	except:
	    if not  h1[len(h1)-1] == "e":
		temp[h1] = entry[h1]
		if not h1 in final_headers:
		    final_headers.append(h1)

    full_clean.append(temp)

filename = "partialNameClean2.csv"
headers = final_headers

gd.write_data_dicts(filename,headers,full_clean)
