from dataclasses import dataclass


@dataclass
class Upgrade:
	name: str
	description: str
	cost: int
	mult: float = 1.0
	level: int = 0
	
	def upgrade(self):
		self.cost *= self.mult
		round(self.cost, 2)
		self.mult = self.mult + (.1 * self.level)
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
