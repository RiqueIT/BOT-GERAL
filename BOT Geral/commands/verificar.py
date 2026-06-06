import discord
from discord.ext import commands

# ID DOS SERVIDORES
SERVIDOR_DIVINA = 1510095462483366008
SERVIDOR_LOGS = 1510083021569523792

# CANAL DE LOGS DO VERIFICAR
CANAL_LOGS = 1511072898830434354

class VerificarView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Verificar",
        emoji="✅",
        style=discord.ButtonStyle.green
    )
    async def verificar(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        divina = interaction.client.get_guild(
            SERVIDOR_DIVINA
        )

        logs = interaction.client.get_guild(
            SERVIDOR_LOGS
        )

        if not divina:

            return await interaction.response.send_message(
                "❌ Não encontrei o servidor Divina RP.",
                ephemeral=True
            )

        membro_divina = divina.get_member(
            interaction.user.id
        )

        if not membro_divina:

            return await interaction.response.send_message(
                "❌ Você não está na Divina RP.",
                ephemeral=True
            )

        cargos_adicionados = []

        for cargo_divina in membro_divina.roles:

            if cargo_divina.name == "@everyone":
                continue

            cargo_logs = discord.utils.get(
                logs.roles,
                name=cargo_divina.name
            )

            if cargo_logs:

                try:

                    if cargo_logs not in interaction.user.roles:

                        await interaction.user.add_roles(
                            cargo_logs
                        )

                        cargos_adicionados.append(
                            cargo_logs.name
                        )

                except:
                    pass

        embed = discord.Embed(
            title="✅ Verificação concluída",
            description="""
Seus cargos foram sincronizados com sucesso.

Obrigado por verificar sua conta.
            """,
            color=0x00ff00
        )

        if cargos_adicionados:

            embed.add_field(
                name="🏷️ Cargos adicionados",
                value="\n".join(cargos_adicionados[:20]),
                inline=False
            )

        else:

            embed.add_field(
                name="📌 Resultado",
                value="Nenhum cargo novo foi encontrado para sincronizar.",
                inline=False
            )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

        # LOGS
        canal_logs = interaction.client.get_channel(
            CANAL_LOGS
        )

        if canal_logs:

            log = discord.Embed(
                title="🔗 Verificação Realizada",
                color=0x00ff00
            )

            log.add_field(
                name="👤 Usuário",
                value=f"{interaction.user.mention}\n`{interaction.user.id}`",
                inline=False
            )

            log.add_field(
                name="📌 Servidor Origem",
                value="Divina RP",
                inline=False
            )

            log.add_field(
                name="📌 Servidor Destino",
                value="Logs Divina",
                inline=False
            )

            log.add_field(
                name="🏷️ Total de Cargos",
                value=str(len(cargos_adicionados)),
                inline=False
            )

            if cargos_adicionados:

                log.add_field(
                    name="📋 Cargos Sincronizados",
                    value="\n".join(cargos_adicionados[:20]),
                    inline=False
                )

            log.set_footer(
                text=f"ID: {interaction.user.id}"
            )

            await canal_logs.send(embed=log)

class Verificar(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verificar(self, ctx):

        embed = discord.Embed(
            title="🔗 Sistema de Verificação",
            description="""
Clique abaixo para VERIFICAR seus cargos nas cidades (UTILIZE APENAS SE ESTIVER SEM CARGO NESTE SERVIDOR).

✅ Verificação automática
✅ Sincronização de cargos
✅ Sistema seguro
            """,
            color=0x2b0d0d
        )

        embed.set_footer(
            text="Divina RP • Sistema de Verificação"
        )

        await ctx.send(
            embed=embed,
            view=VerificarView()
        )

async def setup(bot):
    await bot.add_cog(
        Verificar(bot)
    )