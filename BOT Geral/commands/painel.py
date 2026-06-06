from discord.ext import commands
import discord

class Painel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def painelvincular(self, ctx):

        embed = discord.Embed(
            description="""
# 🆔 VINCULE O SEU ID

• Para vincular envie seu ID do jogo.

• Aguarde a liberação automática.

• Caso não saiba seu ID, entre na cidade.
            """,
            color=0x2b0d0d
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Painel(bot))