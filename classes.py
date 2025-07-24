import random
from typing import List, Dict, Union

class Landpatch:
	'''
	Represents a land patch in a graph.

	Attributes:
		id (int): Unique identifier for the land patch.
		neighbors (List[int]): List of neighbor patch IDs.
		fire (bool): Whether the patch is on fire.

	'''
	def __init__(self, id: int, neighbors: List[int], fire: bool = False) -> None:
		self.id = id
		self.neighbors = neighbors
		self.fire = fire

	def get_neighbors(self) -> List[int]:
		''' 
		Returns list of neighbors
		'''
		return (self.neighbors)
	
	def __repr__(self) -> str:
		return f"Landpatch({self.id})"

class Rockpatch(Landpatch):
	'''
	Subclass of Landpatch representing a rock patch in a graph.

	Attributes:
	id (int): Unique identifier for the rock patch.
	'''
	def __init__(self, id, neighbors, fire) -> None:
		super().__init__(id, neighbors, fire)

	def mutate(self, land_patches: Dict[int, Union['Treepatch', 'Landpatch']],
			probabilities: Dict[str, float], cmap: Dict[int, int]) -> None:
		'''
		Swap a Rockpatch with a Treepatch without loosing connection to
		neighbors and associations with firefighters.
		'''
		if random.uniform(0.0, 1.0) < probabilities['respawn']:
			#Create Treepatch with same id in landpatches
			land_patches[self.id] = Treepatch(id = self.id, treestats=random.randint(0, 256),
									  neighbors = self.neighbors, fire = False)
			
			#Add to cmap
			cmap[self.id] = land_patches[self.id].treestats
		
	def __repr__(self):
		return f"Rockpatch{self.id}"
	
class Treepatch(Landpatch):
	'''
	Subclass of Landpatch representing a rock patch in a graph.

	Attributes:
	id (int): Unique identifier for the rock patch. 
	treestats (int): Tree health and color
	fire (bool): Boolean indicating whether treepatch is on fire
	'''

	def __init__(self, id, neighbors, fire = False, treestats = None) -> None:
		
		super().__init__(id, neighbors, fire)
		if treestats is None:
			self.treestats = 256 #Each tree starts with 256 health
		else: 
			self.treestats = treestats

	def mutate(self, land_patches: Dict[int, Union['Treepatch', Landpatch]], cmap: Dict[int, int]):
		'''
		Swap a Treepatch with a Rockpatch without loosing connection to
		neighbors and associations with firefighters
		'''
		#Create Rockpatch with same id in landpatches
		land_patches[self.id] = Rockpatch(id = self.id, fire = False, neighbors = self.neighbors)
		
		#Remove from cmap
		del cmap[self.id]
	
	def updateland(self, firefighters: Dict[int, 'Firefighter'], land_patches: Dict[int, Union['Treepatch', 'Landpatch']], cmap: Dict[int, int]) -> None:
		'''
		Update value of treestats due to fire or firefighter action
		for each step of iteration
		'''
		#If on fire and no firefighter, damage by 20 units
		if self.fire is True and self.id not in firefighters.values():
			self.treestats -= 20
			if self.treestats <= -256:
				self.fire = False
				self.mutate(land_patches, cmap)

		#If on fire and firefighter present, heal according to skill and put out fire
		elif self.fire is True and self.id in firefighters.values():
			firefighter = [firefighter for firefighter in firefighters if firefighter.position == self.id][0]
			self.treestats += 25 + int(firefighter.skill)
			if self.treestats >= 0:
				self.fire = False
				self.treestats = 256

		#If no fire and no firefighter, heal by 10 units
		elif self.fire is False and self.id not in firefighters.values():
			self.treestats += 10			

	def __repr__(self):
		return f"Treepatch{self.id}"
	
	def combustion(self, probabilities: Dict[str, float]) -> None:
		if random.uniform(0.0, 1.0) < probabilities['combustion']:
			self.fire = True
			self.treestats = 0

	def transmission(self,
				probabilities: Dict[str, float]
				) -> None:
		if self.fire is True:
			for neighbor in self.neighbors:
				if isinstance(neighbor, Treepatch) and random.uniform(0, 1) < probabilities['transmission']:
					neighbor.fire = True
					neighbor.treestats = 0
			
		
class Firefighter:
	'''
	Represents a firefighter in the graph.

	Attributes:
	skill (int): Skill level of the firefighter.
	position: Current position of the firefighter in graph (patch id)

	'''

	instance_count = 0

	def __init__(self,
			  	 skill,
				 position) -> None:
		
		self.skill = skill
		self.position = position
		Firefighter.instance_count += 1
		self.id = Firefighter.instance_count
		
	def __repr__(self):
		return f"Firefighter{self.id}"

	def movement(self, land_patches: Dict[int, Union[Treepatch, Landpatch]]) -> None:
		'''
		Initiate firefighter movement toward fire. 
		'''
		#Retrieve list of neighbors from current patch
		neighbors = land_patches[self.position].neighbors

		#Create list of current neighbors on fire
		neighbors_on_fire = [neighbor for neighbor in neighbors if land_patches[neighbor].fire is True]

		#If current position is on fire, stay
		if land_patches[self.position].fire is True:
			self.position = self.position
			return
		
		#If one or more neighbor treepatch on fire, move randomly there. 
		if neighbors_on_fire:
			self.position = random.choice(neighbors_on_fire)
		#If no neighbors on fire, move to random neighbor
		else:
			self.position = random.choice(neighbors)


