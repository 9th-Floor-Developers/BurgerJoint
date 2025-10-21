from typing import override

from discord import Interaction
from discord.ui import Button, View


class PerPersonView(View):
	def __init__(
		self,
		user_id: int | None = None,
		timeout: int = 2100
	) -> None:
		super().__init__(timeout=timeout)
		self.user_id = user_id
	
	@override
	async def interaction_check(self, interaction: Interaction) -> bool:
		if self.user_id and interaction.user.id != self.user_id:
			await interaction.respond(
				'This is not your button!', ephemeral=True
			)
			return False
		return True


class ChoiceButtons(PerPersonView):
	def __init__(
		self,
		buttons: dict[str, int],
		user_id: int | None = None,
		timeout: int = 30
	) -> None:
		super().__init__(user_id=user_id, timeout=timeout)
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
