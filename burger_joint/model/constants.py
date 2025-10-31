from burger_joint.model.badge import Badge
from burger_joint.model.enums import BadgeID, FoodCategoryID, FoodItemID, \
	UpgradeID
from burger_joint.model.food_item import FoodItem, MenuItem
from burger_joint.model.upgrades import Upgrade, Employee


def get_default_menu_item(food_item_id: FoodItemID) -> MenuItem:
	food_item: FoodItem = ALL_FOOD_ITEMS[food_item_id]
	return MenuItem(
		food_item_ID=food_item_id,
		name=food_item.name,
		price=food_item.default_price,
		prestige=0
	)


ALL_BADGES: dict[BadgeID, Badge] = {
	BadgeID.RENAME_JOINT: Badge(BadgeID.RENAME_JOINT.value, 1_000),
	BadgeID.ADD_MENU_ITEM: Badge(BadgeID.ADD_MENU_ITEM.value, 500),
	BadgeID.REACH_5K_INCOME: Badge(BadgeID.REACH_5K_INCOME.value, 5_000),
	BadgeID.SELL_1_BURGER: Badge(BadgeID.SELL_1_BURGER.value, 250),
	BadgeID.SELL_100_BURGERS: Badge(
		BadgeID.SELL_100_BURGERS.value, 1_000
	),
	BadgeID.SELL_1000_BURGERS: Badge(
		BadgeID.SELL_1000_BURGERS.value, 10_000
	),
	BadgeID.SELL_10000_BURGERS: Badge(
		BadgeID.SELL_10000_BURGERS.value, 100_000
	),
	BadgeID.SECRET: Badge(BadgeID.SECRET.value, 10_000)
}

ALL_UPGRADES: dict[UpgradeID, Upgrade] = {
	UpgradeID.ADVERTISEMENTS: Upgrade(
		'Advertisements', UpgradeID.ADVERTISEMENTS.value, 10_000, UpgradeID.ADVERTISEMENTS,
	),
	UpgradeID.GRILL: Upgrade(
		'Grill', UpgradeID.GRILL.value, 1_000, UpgradeID.GRILL
	),
	UpgradeID.FRYER: Upgrade(
		'Fryer', UpgradeID.FRYER.value, 1_000, UpgradeID.FRYER
	),
	UpgradeID.FOUNTAIN: Upgrade(
		'Fountain', UpgradeID.FOUNTAIN.value, 1_000, UpgradeID.FOUNTAIN
	),
	UpgradeID.COOK: Employee(
		'Cook', UpgradeID.COOK.value, 1_000, UpgradeID.COOK, level=1
	)
}

ALL_FOOD_ITEMS: dict[FoodItemID, FoodItem] = {
	FoodItemID.CLASSIC_BURGER: FoodItem(
		FoodItemID.CLASSIC_BURGER.value, 12, 1, 20, FoodCategoryID.BURGERS
	),
	FoodItemID.FRIES: FoodItem(
		FoodItemID.FRIES.value, 4, 1, 10, FoodCategoryID.SNACKS
	),
	FoodItemID.SODA: FoodItem(
		FoodItemID.SODA.value, 2, 1, 6, FoodCategoryID.DRINKS
	),
	FoodItemID.VEGGIE_BURGER: FoodItem(
		FoodItemID.VEGGIE_BURGER.value, 14, 2, 15, FoodCategoryID.BURGERS
	),
	FoodItemID.CHICKEN_SANDWICH: FoodItem(
		FoodItemID.CHICKEN_SANDWICH.value, 11, 2, 15, FoodCategoryID.BURGERS
	)
}

STARTING_MENU: list[MenuItem] = [
	get_default_menu_item(FoodItemID.CLASSIC_BURGER),
	get_default_menu_item(FoodItemID.FRIES),
	get_default_menu_item(FoodItemID.SODA)
]
