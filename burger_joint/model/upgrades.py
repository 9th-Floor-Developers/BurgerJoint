from dataclasses import dataclass


@dataclass
class Upgrade:
	name: str
	level: int
	cost: int
	mult: float


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
