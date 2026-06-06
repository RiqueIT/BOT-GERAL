import discord
from discord.ext import commands
import re

LINK_REGEX = r'(https?:\/\/[^\s]+)'

class Protection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if re.search(LINK_REGEX, message.content):
            await message.delete()
            await message.channel.send(f'{message.author.mention} link bloqueado.', delete_after=5)

async def setup(bot):
    await bot.add_cog(Protection(bot))