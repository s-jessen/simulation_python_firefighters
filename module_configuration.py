import random
import classes
from typing import List, Tuple, Dict, Set, Union
import graph_helper as gh
import module_user_input as user_input
import module_file_reader as fr

def generate_random_graph() -> Tuple[List[Tuple[int, int]], Dict[int, Tuple[float, float]]]:
	'''
	Retrieve user input for number of nodes and generate a random graph.

	returns: edges, pos
	'''
	min_site_number = user_input.site_number()
	edges, pos = gh.voronoi_to_edges(min_site_number)
	return edges, pos

def read_from_file() -> Tuple[List[Tuple[int, int]], Dict[int, Tuple[float, float]]]:
	'''
	Read edges from file and generate positions for nodes.

	returns: edges, pos
	'''
	while True:
		try: 
			# Read edges from file
			edges = fr.input_file_read()

			# Check if the graph is planar
			is_planar = gh.edges_planar(edges)
			
			if is_planar:
				return edges
			else:
				print("The graph defined by the edges is not planar. Please try again.")
		except Exception:
			print(f"Error")

def create_color_map(nodes: [Set], fraction_tree: float) -> Dict[int, int]:
	'''
	Create initial color map for nodes in graph with random colors.
	
	returns: dictionary with node id as keys and color values as values
	'''
	cmap = {node:random.randint(0, 256) for node in 
			random.sample(list(nodes),int(fraction_tree*len(nodes)))}

	return cmap

def neighbor_id(edges: List[Tuple[int, int]]) -> Dict[int, List[int]]:
		'''
		Return ID of the neighbors to the present patch.
		'''
		nodes = unique_nodes(edges)

		neighbor_dict = {}

		for node in nodes:
			list_of_neighbors = []
			for edge in edges:
				if node in edge and edge[0] not in list_of_neighbors and edge[1] not in list_of_neighbors:
					list_of_neighbors.append(edge[0] if edge[1] == node else edge[1])
			neighbor_dict[node] = list_of_neighbors
		
		return neighbor_dict

def unique_nodes(edges: List[Tuple[int,int]]) -> Set[int]:
	'''
	Return unique nodes from list of edges.

	returns: set of unique nodes
	'''
	#From "edges" list of tuples, extract every integer (node)
	all_nodes = []
	for x in edges:
		all_nodes.append(x[0])
		all_nodes.append(x[1])
	
	#Identify unique nodes by converting list of all nodes to a set	
	unique_nodes = set(all_nodes)
	return unique_nodes

def create_land_patches(cmap: Dict[int, int], nodes: Set[int], edges: List[Tuple[int,int]]) -> Dict[int, Union[classes.Treepatch, classes.Rockpatch]]:
	'''
	Create land patches (treepatches and rockpatches) with node as id.

	returns: dictionary of land patches (objects of class Treepatch or Rockpatch)
	'''
	neighbor_dict = neighbor_id(edges)

	land_patches = {node:classes.Treepatch(id = node, treestats = cmap[node], neighbors = neighbor_dict[node]) if node in cmap.keys()
					 else classes.Rockpatch(id = node, neighbors = neighbor_dict[node], fire = False) for node in nodes}
	
	return land_patches

def create_firefighters(nodes: Set[int]) -> Dict[classes.Firefighter, int]:
	'''
	Create user selected number of firefighters of class Firefighter
	with random starting position.
	
	Assign skill from a normal distribution around the user selected level.
	
	returns: Dictionary of firefighters (objects of class Firefighter)
	'''
	firefighter_number = user_input.firefighter_number(nodes)
	firefighter_skill = user_input.firefighter_skill()
	firefighter_positions = random.sample(list(nodes), firefighter_number)
	
	#Create dictionary of firefighters. Values are current position
	firefighters = {
		classes.Firefighter(skill=random.gauss(
			mu=firefighter_skill, sigma=2.0), position=position): position
			  for position in firefighter_positions
			  }

	return firefighters

