from dataclasses import dataclass
from burger_joint.utils.enums import FoodCategoryID

@dataclass
class FoodItem:
	name: str
	price: int
	difficulty: int 
	category: FoodCategoryID


    