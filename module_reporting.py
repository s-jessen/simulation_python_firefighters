from typing import List
import matplotlib.pyplot as plt

def static_graph(
		number_of_iterations: int,
		fire_history: List[int],
		tree_history: List[int],
		rock_history: List[int]
		) -> None:
	'''
	Visualize population history from simulation.
	'''
	# Create x-axis values (iterations)
	iterations = list(range(1, number_of_iterations + 1))

	# Plot the data
	plt.plot(iterations, fire_history, label='Fire History', color='red')
	plt.plot(iterations, tree_history, label='Tree History', color='green')
	plt.plot(iterations, rock_history, label='Rock History', color='gray')

	# Add labels and title
	plt.xlabel('Iteration')
	plt.ylabel('Population')
	plt.title('Evolution Over Time')

	# Add legend
	plt.legend()

	# Show the plot
	plt.show()