from dataclasses import dataclass

from discord import ApplicationContext

from burger_joint.model.food_item import MenuItem
from burger_joint.model.upgrades import Employee, Upgrade
from burger_joint.utils import ALL_BADGES, BadgeID


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
	badges: set[BadgeID]
	menu_items: list[MenuItem]
	prestige: int
	
	def __post_init__(self):
		pass  # any calculations after init if necessary
	
	async def unlock_badge(
		self,
		badge_id: BadgeID,
		ctx: ApplicationContext
	) -> None:
		from burger_joint.utils import embeds
		
		if not self.has_badge(badge_id):
			self.badges.add(badge_id)
			self.balance += ALL_BADGES[badge_id].reward
			await ctx.send(
				embed=embeds.simple_embed(
					f'🎉 {ctx.author.name} has earned the {badge_id.value} badge!',
					f'{self.shop_name} received ${ALL_BADGES[badge_id].reward}!'
				)
			)
	
	def has_badge(self, badge_id: BadgeID) -> bool:
		return badge_id in self.badges
