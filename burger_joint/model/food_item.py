from dataclasses import dataclass

@dataclass
class FoodItem:
	name: str
	price: int
	difficulty: int 
	category : any

"""Represents a food item on a player's menu. may have different name, price, 
and prestige level than the base FoodItem depending on the joint"""
@dataclass
class MenuItem:
	food_item_ID : any
	name: str
	price: str
	prestige: int 