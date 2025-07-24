from typing import Set, Optional, Dict

def site_number(default: int = 200) -> int:
	'''Ask user for desired number of sites'''
	while True:
		try:
			user_input_patch_number = input("""How many sites do you want minimum? Make choice or press Enter for default (200) """).strip()

			if user_input_patch_number == "":
				patch_number = default
				return default

			patch_number = int(user_input_patch_number)

			if patch_number <= 0:
				print("Please enter an integer greater than 0")
			else:
				return patch_number
		
		except ValueError:
			print("Please enter a valid integer")

def fraction_tree(default: float = 0.8) -> float:
	'''Ask user for desired fraction of trees'''
	while True:
		try:
			user_input = input("""Which initial landscape configuration do you want?
			1. All trees
			2. All rocks
			3. Enter a fixed ratio
			Make choice (default = 0.8 tree/rock ratio) """).strip()

			if user_input == "":
				fraction_tree = default
				return fraction_tree

			choice = int(user_input)

			if choice == 1:
				return 1.0
				#fraction_tree = 1.0
			elif choice == 2:
				return 0.0
				#fraction_tree = 0.0
			elif choice == 3:
				user_input_fraction = input("""What fraction of trees do you want? Enter a float between 0.0 and 1.0: default=0.8 """).strip()
				
				fraction_tree = float(user_input_fraction)

				if 0.0 <= fraction_tree <=1.0:
					return fraction_tree
				else:
					print("Enter avalid number between 0.0 and 1.0 \n")
			else:
				print(f"'{user_input}' not recognized, please enter a number that corresponds to one of the options displayed.\n")
			
		except ValueError:
			print(f"'{user_input}' not recognized , please enter a number that corresponds to one of the options displayed.\n")
		except Exception:
			print(f"An unexpected error occurred. Please try again.\n")
	

def firefighter_number(nodes: Set[int]) -> int:
	''' Ask user for desired number of firefighters'''

	default = max(1, len(nodes)//10)

	while True:
		try:
			
			user_input_firefighter_number = input(f"How many firefighters do you want? Enter a positive integer (default = {default}): ").strip()

			if user_input_firefighter_number == "":
				firefighter_number = default
				return firefighter_number
			
			firefighter_number = int(user_input_firefighter_number)			

			if firefighter_number <= 0:
				print("Please enter an integer greater than 0")
			elif firefighter_number > len(nodes):
				print("There can not be more firefighters than nodes")
			else:
				return firefighter_number
	
		except ValueError:
			print("Please enter a valid integer as an input")
		except Exception:
			print(f"An unexpected error occurred. Please try again.\n")

def firefighter_skill(default: int = 5) -> int:
	'''Ask user for desired skill level of firefighters'''
	while True:
		try:
			user_input_firefighter_skill = input("""What average skill level? Enter a float between 1-10 (default=5): """).strip()

			if user_input_firefighter_skill == "":
				user_input_firefighter_skill = default
				return default
			
			firefighter_skill = int(user_input_firefighter_skill)
			
			if 1.0 <= user_input_firefighter_skill <= 10.0:
				return firefighter_skill
			print("Please enter a valid float between 1 and 10")
			
		except ValueError:
			print("Please enter a valid float between 1 and 10 ")
		except Exception:
			print(f"An unexpected error occurred. Please try again.\n")


def number_of_iterations(default: int = 50) -> int:
	'''Ask user for desired number of iterations'''
	while True:
		try:
			user_input_number_iterations = input("""How many iterations do you want? Enter a positive integer (default = 50): """).strip()

			if user_input_number_iterations == "":
				return default

			number_iterations = int(user_input_number_iterations)

			if user_input_number_iterations <= 0:
				print("Please enter an integer greater than 0")
			else:
				return number_iterations
		
		except ValueError:
			print("Please enter a valid integer as an input")
		except Exception:
			print(f"An unexpected error occurred. Please try again.\n")


def probabilities(default_combustion: float = 0.1,
				  default_transmission: float = 0.5,
				  default_respawn: float = 0.1) -> Dict[str,float]:
	'''Ask user for desired probabilities'''
	while True:
		try:
			user_input_combustion = input("Probability of tree self combustion? Enter a float between 0 and 1 (default=0.1): ").strip()
			if user_input_combustion == "":
				combustion = default_combustion
			else:
				combustion = float(user_input_combustion)
				if not (0.0 <= combustion <= 1.0 and combustion >= 0.0):
					print("Please enter a valid non-negative probability between 0 and 1")
					continue
			
			user_input_transmission = input("Probability of fire transmission?: Enter a float between 0 and 1 (default = 0.5): ").strip()
			if user_input_transmission == "":
				transmission = default_transmission
			else:
				transmission = float(user_input_transmission)
				if not (0.0 <= transmission <= 1.0 and transmission >= 0.0):
					print("Please enter a valid non-negative probability between 0 and 1")
					continue
			
			user_input_respawn = input("Probability rock to tree conversion?: Enter a float between 0 and 1 (default = 0.1): ").strip()
			if user_input_respawn == "":
				respawn = default_respawn
			else:
				respawn = float(user_input_respawn)
				if not (0.0 <= respawn <= 1.0 and respawn >= 0.0):
					print("Please enter a valid non-negative probability between 0 and 1")
					continue

			return {"combustion": combustion, "transmission": transmission, "respawn": respawn}
		
		except ValueError:
			print("Please enter valid float probabilities between 0 and 1")
