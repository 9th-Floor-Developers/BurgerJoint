from discord import Cog, User

from burger_joint.model import Player
from burger_joint.utils import database


class PlayerCommands(Cog):
	@staticmethod
	def create_new_player(user: User):
		player = Player(
			user_id=user.id, username=user.name,
			shop_name=f"{user.name}'s Burger Joint", balance=100, level=1,
			xp=0, burgers_sold=0, upgrades=[], employees=[], badges=[],
			prestige=0
		)
		database.save_data(player)
		return player
