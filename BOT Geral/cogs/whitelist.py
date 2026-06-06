import discord
from discord.ext import commands

class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whitelist(self, ctx, user: discord.Member):
        cargo = discord.utils.get(ctx.guild.roles, name='Whitelist')

        if cargo:
            await user.add_roles(cargo)
            await ctx.send(f'{user.mention} aprovado na whitelist.')

async def setup(bot):
    await bot.add_cog(Whitelist(bot))