import functools

from discord import ApplicationContext, Color

from burger_joint.model.player import Player
from burger_joint.model.enums import LeaderboardID
from burger_joint.utils import database, embeds


def player_check(func):
	@functools.wraps(func)
	async def wrapper(*args, **kwargs):
		idx: int
		if isinstance(args[0], ApplicationContext):
			idx = 0
		elif len(args) > 1 and isinstance(args[1], ApplicationContext):
			idx = 1
		else:
			raise ValueError(
				'No ApplicationContext found in first two arguments '
				'of function decorated with @player_check'
			)
		
		player: Player | None = database.get_player(args[idx].author.id)
		if not player:
			await args[idx].respond(
				embed=embeds.simple_embed(
					'❌ You do not own a burger joint!',
					'Use the `/start` command to '
					'start your very own burger joint!',
					Color.red()
				)
			)
			return None
		
		args[idx].player = player
		result = await func(*args, **kwargs)
		database.save_data(player)
		return result
	
	return wrapper


def cost_check(needed: int = 1, extra: bool = False):
	def decorator(func):
		@functools.wraps(func)
		async def wrapper(self, ctx: ApplicationContext, *args, **kwargs):
			player: Player = ctx.player  # type: ignore
			if player.balance < 1:
				await ctx.respond(
					embed=embeds.simple_embed(
						description_text='🏦 You do not have any money.',
						embed_color=Color.red()
					)
				)
				return
			elif player.balance < needed:
				await ctx.respond(
					embed=embeds.simple_embed(
						description_text=f'💵 You need at least ${needed} '
						                 f'(${needed - player.balance} more).',
						embed_color=Color.red()
					)
				)
				return
			elif extra:
				bet = list(kwargs.values())[0]
				
				if bet > player.balance:
					await ctx.respond(
						embed=embeds.simple_embed(
							description_text=f'💰 You cannot spend more than you have',
							embed_color=Color.red()
						)
					)
					return
				elif bet < 1:
					await ctx.respond(
						embed=embeds.simple_embed(
							description_text=f'💰 You cannot bet a negative number.',
							embed_color=Color.red()
						)
					)
					return
			
			await func(self, ctx, *args, **kwargs)
		
		return wrapper
	
	return decorator


def leaderboard_command(attr: str, leaderboard_id: LeaderboardID):
	def decorator(func):
		@functools.wraps(func)
		async def wrapper(_, ctx: ApplicationContext):
			from burger_joint.cogs.leaderboards import leaderboard_embed
			
			players: list[Player] = database.get_all_players()
			players.sort(key=lambda p: getattr(p, attr), reverse=True)
			await ctx.respond(
				embed=leaderboard_embed(players, leaderboard_id)
			)
		
		return wrapper
	
	return decorator
