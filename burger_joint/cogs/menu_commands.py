from discord import ApplicationContext, Bot, ButtonStyle, Cog, slash_command
from discord.ui import button, View

from burger_joint.bot import player_check
from utils import embeds


class MenuCommands(Cog):
	@slash_command(description='View and edit you joint\'s menu')
	@player_check
	async def menu(self, ctx: ApplicationContext):
		await ctx.respond(
			embed=embeds.menu_embed(ctx.player),  # type: ignore
			view=MenuView()
		)


class MenuView(View):
	@button(
		label='Add Item', style=ButtonStyle.success  # type: ignore
	)
	async def add_item_button_callback(self, _, interaction):
		await interaction.response.send_message('You clicked the button1!')
	
	@button(label='Remove Item', style=ButtonStyle.red)  # type: ignore
	async def remove_item_button_callback(self, _, interaction):
		await interaction.response.send_message('You clicked the button2!')
	
	@button(
		label='Edit Item', style=ButtonStyle.primary  # type: ignore
	)
	async def edit_item_button_callback(self, _, interaction):
		await interaction.response.send_message('You clicked the button3!')


def setup(bot: Bot):
	bot.add_cog(MenuCommands(bot))
