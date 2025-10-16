from dataclasses import dataclass

from burger_joint.model.badge import Badge
from burger_joint.model.upgrades import Employee, Upgrade


@dataclass
class Player:
	user_id: int
	username: str
	shop_name: str
	balance: int
	level: int
	xp: int
	burgers_sold: int
	upgrades: list[Upgrade]
	employees: list[Employee]
	badges: list[Badge]
	prestige: int
	
	def __post_init__(self):
		pass  # any calculations after init if necessary

# TODO Related Commands:
#  - /rename <NAME>
