import classes
import visualiser_random_forest_graph as vr
from typing import List, Tuple, Dict, Union

def visualization(
		graph: vr.Visualiser,
		edges: List[Tuple[int, int]],
		probabilities: Dict[str, float],
		firefighters: Dict[classes.Firefighter, int],
		land_patches: Dict[int, Union[classes.Treepatch, classes.Landpatch]],
		cmap: Dict[int, int],
		number_of_iterations: int
		) -> Tuple[List[int], List[int], List[int]]:
	'''
	Visualize the simulation and return the population history.

	returns: fire_history, tree_history, rock_history
	'''
	
	#initialize iteration count
	iteration = 1
	
	#Create variables to keep track of landpatch and fire populations
	fire_history = []
	tree_history = []
	rock_history = []

	#Run simulation
	while graph.is_open() and iteration <= number_of_iterations:
		iteration += 1
		update(edges,
				probabilities,
				graph,
				firefighters,
				land_patches,
				cmap,
				fire_history,
				tree_history,
				rock_history)
	graph.close()

	return fire_history, tree_history, rock_history

def update(
		edges: List[Tuple[int, int]],
		probabilities: Dict[str, float],
		graph: vr.Visualiser,
		firefighters: Dict[classes.Firefighter, int],
		land_patches: Dict[int, Union[classes.Treepatch, classes.Landpatch]],
		cmap: Dict[int, int],
		fire_history: List[int],
		tree_history: List[int],
		rock_history: List[int]
		) -> None:
	'''
	Update firefighter positions, tree patch health, fire spread,
	rock to tree conversions, tree to rock conversions, and color map.

	Returns: None
	'''
	#Move firefighters
	move_firefighters(firefighters, land_patches)

	#Update land_patches
	update_land_patches(land_patches, probabilities, cmap, firefighters)

	#Store population history for static graph
	population_history(land_patches, fire_history, tree_history, rock_history)

	#Update cmap
	update_color_map(land_patches, cmap)

	#Update graph color and firefighter positions
	graph.update_node_colours(cmap)
	graph.update_node_edges([firefighter.position for firefighter in firefighters.keys()])

def move_firefighters(
		firefighters: Dict[classes.Firefighter, int],
		land_patches: Dict[int, Union[classes.Treepatch, classes.Landpatch]]
		) -> None:
	'''
	Move firefighter positions and return an updated firefighter dictionary.

	Returns: None
	'''
	for firefighter in firefighters.keys():
		firefighter.movement(land_patches)
		firefighters[firefighter] = firefighter.position

def update_land_patches(
		land_patches: Dict[int, Union[classes.Treepatch, classes.Landpatch]],
		probabilities: Dict[str, float],
		cmap: Dict[int, int],
		firefighters: Dict[classes.Firefighter, int]
		) -> None:
	'''
	Update land patches and color map.

	returns: None
	'''
	# Update land_patches
	for patch in land_patches.values():
		#Update rock to tree conversions
		if isinstance(patch, classes.Rockpatch):
			patch.mutate(land_patches, probabilities, cmap)
		elif isinstance(patch, classes.Treepatch):
			#Update spontaneous combustion
			patch.combustion(probabilities)
			#Update treestats
			patch.updateland(firefighters, land_patches, cmap)
			#Update colors
			cmap[patch.id] = patch.treestats
			#Update fire spread
			if patch.fire is True:
				patch.transmission(probabilities)

def population_history(
		land_patches: Dict[int, Union[classes.Treepatch, classes.Landpatch]],
		fire_history: List[int],
		tree_history: List[int],
		rock_history: List[int]
		) -> None:
	'''
	Add current population to population history lists.

	Returns: None
	'''
	fire_history.append(len([1 for element in land_patches.values() if isinstance(element, classes.Treepatch) and element.fire is True]))
	tree_history.append(len([1 for element in land_patches.values() if isinstance(element, classes.Treepatch)]))
	rock_history.append(len([1 for element in land_patches.values() if isinstance(element, classes.Rockpatch)]))

def update_color_map(
		land_patches: Dict[int, Union[classes.Treepatch, classes.Landpatch]],
		cmap: Dict[int, int]
		) -> None:
	'''
	Update color map.

	Returns: None
	'''
	for patch in land_patches.values():
		if isinstance(patch, classes.Treepatch):
			cmap[patch.id] = patch.treestats