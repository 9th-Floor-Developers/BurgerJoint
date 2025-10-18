"""Display various information as embeds."""

from discord import Color, Embed

from burger_joint.cogs.mini_games.blackjack import Card
from burger_joint.model import Player
from burger_joint.utils.constants import ALL_BADGES, ALL_FOOD_ITEMS
from burger_joint.utils.enums import FoodCategoryID, LeaderboardID


def simple_embed(
	title_text: str = None,
	description_text: str = None,
	embed_color: Color = Color.green()
) -> Embed:
	return Embed(
		title=title_text,
		description=description_text,
		color=embed_color
	)


def status_embed(player: Player) -> Embed:
	"""Returns an embed displaying the player's stats with emojis."""
	
	embed = Embed(
		title=f'🍔 {player.shop_name} Status:',
		description=f'🏆 Level: {player.level} | ✨ XP: {player.xp} | '
		            f'💰 Balance: ${player.balance}',
		color=Color.green()
	)
	
	embed.add_field(
		name='💵 Burgers Sold',
		value=str(player.burgers_sold)
	).add_field(
		name='🛠️ Upgrades',
		value=str(len(player.upgrades))
	).add_field(
		name='👨‍🍳 Employees',
		value=str(len(player.employees))
	).set_footer(
		text=f'⭐ Prestige Level: {player.prestige}'
	)
	
	return embed


def badges_embed(player: Player) -> Embed:
	embed: Embed = simple_embed(f'{player.shop_name}\'s Badges:')
	
	for badge_id in ALL_BADGES:
		badge_obj = ALL_BADGES[badge_id]
		
		if player.has_badge(badge_id):
			embed.add_field(
				name=f'✅ {badge_obj.name}',
				value=f'~~Reward: {badge_obj.reward}~~',
				inline=False
			)
		else:
			embed.add_field(
				name=f'🔒 {badge_obj.name}',
				value=f'Reward: ${badge_obj.reward}',
				inline=False
			)
	
	embed.set_footer(
		text=f'Total Progress: {len(player.badges) // len(ALL_BADGES)}%'
	)
	
	return embed


def leaderboard_embed(
	players: list[Player],
	leaderboard_type: LeaderboardID
) -> Embed:
	embed = Embed(
		title=f'🍔 {leaderboard_type.value[0]} Leaderboard 🍔',
		color=Color.purple()
	)
	
	for i, player in enumerate(players):
		embed.add_field(
			name=f'{i + 1}. {player.shop_name} - '
			     f'{getattr(player, leaderboard_type.value[1])} '
			     f'{leaderboard_type.value[0]}',
			value='',
			inline=False
		)
	
	return embed


def menu_embed(player: Player) -> Embed:
	embed = Embed(
		title=f'🍔 {player.shop_name}'
	s
	Menu: ',
		color=Color.lighter_grey()
	)
	
	menu_item_categories: set[FoodCategoryID] = {
		ALL_FOOD_ITEMS[item.item_id].category
		for item in player.menu_items
	}
	
	for category in menu_item_categories:
		items_text = '\n'.join(
			f'{item.name} — ${item.price}'
				for item in player.menu_items
				if ALL_FOOD_ITEMS[item.item_id].category == category
		)
		
		embed.add_field(name=category.value, value=items_text, inline=False)
	
	return embed


def blackjack_embed(
	player_cards: list[Card],
	dealer_cards: list[Card],
	value_func
) -> Embed:
	embed = Embed(
		title=f'♣️ Blackjack ♦️',
		color=Color.red()
	)
	
	embed.add_field(
		name='Your Cards:',
		value=' '.join(str(c) for c in player_cards)
	).add_field(
		name='Dealer Cards:',
		value=' '.join(str(c) for c in dealer_cards)
	)
	
	embed.add_field(name='-------------------------', value='', inline=False)
	
	embed.add_field(
		name=f'Total: {value_func(player_cards)}',
		value=''
	).add_field(
		name=f'Total: {value_func(dealer_cards)}',
		value=''
	)
	
	return embed
