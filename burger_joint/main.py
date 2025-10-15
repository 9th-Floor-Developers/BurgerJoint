"""Entry point for discord bot"""

import os

from discord import Bot, Intents
from dotenv import load_dotenv


def main():
	bot: Bot = Bot(intents=Intents.all())
	load_dotenv()
	bot.run(os.getenv('DISCORD_TOKEN'))


if __name__ == '__main__':
	main()
