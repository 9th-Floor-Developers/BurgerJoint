from discord import ApplicationContext, Interaction, Message
from discord.ui import Button, View
from typing import override

class ChoiceButtons(View):
	def __init__(self, buttons: dict[str, int], user_id: int | None = None) -> None:
		super().__init__()
		self.user_id = user_id
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
		if (self.user_id is not None and interaction.user.id != self.user_id):
			await interaction.response.send_message(
				'This is not your button!', ephemeral=True
			)
			return True
		await interaction.response.defer()
		self.value = interaction.data["custom_id"].lower().split()[1]
		self.stop()
		return True
