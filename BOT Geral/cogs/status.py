import discord
from discord.ext import commands, tasks

class Status(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        if not self.status.is_running():
            self.status.start()

    @tasks.loop(minutes=1)
    async def status(self):

        await self.bot.change_presence(
            activity=discord.Game(
                name="Divina City Online"
            )
        )

    @status.before_loop
    async def before_status(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Status(bot))