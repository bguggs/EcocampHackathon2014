import get_data as gd

headers_clean = gd.get_headers()
list_of_dicts = gd.get_data_list_of_dicts()

new_headers = []
for h in headers_clean:
    h = h.split(",")
    if not " Error" in h and not "" in h:
	new_headers.append(",".join(h))


final = []
for entry in list_of_dicts:
    temp = {}
    for header in new_headers:
	temp[header] = entry[header]

    final.append(temp)

filename = "noError.csv"
headers = new_headers
gd.write_data_dicts(filename,headers,final)
