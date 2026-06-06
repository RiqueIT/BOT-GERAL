import discord
from discord.ext import commands
import json
from datetime import datetime

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

class Member(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ✅ MEMBRO ENTROU
    @commands.Cog.listener()
    async def on_member_join(self, member):

        cargo = member.guild.get_role(
            int(config["cargo_auto"])
        )

        if cargo:

            try:
                await member.add_roles(cargo)
            except:
                pass

        canal = member.guild.get_channel(
            int(config["canal_logs"])
        )

        if not canal:
            return

        embed = discord.Embed(
            title="✅ Membro entrou",
            description=f"Bem-vindo(a) {member.mention}",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )

        embed.set_thumbnail(
            url=member.display_avatar.url
        )

        embed.add_field(
            name="👤 Usuário",
            value=f"{member} ({member.id})",
            inline=False
        )

        embed.add_field(
            name="📅 Conta criada",
            value=f"<t:{int(member.created_at.timestamp())}:R>",
            inline=False
        )

        embed.set_footer(
            text=f"Total de membros: {member.guild.member_count}"
        )

        await canal.send(embed=embed)

    # ❌ MEMBRO SAIU
    @commands.Cog.listener()
    async def on_member_remove(self, member):

        canal = member.guild.get_channel(
            int(config["canal_logs"])
        )

        if not canal:
            return

        embed = discord.Embed(
            title="❌ Membro saiu",
            description=f"{member.name} saiu do servidor.",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )

        embed.set_thumbnail(
            url=member.display_avatar.url
        )

        embed.add_field(
            name="👤 Usuário",
            value=f"{member} ({member.id})",
            inline=False
        )

        embed.set_footer(
            text=f"Total de membros: {member.guild.member_count}"
        )

        await canal.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Member(bot))