__author__ = "Jayden Evetts"
__copyright__ = "Copyright 2023, Kaze"
__license__ = "Creative Commons Attribution-ShareAlike 4.0 International License."
__version__ = "1.0"
__email__ = "jayden.evetts@gmail.com"

from yawning_titan.networks.node import Node
from yawning_titan.networks.network import Network

def dijkstra(network:Network):
    distances = []

    for entry_node in network.entry_nodes:
        current_min_node_distances = {entry_node:0}
        current_min_node_distances = explore(network,entry_node,current_min_node_distances)

        distances.append(current_min_node_distances)

    min_node_distances = {node:min([paths[node] for paths in distances]) for node in network.get_nodes()}

    return min_node_distances

def explore(network:Network,start_node:Node,min_node_distances:dict):
    for neighbour in network.neighbors(start_node):
        if neighbour not in min_node_distances.keys():
            min_node_distances[neighbour] = min_node_distances[start_node] + 1
            min_node_distances = explore(network,neighbour,min_node_distances)

    return min_node_distances