
from discord import ApplicationContext, Bot, Cog, slash_command
from discord.ext import tasks
from burger_joint.bot import player_check


        
class WorkSytem(Cog):
    @slash_command(description="Work to earn money and XP")
    @player_check
    async def work(self, ctx: ApplicationContext):
        await ctx.respond("work in progress")
        WorkSession(ctx.author.id)

class WorkSession:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.printer.start()
        
    @tasks.loop(seconds=2, count=5)
    async def printer(self):
        print("working...")

    def update(self):
        pass

		
def setup(bot: Bot):
	bot.add_cog(WorkSytem(bot))
