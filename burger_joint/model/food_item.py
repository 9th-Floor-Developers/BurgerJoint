from dataclasses import dataclass

from burger_joint.utils.enums import FoodCategoryID, FoodItemID


@dataclass
class FoodItem:
	name: str
	price: int
	difficulty: int
	category: FoodCategoryID


"""Represents a food item on a player's menu. may have different name, price,
and prestige level than the base FoodItem depending on the joint"""


@dataclass
class MenuItem:
	food_item_ID: FoodItemID
	name: str
	price: str
	prestige: int
