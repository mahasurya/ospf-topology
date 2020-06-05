import re
import networkx as nx
import sys
import json
from datetime import datetime

devices_list=[]
ospf_list=[]
path = '/home/admapp/surya/ospf/'

file = open(path + 'OSPF_0_region.dot','r')
for line in file:

    if not '>' in line:

        id_rex = re.match (r"\s+(\S+)\s+\[label\=\"(\S+)\\n(\S+)\"",line)
        id_rex2 = re.match (r"\s+(\S+)\s+\[label\=\"(\d+\.\d+\.\d+\.\d+)\"",line)
        if id_rex:
            my_id = (id_rex.group(1),id_rex.group(2),id_rex.group(3))
            devices_list.append(my_id) # add this device object to list
        elif id_rex2:
            my_id = (id_rex2.group(1),id_rex2.group(2))
            devices_list.append(my_id) # add this device object to list

    else:

        id_rex3 = re.match (r"\s+(\S+)\s+\-\>\s+(\S+)\[label\=\"(\d+)\"",line)
        host_a = ""
        host_b = ""

        if id_rex3.group(1):
            for x in devices_list:
                if x[0] == id_rex3.group(1):
                    host_a = x[-1]

        if id_rex3.group(2):
            for x in devices_list:
                if x[0] == id_rex3.group(2):
                    host_b = x[-1]
        cost = int(id_rex3.group(3))

        if 'color' in line:
            temp = (host_a, host_b, cost)
            ospf_list.append(temp) # add this device object to list
        elif 'none' in line:
            temp = (host_a, host_b, cost)
            ospf_list.append(temp) # add this device object to list
            temp = (host_b, host_a, cost)
            ospf_list.append(temp) # add this device object to list

file.close() # Close the file since we are done with it

H = nx.MultiDiGraph()
H.add_weighted_edges_from(ospf_list)

path = dict(nx.all_pairs_dijkstra_path_length(H))
cost = dict(nx.all_pairs_dijkstra_path(H))

temp_list = []

for key,val in path.items():
	for key1,val1 in val.items():
		#my_list = ["\"source\":\""+str(key)+"\""]
		now = datetime.now()
		my_dict = {'source_router':str(key), 'destination_router':str(key1), 'cost':str(val1), 'path':str(cost[key][key1]), 'timestamp':now.strftime("%Y-%m-%dT%H:%M:%S")}
		temp_list.append(my_dict)

y=json.dumps(temp_list)

print y
