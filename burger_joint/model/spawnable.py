from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from burger_joint.model import Player, UpgradeID


@dataclass
class Spawnable:
	image: str
	is_cash: bool
	cash_reward: int = 0
	upgrade_reward: 'UpgradeID' = None
	
	def claim(self, player: 'Player') -> None:
		from burger_joint.utils import database
		
		if self.is_cash:
			player.balance += self.cash_reward
		else:
			for upgrade in player.upgrades:
				if upgrade.upgrade_id != self.upgrade_reward:
					continue
				
				upgrade.upgrade()
				break
		
		database.save_data(player)
