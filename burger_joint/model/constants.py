from burger_joint.model.badge import Badge
from burger_joint.model.enums import BadgeID, FoodCategoryID, FoodItemID, \
	UpgradeID
from burger_joint.model.food_item import FoodItem, MenuItem
from burger_joint.model.spawnable import Spawnable
from burger_joint.model.upgrades import Employee, Upgrade


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
		'Advertisements', UpgradeID.ADVERTISEMENTS.value, 10_000,
		UpgradeID.ADVERTISEMENTS, 'advertisement.png'
	),
	UpgradeID.GRILL: Upgrade(
		'Grill', UpgradeID.GRILL.value, 1_000,
		UpgradeID.GRILL, 'grill.png'
	),
	UpgradeID.FRYER: Upgrade(
		'Fryer', UpgradeID.FRYER.value, 1_000,
		UpgradeID.FRYER, 'fryer.png'
	),
	UpgradeID.FOUNTAIN: Upgrade(
		'Fountain', UpgradeID.FOUNTAIN.value, 1_000,
		UpgradeID.FOUNTAIN, 'fountain.png'
	),
	UpgradeID.COOK: Employee(
		'Cook', UpgradeID.COOK.value, 1_000,
		UpgradeID.COOK, 'cook.png', level=1
	)
}

ALL_FOOD_ITEMS: dict[FoodItemID, FoodItem] = {
	FoodItemID.CHEESE_BURGER: FoodItem(
		FoodItemID.CHEESE_BURGER.value, 10, 1, 18, FoodCategoryID.BURGERS
	),
	FoodItemID.DOUBLE_CHEESE_BURGER: FoodItem(
		FoodItemID.DOUBLE_CHEESE_BURGER.value, 14, 2, 25,
		FoodCategoryID.BURGERS
	),
	FoodItemID.CLASSIC_BURGER: FoodItem(
		FoodItemID.CLASSIC_BURGER.value, 12, 1, 20, FoodCategoryID.BURGERS
	),
	FoodItemID.VEGGIE_BURGER: FoodItem(
		FoodItemID.VEGGIE_BURGER.value, 13, 2, 15, FoodCategoryID.BURGERS
	),
	FoodItemID.CHICKEN_SANDWICH: FoodItem(
		FoodItemID.CHICKEN_SANDWICH.value, 11, 2, 17, FoodCategoryID.BURGERS
	),
	FoodItemID.SPICY_CHICKEN_SANDWICH: FoodItem(
		FoodItemID.SPICY_CHICKEN_SANDWICH.value, 12, 3, 18,
		FoodCategoryID.BURGERS
	),
	FoodItemID.BACON_BURGER: FoodItem(
		FoodItemID.BACON_BURGER.value, 13, 3, 23, FoodCategoryID.BURGERS
	),
	
	FoodItemID.FRIES: FoodItem(
		FoodItemID.FRIES.value, 4, 1, 10, FoodCategoryID.SNACKS
	),
	FoodItemID.CURLY_FRIES: FoodItem(
		FoodItemID.CURLY_FRIES.value, 5, 2, 12, FoodCategoryID.SNACKS
	),
	FoodItemID.ONION_RINGS: FoodItem(
		FoodItemID.ONION_RINGS.value, 6, 2, 11, FoodCategoryID.SNACKS
	),
	FoodItemID.MOZZARELLA_STICKS: FoodItem(
		FoodItemID.MOZZARELLA_STICKS.value, 7, 3, 13, FoodCategoryID.SNACKS
	),
	FoodItemID.CHICKEN_NUGGETS: FoodItem(
		FoodItemID.CHICKEN_NUGGETS.value, 6, 1, 12, FoodCategoryID.SNACKS
	),
	FoodItemID.SIDE_SALAD: FoodItem(
		FoodItemID.SIDE_SALAD.value, 5, 1, 8, FoodCategoryID.SNACKS
	),
	FoodItemID.APPLE_PIE: FoodItem(
		FoodItemID.APPLE_PIE.value, 4, 2, 9, FoodCategoryID.SNACKS
	),
	
	FoodItemID.SODA: FoodItem(
		FoodItemID.SODA.value, 2, 1, 6, FoodCategoryID.DRINKS
	),
	FoodItemID.ICED_TEA: FoodItem(
		FoodItemID.ICED_TEA.value, 3, 1, 5, FoodCategoryID.DRINKS
	),
	FoodItemID.LEMONADE: FoodItem(
		FoodItemID.LEMONADE.value, 3, 2, 7, FoodCategoryID.DRINKS
	),
	FoodItemID.MILKSHAKE: FoodItem(
		FoodItemID.MILKSHAKE.value, 5, 2, 12, FoodCategoryID.DRINKS
	),
	FoodItemID.COFFEE: FoodItem(
		FoodItemID.COFFEE.value, 3, 1, 4, FoodCategoryID.DRINKS
	),
	FoodItemID.WATER: FoodItem(
		FoodItemID.WATER.value, 1, 1, 0, FoodCategoryID.DRINKS
	)
}

STARTING_MENU: list[MenuItem] = [
	get_default_menu_item(FoodItemID.CLASSIC_BURGER),
	get_default_menu_item(FoodItemID.FRIES),
	get_default_menu_item(FoodItemID.SODA)
]

ALL_SPAWNS: list[Spawnable] = [
	Spawnable(upgrade.image, False, upgrade_reward=upgrade.upgrade_id)
	for upgrade in ALL_UPGRADES.values()
]

ALL_SPAWNS += [
	Spawnable('money.png', True, cash_reward=1000)
]
