import discord
from discord.ext import commands
from datetime import datetime

LOG_CHANNEL_ID = 1511065325280432209

class CommandLogs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ✅ COMANDO EXECUTADO
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):

        canal = self.bot.get_channel(LOG_CHANNEL_ID)

        if not canal:
            return

        embed = discord.Embed(
            title="✅ Comando Executado",
            color=0x00ff00,
            timestamp=datetime.now()
        )

        embed.add_field(
            name="👤 Usuário",
            value=f"{ctx.author.mention}\n`{ctx.author.id}`",
            inline=False
        )

        embed.add_field(
            name="📌 Comando",
            value=f"`{ctx.message.content}`",
            inline=False
        )

        embed.add_field(
            name="📂 Canal",
            value=ctx.channel.mention,
            inline=False
        )

        embed.add_field(
            name="🏷️ Cargo Mais Alto",
            value=ctx.author.top_role.mention,
            inline=False
        )

        await canal.send(embed=embed)

    # ❌ COMANDO COM ERRO
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        canal = self.bot.get_channel(LOG_CHANNEL_ID)

        if not canal:
            return

        embed = discord.Embed(
            title="❌ Comando Falhou",
            color=0xff0000,
            timestamp=datetime.now()
        )

        embed.add_field(
            name="👤 Usuário",
            value=f"{ctx.author.mention}\n`{ctx.author.id}`",
            inline=False
        )

        embed.add_field(
            name="📌 Comando",
            value=f"`{ctx.message.content}`",
            inline=False
        )

        embed.add_field(
            name="📂 Canal",
            value=ctx.channel.mention,
            inline=False
        )

        embed.add_field(
            name="⚠️ Erro",
            value=f"```{str(error)[:900]}```",
            inline=False
        )

        await canal.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CommandLogs(bot))