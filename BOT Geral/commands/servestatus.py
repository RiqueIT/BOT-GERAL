from discord.ext import commands
import discord
import requests

IP = "SEU_IP:30120"
CODIGO = "cfx.re/join/seucodigo"

class ServerStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="status")
    async def status(self, ctx):

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
            title="Status do Servidor -> SANTA GROUP",
            color=0x2b0d0d
        )

        embed.add_field(
            name="👾 Players:",
            value=f"```{players}```",
            inline=True
        )

        embed.add_field(
            name="📡 Status:",
            value=f"```{status}```",
            inline=True
        )

        embed.add_field(
            name="🎮 CONECTE-SE PELO F8 DO FIVEM COM O CÓDIGO:",
            value=f"```{CODIGO}```",
            inline=False
        )

        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/1374170879837247590/1374170956353945610/standard.gif"
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerStatus(bot))