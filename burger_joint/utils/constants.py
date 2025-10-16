from burger_joint.model.badge import Badge
from burger_joint.utils.enums import BadgeID

ALL_BADGES: dict[BadgeID, Badge] = {
	BadgeID.RENAME_SHACK: Badge(BadgeID.RENAME_SHACK.value, None, 1_000),
	BadgeID.ADD_MENU_ITEM: Badge(BadgeID.ADD_MENU_ITEM.value, None, 500),
	BadgeID.REACH_5K_INCOME: Badge(BadgeID.REACH_5K_INCOME.value, None, 5_000),
	BadgeID.SELL_1_BURGER: Badge(BadgeID.SELL_1_BURGER.value, None, 250),
	BadgeID.SELL_100_BURGERS: Badge(BadgeID.SELL_100_BURGERS.value, None, 1_000),
	BadgeID.SELL_1000_BURGERS: Badge(BadgeID.SELL_1000_BURGERS.value, None, 10_000),
	BadgeID.SELL_10000_BURGERS: Badge(BadgeID.SELL_10000_BURGERS.value, None, 100_000)
}