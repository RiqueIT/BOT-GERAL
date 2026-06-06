from discord.ext import commands
import discord

class Mod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # 🧹 CLEAR
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, quantidade: int):

        await ctx.channel.purge(limit=quantidade + 1)

        msg = await ctx.send(
            f"✅ {quantidade} mensagens apagadas."
        )

        await msg.delete(delay=3)

    # ➕ ADD CARGO
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addcargo(
        self,
        ctx,
        cargo: discord.Role,
        *membros: discord.Member
    ):

        if not membros:
            return await ctx.send(
                "❌ Informe os membros."
            )

        if cargo.position >= ctx.author.top_role.position:
            return await ctx.send(
                "❌ Você não pode adicionar cargos acima do seu."
            )

        if cargo.position >= ctx.guild.me.top_role.position:
            return await ctx.send(
                "❌ Meu cargo precisa estar acima desse cargo."
            )

        for membro in membros:
            await membro.add_roles(cargo)

        embed = discord.Embed(
            title="✅ Cargo Adicionado",
            color=0x00ff00
        )

        embed.add_field(
            name="👮 Staff",
            value=ctx.author.mention,
            inline=False
        )

        embed.add_field(
            name="📌 Cargo",
            value=cargo.mention,
            inline=False
        )

        embed.add_field(
            name="👥 Membros",
            value=", ".join([m.mention for m in membros]),
            inline=False
        )

        await ctx.send(embed=embed)

    # ➖ REMOVER CARGO
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def remcargo(
        self,
        ctx,
        cargo: discord.Role,
        *membros: discord.Member
    ):

        if not membros:
            return await ctx.send(
                "❌ Informe os membros."
            )

        if cargo.position >= ctx.author.top_role.position:
            return await ctx.send(
                "❌ Você não pode remover cargos acima do seu."
            )

        if cargo.position >= ctx.guild.me.top_role.position:
            return await ctx.send(
                "❌ Meu cargo precisa estar acima desse cargo."
            )

        for membro in membros:
            await membro.remove_roles(cargo)

        embed = discord.Embed(
            title="❌ Cargo Removido",
            color=0xff0000
        )

        embed.add_field(
            name="👮 Staff",
            value=ctx.author.mention,
            inline=False
        )

        embed.add_field(
            name="📌 Cargo",
            value=cargo.mention,
            inline=False
        )

        embed.add_field(
            name="👥 Membros",
            value=", ".join([m.mention for m in membros]),
            inline=False
        )

        await ctx.send(embed=embed)

    # ➕ CARGO EM TODOS
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def cargoall(
        self,
        ctx,
        cargo: discord.Role
    ):

        mensagem = await ctx.send(
            f"⏳ Adicionando {cargo.mention} em todos os membros..."
        )

        adicionados = 0

        for membro in ctx.guild.members:

            if membro.bot:
                continue

            try:

                if cargo not in membro.roles:

                    await membro.add_roles(cargo)

                    adicionados += 1

            except:
                pass

        embed = discord.Embed(
            title="✅ Cargo Adicionado em Massa",
            color=0x00ff00
        )

        embed.add_field(
            name="📌 Cargo",
            value=cargo.mention,
            inline=False
        )

        embed.add_field(
            name="👥 Membros Afetados",
            value=str(adicionados),
            inline=False
        )

        embed.add_field(
            name="👮 Executado por",
            value=ctx.author.mention,
            inline=False
        )

        await mensagem.edit(
            content=None,
            embed=embed
        )

    # ➖ REMOVER CARGO DE TODOS
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def remcargoall(
        self,
        ctx,
        cargo: discord.Role
    ):

        mensagem = await ctx.send(
            f"⏳ Removendo {cargo.mention} de todos os membros..."
        )

        removidos = 0

        for membro in ctx.guild.members:

            if membro.bot:
                continue

            try:

                if cargo in membro.roles:

                    await membro.remove_roles(cargo)

                    removidos += 1

            except:
                pass

        embed = discord.Embed(
            title="❌ Cargo Removido em Massa",
            color=0xff0000
        )

        embed.add_field(
            name="📌 Cargo",
            value=cargo.mention,
            inline=False
        )

        embed.add_field(
            name="👥 Membros Afetados",
            value=str(removidos),
            inline=False
        )

        embed.add_field(
            name="👮 Executado por",
            value=ctx.author.mention,
            inline=False
        )

        await mensagem.edit(
            content=None,
            embed=embed
        )

async def setup(bot):
    await bot.add_cog(Mod(bot))