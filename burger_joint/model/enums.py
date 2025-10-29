from enum import Enum


class BadgeID(Enum):
	RENAME_JOINT = 'Rename Your Burger Joint'
	ADD_MENU_ITEM = 'Add A Menu Item'
	REACH_5K_INCOME = 'Reach $5,000 Income'
	SELL_1_BURGER = 'Sell 1 Burger'
	SELL_100_BURGERS = 'Sell 100 Burgers'
	SELL_1000_BURGERS = 'Sell 1000 Burgers'
	SELL_10000_BURGERS = 'Sell 10000 Burgers'


class UpgradeID(Enum):
	DRIVE_THRU = 'Increase Customers Per Work Session',
	CASH_REGISTER = 'Increase Cost Of All Food Items'
	COOK = 'Increses the amount of cooking that can be done'


class LeaderboardID(Enum):
	BALANCE = ('Balance', 'balance')
	XP = ('XP', 'xp')
	BURGERS_SOLD = ('Burgers', 'burgers_sold')
	PRESTIGE = ('Prestige', 'prestige')


class FoodItemID(Enum):
	CLASSIC_BURGER = 'Classic Burger'
	FRIES = 'Fries'
	SODA = 'Soda'
	VEGGIE_BURGER = 'Veggie Burger'
	CHICKEN_SANDWICH = 'Chicken Sandwich'


class FoodCategoryID(Enum):
	BURGERS = 'Burgers'
	SNACKS = 'Snacks'
	DRINKS = 'Drinks'
