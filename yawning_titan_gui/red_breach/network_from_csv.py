__author__ = "Jayden Evetts"
__copyright__ = "Copyright 2023, Kaze"
__license__ = "Creative Commons Attribution-ShareAlike 4.0 International License."
__version__ = "1.0"
__email__ = "jayden.evetts@gmail.com"

import random
import json

from yawning_titan.networks.node import Node
from yawning_titan.networks.network import Network
from yawning_titan_gui.red_breach.retrieve_cpe_from_azure import retrieve_csv_vulnerabilities

def normalise(min_val:float,max_val:float,val:float): #normalises to a val between 0 and 1
    val -= min_val
    val /= (max_val - min_val)

    return val

def find_highest_vulnerability(cpe_list:list,cpe_vuln_dict:dict,min_val = 0,max_val = 1):
    max_vulnerability = 0

    for cpe in cpe_list:
        if cpe_vuln_dict.get(cpe):
            current_vulnerability = cpe_vuln_dict.get(cpe)

        else:
            current_vulnerability = 0.01

        max_vulnerability = max(max_vulnerability,current_vulnerability)

    return normalise(min_val,max_val,max_vulnerability)

def generate_network(csv_json_str:str,fetch_vulnerabilities:bool = False,generate_node_positions:bool = False):
    """
    Configures a network from a CSV file. The config file should be
    in the format:

    nodeID,xGraphLocation,yGraphLocation,isEntryNode,isHighValue,cpe,connections

    where the 'cpe'  column is a list of the node's CPEs separated by the '|' 
    character, and the 'connections' column is a a list of nodeIDs separated by
    commas. See example_network.csv

    Args:
        csv_path: Path to CSV config file
        generate_node_positions: Whether the positions should be generated 
        automatically or not. Overrides any positions specified in the config
        if set to True.
        fetch_vulnerabilities: Whether to retrieve vulnerability scores from
        azure or to randomly generate them.

    Returns:
        Network
    """

    csv_str = json.loads(csv_json_str)
    csv_lines = csv_str.replace("\r","").split("\n")

    nodes = {}
    nodes_csv = {}

    num_high_value_targets = 0

    for line in csv_lines[1:]:
        split_line = line.replace("\n","").split(",")
        nodeID = split_line[0]
        nodes_csv[nodeID] = split_line

        if fetch_vulnerabilities: 
            cpe_vuln_dict = retrieve_csv_vulnerabilities(num_rows = 50000) #gets the table of CPE vulnerabilities from the server
            node_vulnerability = find_highest_vulnerability(split_line[5].split("|"),cpe_vuln_dict) #finds the highest vulnerability of the CPEs attached to the node

        else: node_vulnerability = random.random()        

        if split_line[4] == "T": num_high_value_targets += 1

        nodes[nodeID] = Node(name = split_line[0],
                             entry_node = (split_line[3] == "T"),
                             high_value_node = (split_line[4] == "T"),
                             vulnerability = node_vulnerability)

    net = Network()
    net.num_of_random_high_value_nodes = num_high_value_targets

    for node in nodes.keys(): #adds each node from the csv file to the new network
        net.add_node(nodes[node])

    for node in nodes_csv.keys(): #adds an edge to all extra arguments at the end of the node's csv line
        for connected_node in nodes_csv[node][6:]:
            net.add_edge(nodes[node],nodes[connected_node])

    if not generate_node_positions:
        for node in nodes.keys(): #x and y positions must be set after adding nodes to the network since it regenerates positions when changed
            nodes[node].x_pos = float(nodes_csv[node][1])
            nodes[node].y_pos = float(nodes_csv[node][2])

    return net