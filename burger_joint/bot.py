"""Bot initialization, event loop, command loader"""


@bot.event
async def on_ready():
	print('Burger Joint Bot Online')
	
	for guild in bot.guilds:
		channel = guild.system_channel
		await channel.send('Burger Joint Bot Online')
