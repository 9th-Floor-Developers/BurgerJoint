import os

from discord import Bot, Intents
from dotenv import load_dotenv

bot: Bot = Bot(intents=Intents.all())


@bot.event
async def on_ready():
	print('Burger Joint Bot Online')
	
	for guild in bot.guilds:
		channel = guild.system_channel
		await channel.send('Burger Joint Bot Online')


if __name__ == '__main__':
	load_dotenv()
	bot.run(os.getenv('DISCORD_TOKEN'))
