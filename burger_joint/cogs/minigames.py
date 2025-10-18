import discord
from discord import ApplicationContext, Bot, Cog

from bot import player_check
from burger_joint.cogs.mini_games.blackjack import BlackJack
from burger_joint.model import Player
from burger_joint.utils import embeds


class MiniGames(Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@discord.slash_command(description='')
	@player_check
	async def blackjack(self, ctx: ApplicationContext, bet: int):
		player: Player = ctx.player
		if player.balance < 1:
			await ctx.respond(
				embed=embeds.simple_embed(
					description_text='🏦 You do not have enough money to play blackjack',
					embed_color=discord.Color.red()
				)
			)
			return
		elif bet <= 0:
			await ctx.respond(
				embed=embeds.simple_embed(
					description_text='💵 Minimum Bet is $1',
					embed_color=discord.Color.red()
				)
			)
			return
		
		streak = await BlackJack().play(bet, ctx)
		player.balance += streak
		
		await ctx.respond(
			embed=embeds.simple_embed(
				title_text=f'You made ${streak}!',
				description_text=f'New balance: ${player.balance}'
			)
		)


def setup(bot: Bot):
	bot.add_cog(MiniGames(bot))
