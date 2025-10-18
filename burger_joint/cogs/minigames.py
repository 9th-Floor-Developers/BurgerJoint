import functools
import random

import discord
from discord import ApplicationContext, Bot, Cog, Option

from bot import player_check
from burger_joint.cogs.mini_games.blackjack import BlackJack
from burger_joint.model import Player
from burger_joint.utils import embeds


def cost_check(needed: int = 1, extra: bool = False):
	def decorator(func):
		@functools.wraps(func)
		async def wrapper(self, ctx: ApplicationContext, *args, **kwargs):
			player: Player = ctx.player  # type: ignore
			if player.balance < 1:
				await ctx.respond(
					embed=embeds.simple_embed(
						description_text='🏦 You do not have any money.',
						embed_color=discord.Color.red()
					)
				)
				return
			elif player.balance < needed:
				await ctx.respond(
					embed=embeds.simple_embed(
						description_text=f'💵 You need at least ${needed} (${needed - player.balance} more).',
						embed_color=discord.Color.red()
					)
				)
				return
			elif extra:
				bet = list(kwargs.values())[0]
				
				if bet > player.balance:
					await ctx.respond(
						embed=embeds.simple_embed(
							description_text=f'💰 You cannot spend more than you have',
							embed_color=discord.Color.red()
						)
					)
					return
				elif bet < 1:
					await ctx.respond(
						embed=embeds.simple_embed(
							description_text=f'💰 You cannot bet a negative number.',
							embed_color=discord.Color.red()
						)
					)
					return
			
			await func(self, ctx, *args, **kwargs)
		
		return wrapper
	
	return decorator


class MiniGames(Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@discord.slash_command(description='')
	@player_check
	@cost_check(extra=True)
	async def blackjack(self, ctx: ApplicationContext, bet: int) -> None:
		player: Player = ctx.player  # type: ignore
		streak = await BlackJack().play(bet, ctx)
		player.balance += streak - bet
		
		await ctx.respond(
			embed=embeds.simple_embed(
				title_text=f'You made ${streak}!',
				description_text=f'New balance: ${player.balance}'
			)
		)
	
	@discord.slash_command(description='')
	@player_check
	@cost_check(extra=True)
	async def coinflip(
		self,
		ctx: ApplicationContext,
		bet: int,
		choice: Option(str, choices=['Heads', 'Tails'])  # type: ignore
	) -> None:
		player: Player = ctx.player  # type: ignore
		streak = int(.5 * bet)
		result = random.choice(['Heads', 'Tails'])
		
		won = result == choice
		player.balance += streak \
			if won \
			else -bet
		
		if won:
			await ctx.respond(
				embed=embeds.simple_embed(
					title_text=f'🎉 {result}!!! You won ${bet + streak}',
					description_text=f'New balance: ${player.balance}'
				)
			)
		else:
			await ctx.respond(
				embed=embeds.simple_embed(
					title_text=f'📉 {result}... You lost ${bet}',
					description_text=f'New balance: ${player.balance}',
					embed_color=discord.Color.red()
				)
			)


def setup(bot: Bot):
	bot.add_cog(MiniGames(bot))
