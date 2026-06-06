from discord.ext import commands
import discord
import requests

IP = "SEUIP:30120"
CODIGO = "cfx.re/join/seucodigo"

class Cidade(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cidade")
    async def cidade(self, ctx):

        try:

            req = requests.get(
                f"http://{IP}/players.json",
                timeout=5
            )

            players = len(req.json())

            status = "🟢 Online"

        except:

            players = 0
            status = "🔴 Offline"

        embed = discord.Embed(
            title="Status do Servidor -> Divina City",
            color=0x2b0d0d
        )

        embed.add_field(
            name="👥 Players",
            value=f"```{players}```",
            inline=True
        )

        embed.add_field(
            name="📡 Status",
            value=f"```{status}```",
            inline=True
        )

        embed.add_field(
            name="🎮 Connect",
            value=f"```{CODIGO}```",
            inline=False
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Cidade(bot))