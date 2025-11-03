from dataclasses import dataclass

from discord import Color, Interaction, TextChannel

from burger_joint.model.constants import ALL_BADGES
from burger_joint.model.enums import BadgeID, UpgradeID
from burger_joint.model.food_item import MenuItem
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
	badges: set[BadgeID]
	menu_items: list[MenuItem]
	prestige: int
	
	async def unlock_badge(
		self,
		badge_id: BadgeID,
		ctx: TextChannel
	) -> None:
		from burger_joint.utils import embeds
		
		if not self.has_badge(badge_id):
			self.badges.add(badge_id)
			self.balance += ALL_BADGES[badge_id].reward
			await ctx.send(
				embed=embeds.simple_embed(
					f'🎉 {self.username} has earned the {badge_id.value} badge!',
					f'{self.shop_name} received ${ALL_BADGES[badge_id].reward}!'
				)
			)
	
	def has_badge(self, badge_id: BadgeID) -> bool:
		return badge_id in self.badges
	
	async def has_menu_item_name(
		self,
		name: str,
		interaction: Interaction | None = None
	) -> bool:
		for item in self.menu_items:
			from burger_joint.utils import embeds
			
			if item.name.strip() != name.strip() or not interaction:
				continue
			
			await interaction.respond(
				embed=embeds.simple_embed(
					description_text=f'You already have a menu item named {name}',
					embed_color=Color.red()
				),
				ephemeral=True
			)
			
			return True
		return False
	
	def get_upgrade(self, upgrade_id: UpgradeID) -> Upgrade:
		for upgrade in self.upgrades:
			if upgrade.upgrade_id.name == upgrade_id.name:
				return upgrade
		raise ValueError(
			f'Cannot Find Upgrade: {upgrade_id} In Player.upgrades'
		)
