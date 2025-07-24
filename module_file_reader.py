from typing import List, Tuple

def input_file_read() -> List[Tuple[int,int]]:
	'''
	Create list of edges from a file located in a user-defined location.

	Returns:
	List of edges
	'''
	while True:
		try:
			#Create empty list
			edges = []
			
			path = input("""Input system data file location: """).strip()

			#Read file and create list of edges
			with open(path, 'r') as filestream:
				for line in filestream:
					line = line.strip()
					if line and not line.startswith('#'): #Checks if the line is empty and if the line starts with a '#'.
						line =  line.split(',') #Splits line into parts when it encounters ','. Returns list of strings
						if len(line) == 2 and all(line):
							edge = tuple(map(int, line)) #Converts each list into a tuple. Map converts each element of the list to an int.
							edges.append(edge) #Appends tuple to list

			#Check if edges list is empty. If yes, skip rest of while loop and start over.
			if not edges:
				print(f"Chosen file produced no edges. Is the file the correct format? Or is it empty?")
				continue

			return edges
		
		except FileNotFoundError:
			print(f"File was not found. Enter a valid file path.")

		except UnicodeDecodeError:
			print(f"File could not be read. Try another file format.")

		except Exception:
			print(f'An error has occured. Beaware that the number of points must be larger than 3')