from dataclasses import dataclass
from typing import override, TYPE_CHECKING

if TYPE_CHECKING:
	from burger_joint.model import UpgradeID


@dataclass
class Upgrade:
	name: str
	description: str
	cost: int
	upgrade_id: 'UpgradeID'
	mult: float = 1.0
	level: int = 0
	
	def upgrade(self):
		self.cost *= self.mult
		self.cost = round(self.cost, 2)
		self.mult += 0.1
		self.level += 1


# TODO Related Commands:
#  - /shop
#  - /buy <UPGRADE>
#  - /inventory

@dataclass
class Employee(Upgrade):
	pass  # employee functionality, i.e.: customer attraction, spawn rates, etc.

# TODO Related Commands:
#  - /hire <EMPLOYEE>
#  - /promote <EMPLOYEE>
#  - /employees
