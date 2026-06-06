from discord.ext import commands
import discord

spam = {}

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if "http://" in message.content or "https://discord.gg/2Wz6g6W3Dc" in message.content:
            await message.delete()

            await message.channel.send(
                f"{message.author.mention} link bloqueado.",
                delete_after=5
            )

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(AntiSpam(bot))