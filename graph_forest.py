"""
graph_forest.py

Main entry point for the Fire Simulation project.
Handles user interaction, environment configuration, and simulation execution.

Author: Søren Jessen
Course: Introduction to Programming (SDU, 2023)
"""

import module_user_input as user_input
import module_configuration as configuration
import module_simulation as simulation
import module_reporting as reporting
import visualiser_random_forest_graph as vr

def menu_main() -> None:
	""" Create main menu of the program in which users can select 
	to read the graph data from a file or random generation"""

	while True:
		try:
			user_option = input("Enter your choice (default = Randomly generated): ").strip()

			if user_option == "":
				edges, pos = configuration.generate_random_graph()

			option = int(user_option)

			if option == 1: #Load
				edges = configuration.read_from_file()

			elif option == 2: #Random
				edges, pos = configuration.generate_random_graph()
				
			elif option == 9: #Exit
				print('Bye')
				break
			else:
				print(f"""'{option}' not recognised, please enter a number 
	that corresponds to one of the options displayed.""")

		except ValueError:
			print(f"Please enter a valid integer choice")

		#Identify unique nodes
		nodes = configuration.unique_nodes(edges)

		#Landscape pattern (create initial color map)
		fraction_tree = user_input.fraction_tree()	

		#Probabilities (combustion, fire transmission, rock->tree respawn)
		probabilities = user_input.probabilities()

		#Iterations
		number_of_iterations = user_input.number_of_iterations()

		#Create initial color map
		cmap = configuration.create_color_map(nodes, fraction_tree)
		
		#Assign nodes to appropriate classes
		land_patches = configuration.create_land_patches(cmap, nodes, edges)

		#Initialize firefighters
		firefighters = configuration.create_firefighters(nodes)
		
		#Initialize graph
		if pos is not None:
			graph = vr.Visualiser(edges, pos_nodes=pos, vis_labels=True)
		else:
			graph = vr.Visualiser(edges, vis_labels=True)

		graph.update_node_colours(cmap)
		graph.update_node_edges([firefighter.position for firefighter in firefighters.keys()])
		
		#Run simulation (and store history lists)
		fire_history, tree_history, rock_history = simulation.visualization(
			graph, edges, probabilities, firefighters, land_patches, cmap, number_of_iterations)

		#Create static graph with simulation results
		reporting.static_graph(number_of_iterations,
							fire_history,
							tree_history,
							rock_history)
	
		exit(0)

if __name__ == '__main__':
  print("""Welcome to the Graph Creator.
You have the following options for landscape designing. 
1) Load terrain data from file.
2) Use randomly generated data.
9) Quit.""")
  menu_main()
	

