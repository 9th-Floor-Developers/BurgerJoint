from burger_joint.model.badge import Badge
from burger_joint.model.food_item import FoodItem, MenuItem
from burger_joint.utils.enums import BadgeID, FoodCategoryID, FoodItemID


def get_default_menu_item(food_item_ID: FoodItemID) -> MenuItem:
	food_item: FoodItem = ALL_FOOD_ITEMS[food_item_ID]
	return MenuItem(
		food_item_ID=food_item_ID,
		name=food_item.name,
		price=food_item.price,
		prestige=0
	)


ALL_BADGES: dict[BadgeID, Badge] = {
	BadgeID.RENAME_JOINT: Badge(BadgeID.RENAME_JOINT.value, None, 1_000),
	BadgeID.ADD_MENU_ITEM: Badge(BadgeID.ADD_MENU_ITEM.value, None, 500),
	BadgeID.REACH_5K_INCOME: Badge(BadgeID.REACH_5K_INCOME.value, None, 5_000),
	BadgeID.SELL_1_BURGER: Badge(BadgeID.SELL_1_BURGER.value, None, 250),
	BadgeID.SELL_100_BURGERS: Badge(
		BadgeID.SELL_100_BURGERS.value, None, 1_000
	),
	BadgeID.SELL_1000_BURGERS: Badge(
		BadgeID.SELL_1000_BURGERS.value, None, 10_000
	),
	BadgeID.SELL_10000_BURGERS: Badge(
		BadgeID.SELL_10000_BURGERS.value, None, 100_000
	)
}

ALL_FOOD_ITEMS: dict[FoodItemID, FoodItem] = {
	FoodItemID.CLASSIC_BURGER: FoodItem(
		FoodItemID.CLASSIC_BURGER.value, 12, 1, FoodCategoryID.BURGERS
	),
	FoodItemID.FRIES: FoodItem(
		FoodItemID.FRIES.value, 4, 1, FoodCategoryID.SNACKS
	),
	FoodItemID.SODA: FoodItem(
		FoodItemID.SODA.value, 2, 1, FoodCategoryID.DRINKS
	),
	FoodItemID.VEGGIE_BURGER: FoodItem(
		FoodItemID.VEGGIE_BURGER.value, 14, 2, FoodCategoryID.BURGERS
	),
	FoodItemID.CHICKEN_SANDWICH: FoodItem(
		FoodItemID.CHICKEN_SANDWICH.value, 11, 2, FoodCategoryID.BURGERS
	)
}

STARTING_MENU: list[FoodItemID] = [
	get_default_menu_item(FoodItemID.CLASSIC_BURGER),
	get_default_menu_item(FoodItemID.FRIES),
	get_default_menu_item(FoodItemID.SODA)
]
