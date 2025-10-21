from typing import override

from discord import Interaction
from discord.ui import Button, View
from burger_joint.model import Player


class PerPersonView(View):
	def __init__(
		self,
		player: Player | None = None,
		timeout: int = 2100
	) -> None:
		super().__init__(timeout=timeout)
		self.player = player
	
	@override
	async def interaction_check(self, interaction: Interaction) -> bool:
		if self.player and interaction.user.id != self.player.user_id:
			await interaction.respond(
				'This is not your button!', ephemeral=True
			)
			return False
		return True


class ChoiceButtons(PerPersonView):
	def __init__(
		self,
		buttons: dict[str, int],
		player: int | None = None,
		timeout: int = 30
	) -> None:
		super().__init__(player=player, timeout=timeout)
		self.value = None
		for label, style in buttons.items():
			self.add_item(
				Button(
					label=label,
					style=style,  # type: ignore
					custom_id=label
				)
			)
	
	@override
	async def interaction_check(self, interaction: Interaction) -> bool:
		if not await super().interaction_check(interaction):
			return True
		
		await interaction.response.defer()
		self.value = interaction.data["custom_id"].lower().split()[1]
		await self.message.edit(embed=self.message.embeds[0], view=None)
		self.stop()
		return True
	
	@override
	async def on_timeout(self) -> None:
		await self.message.edit(embed=self.message.embeds[0], view=None)
