import random

from discord import ApplicationContext, Bot, Cog, Color, Option, \
	SlashCommandGroup

from burger_joint.bot import player_check
from burger_joint.cogs.mini_games.blackjack import BlackJack
from burger_joint.model.player import Player
from burger_joint.utils import embeds
from burger_joint.utils.decorators import cost_check


class MiniGames(Cog):
	_casino = SlashCommandGroup('casino', 'Ruin Your Savings')
	
	@_casino.command(description='')
	@player_check
	@cost_check(extra=True)
	async def blackjack(self, ctx: ApplicationContext, bet: int) -> None:
		player: Player = ctx.player  # type: ignore
		player.balance -= bet
		game: BlackJack = BlackJack(player)
		
		response = await ctx.respond(
			embed=embeds.simple_embed('Starting blackjack...')
		)
		game.message = await response.original_response()
		streak = 0
		
		while True:
			result: int = await game.play_round(bet)
			player.balance += result
			if result:
				streak += result
			else:
				streak -= bet
			
			await game.buttons.wait()
			
			if game.buttons.value == 'replay':
				if bet > player.balance:
					await ctx.edit(
						embed=embeds.simple_embed(
							description_text=f'💰 You cannot spend more than you have',
							embed_color=Color.red()
						)
					)
					return
				
				game.__init__(player)
				game.message = await response.original_response()
				continue
			break
		
		await ctx.respond(
			embed=embeds.simple_embed(
				title_text=f'You made ${streak - bet}!',
				description_text=f'New balance: ${player.balance}'
			)
		)
	
	@_casino.command(description='')
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
					embed_color=Color.red()
				)
			)


def setup(bot: Bot):
	bot.add_cog(MiniGames())
