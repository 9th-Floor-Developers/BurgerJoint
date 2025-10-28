import random
from typing import override

from discord import ButtonStyle, Color, Embed, Message

from burger_joint.model.player import Player
from burger_joint.utils.inputs import ChoiceButtons


class Card:
	def __init__(self, rank: str, suit: str) -> None:
		self.rank = rank
		self.suit = suit
	
	@override
	def __str__(self) -> str:
		return f'{self.rank}{self.suit}'
	
	def value(self) -> int:
		return 11 if self.rank == 'A' \
			else 10 if self.rank in 'JQK' \
			else int(self.rank)


class Deck:
	def __init__(self) -> None:
		self.cards: list[Card] = [
			Card(v, s)
			for s in '♠♡♢♣'
			for v in [
				'A', '2', '3', '4', '5', '6', '7',
				'8', '9', '10', 'J', 'Q', 'K'
			]
		]
		random.shuffle(self.cards)
	
	def draw(self) -> Card:
		if not self.cards:
			self.__init__()
		return self.cards.pop()


class BlackJack:
	def __init__(self, player) -> None:
		self.deck: Deck = Deck()
		self.player_cards: list[Card] = [self.deck.draw(), self.deck.draw()]
		self.dealer_cards: list[Card] = [self.deck.draw()]
		self.secret_card: Card = self.deck.draw()
		self.player: Player = player
		self.message: Message | None = None
		self.buttons: ChoiceButtons | None = None
	
	@staticmethod
	def hand_value(cards: list[Card]) -> int:
		total = sum(c.value() for c in cards)
		for _ in range(sum(c.rank == 'A' for c in cards)):
			if total > 21:
				total -= 10
		return total
	
	async def update_embed(
		self,
		title: str,
		msg: str,
		extra: bool = True
	) -> None:
		embed = blackjack_embed(
			self.player_cards, self.dealer_cards, self.hand_value
		).add_field(name=title, value=msg, inline=False)
		
		if extra:
			embed.add_field(name='> 📈 Keep Playing? 📉', value='', inline=False)
		
		await self.message.edit(embed=embed, view=self.buttons)
	
	async def play_round(self, bet: int) -> int:
		p_val, d_val = self.hand_value(self.player_cards), self.hand_value(
			self.dealer_cards
		)
		self.buttons = ChoiceButtons(
			{
				'🔄️ Replay': ButtonStyle.green
			},
			player=self.player,
			timeout=10
		)
		
		if p_val == 21 and d_val != 21:
			await self.update_embed('🎉 You Win!', 'You have blackjack!')
			return int(1.5 * bet + .5)
		elif d_val == 21:
			await self.update_embed('❌ You Lose...', 'Dealer has blackjack!')
			return 0
		
		while p_val < 21:
			buttons = ChoiceButtons(
				{
					'➕ Hit': ButtonStyle.green,
					'🛑 Stand': ButtonStyle.red
				},
				player=self.player,
				timeout=20
			)
			await self.message.edit(
				embed=blackjack_embed(
					self.player_cards,
					self.dealer_cards,
					self.hand_value
				),
				view=buttons
			)
			await buttons.wait()
			
			if buttons.value == 'hit':
				self.player_cards.append(self.deck.draw())
				p_val = self.hand_value(self.player_cards)
				continue
			break
		
		if p_val > 21:
			await self.update_embed('❌ You Lose...', 'Your hand is over 21!')
			return 0
		
		self.dealer_cards.append(self.secret_card)
		while self.hand_value(self.dealer_cards) < 16:
			self.dealer_cards.append(self.deck.draw())
		
		d_val = self.hand_value(self.dealer_cards)
		
		if d_val > 21:
			msg, res = ('🎉 You Win!', 'Dealer has over 21!'), int(
				1.5 * bet + .5
			)
		elif d_val == 21:
			msg, res = ('❌ You Lose...', 'Dealer has blackjack!'), 0
		elif p_val == 21:
			msg, res = ('🎉 You Win!', 'You have blackjack!'), int(
				1.5 * bet + .5
			)
		elif p_val > d_val:
			msg, res = (('🎉 You Win!', 'You have higher than the dealer!'),
				int(1.5 * bet + .5)
			)
		elif p_val < d_val:
			msg, res = ('❌ You Lose...', 'Dealer has higher than you!'), 0
		else:
			msg, res = ('🤝 Tie...',
				'Both you and the dealer have equal values!'), bet
		
		await self.update_embed(*msg)
		return res


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
