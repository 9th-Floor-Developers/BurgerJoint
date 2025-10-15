"""Entry point for discord bot"""

import os
from bot import setup

from discord import Bot, Intents
from dotenv import load_dotenv


def main():
	bot: Bot = Bot(intents=Intents.all())
	setup(bot)
	load_dotenv()
	bot.run(os.getenv('DISCORD_TOKEN'))


if __name__ == '__main__':
	main()
