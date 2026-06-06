from discord.ext import commands
import discord

class Comandos(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="comandos")
    async def comandos(self, ctx):

        embed = discord.Embed(
            title="📖 COMANDOS DO BOT Divina",
            color=0x2b0d0d
        )

        embed.add_field(
            name="🛡️ Moderação",
            value="""
`!clear 10`
Apaga mensagens.

`!addcargo @cargo @membro`
Adiciona cargo.

`!remcargo @cargo @membro`
Remove cargo.
            """,
            inline=False
        )

        embed.add_field(
            name="📊 Informações",
            value="""
`!infoid ID`
Ver perfil da conta.

`!infocaccount ID`
Ver conta HWID.

`!infodiscord ID`
Ver contas vinculadas.

`!infoplayer ID`
Ver informações completas.

`!motivoban ID`
Ver motivo banimento.

`!motivoig ID`
Ver motivo ban IG.
            """,
            inline=False
        )

        embed.set_footer(
            text="Divina RP ©"
        )

        await ctx.send(embed=embed)

async def setup(bot):

    await bot.add_cog(
        Comandos(bot)
    )