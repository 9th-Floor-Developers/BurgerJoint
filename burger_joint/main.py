"""Entry point for discord bot"""

import os

from discord import Bot
from dotenv import load_dotenv

from burger_joint.bot import setup


def main():
	bot: Bot = setup()
	load_dotenv()
	bot.run(os.getenv('DISCORD_TOKEN'))


if __name__ == '__main__':
	main()
