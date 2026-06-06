from discord.ext import commands
import discord
import json
import asyncio

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

PERGUNTAS = [

    "Nome RL:",
    "Data de nascimento:",
    "Já foi STAFF? Se sim, quanto tempo?",
    "Há quanto tempo joga FiveM?",
    "O que é ser STAFF para você?",
    "Qual postura um STAFF deve ter?",
    "Por que deveríamos te aprovar?",
    "Disponibilidade para STAFF?",
    "Qual seu objetivo na STAFF?",
    "Você é responsável? se sim, Por quê?",
    "O que é Dark RP?",
    "O que é abuso de poder?",
    "O que é RDM e VDM?",
    "Drop no asfalto infringe qual regra?"

]

class ResultadoView(discord.ui.View):

    def __init__(self, usuario):
        super().__init__(timeout=None)
        self.usuario = usuario

    @discord.ui.button(
        label="Aprovar",
        style=discord.ButtonStyle.green
    )
    async def aprovar(self, interaction: discord.Interaction, button: discord.ui.Button):

        try:

            guild = interaction.guild

            membro = guild.get_member(self.usuario.id)

            if membro is None:
                membro = await guild.fetch_member(
                    self.usuario.id
                )

            cargo = guild.get_role(
                int(config["cargo_aprovado"])
            )

            if cargo is not None:
                await membro.add_roles(cargo)

            canal = guild.get_channel(
                int(config["canal_aprovados"])
            )

            canal_resultados = guild.get_channel(
                int(config["canal_resultados"])
            )

            embed = discord.Embed(
                title="✅ Formulário Aprovado",
                description=f"{membro.mention} foi aprovado no formulário.",
                color=0x00ff00
            )

            await canal.send(embed=embed)

            await canal_resultados.send(embed=embed)

            try:
                await membro.send(
                    "✅ Você foi aprovado no formulário da Divina RP!"
                )
            except:
                pass

            await interaction.response.send_message(
                "✅ Usuário aprovado com sucesso.",
                ephemeral=True
            )

        except Exception as e:

            print("ERRO APROVAR:", e)

            await interaction.response.send_message(
                f"❌ Erro ao aprovar: {e}",
                ephemeral=True
            )

    @discord.ui.button(
        label="Reprovar",
        style=discord.ButtonStyle.red
    )
    async def reprovar(self, interaction: discord.Interaction, button: discord.ui.Button):

        try:

            guild = interaction.guild

            membro = guild.get_member(self.usuario.id)

            if membro is None:
                membro = await guild.fetch_member(
                    self.usuario.id
                )

            cargo = guild.get_role(
                int(config["cargo_reprovado"])
            )

            if cargo is not None:
                await membro.add_roles(cargo)

            canal = guild.get_channel(
                int(config["canal_reprovados"])
            )

            canal_resultados = guild.get_channel(
                int(config["canal_resultados"])
            )

            embed = discord.Embed(
                title="❌ Formulário Reprovado",
                description=f"{membro.mention} foi reprovado.",
                color=0xff0000
            )

            await canal.send(embed=embed)

            await canal_resultados.send(embed=embed)

            try:
                await membro.send(
                    "❌ Você foi reprovado no formulário da Divina RP."
                )
            except:
                pass

            await interaction.response.send_message(
                "❌ Usuário reprovado.",
                ephemeral=True
            )

        except Exception as e:

            print("ERRO REPROVAR:", e)

            await interaction.response.send_message(
                f"❌ Erro ao reprovar: {e}",
                ephemeral=True
            )

class Iniciar(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Iniciar",
        style=discord.ButtonStyle.red
    )
    async def iniciar(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message(
            "✅ Formulário iniciado.",
            ephemeral=True
        )

        categoria = interaction.guild.get_channel(
            int(config["categoria"])
        )

        canal = await interaction.guild.create_text_channel(
            name=f"formulario-{interaction.user.name}",
            category=categoria
        )

        await canal.set_permissions(
            interaction.guild.default_role,
            view_channel=False
        )

        await canal.set_permissions(
            interaction.user,
            view_channel=True,
            send_messages=True
        )

        respostas = []

        for numero, pergunta in enumerate(PERGUNTAS, start=1):

            embed = discord.Embed(
                title=f"Questão {numero}/{len(PERGUNTAS)}",
                description=f"""
{pergunta}

⏳ Você tem 120 segundos para responder.
                """,
                color=0x2b0d0d
            )

            embed.set_footer(
                text=f"Divina RP • Questão {numero}/{len(PERGUNTAS)}"
            )

            mensagem_pergunta = await canal.send(embed=embed)

            def check(m):
                return (
                    m.author == interaction.user
                    and m.channel == canal
                )

            try:

                resposta = await interaction.client.wait_for(
                    "message",
                    timeout=120,
                    check=check
                )

                respostas.append(
                    f"**{pergunta}**\n{resposta.content}"
                )

                try:

                    await resposta.delete()

                    await mensagem_pergunta.delete()

                except:
                    pass

            except asyncio.TimeoutError:

                timeout = discord.Embed(
                    description="""
❌ Você demorou mais de 120 segundos para responder.

Seu formulário foi cancelado.
                    """,
                    color=0xff0000
                )

                await canal.send(embed=timeout)

                await asyncio.sleep(5)

                return await canal.delete()

        staff = interaction.guild.get_channel(
            int(config["canal_staff"])
        )

        resultado = discord.Embed(
            title="📋 Novo Formulário",
            description="\n\n".join(respostas),
            color=0x00ff00
        )

        resultado.set_author(
            name=str(interaction.user),
            icon_url=interaction.user.display_avatar.url
        )

        resultado.set_footer(
            text=f"ID: {interaction.user.id}"
        )

        await staff.send(
            embed=resultado,
            view=ResultadoView(interaction.user)
        )

        canal_resultados = interaction.guild.get_channel(
            int(config["canal_resultados"])
        )

        embed_resultado = discord.Embed(
            title="📨 Novo Formulário",
            description=f"{interaction.user.mention} enviou um formulário.",
            color=0x2b0d0d
        )

        await canal_resultados.send(
            embed=embed_resultado
        )

        final = discord.Embed(
            description="""
✅ Seu formulário foi enviado para nossa staff.

⏳ Este canal será apagado em 1 minuto.
            """,
            color=0x00ff00
        )

        await canal.send(embed=final)

        await asyncio.sleep(60)

        await canal.delete()

class Recrutamento(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def recrutamento(self, ctx):

        embed = discord.Embed(
            title="📋 Formulário | Divina RP",
            description="""
Seja bem-vindo ao Divina RP!

Clique em `Iniciar` para começar seu formulário.
            """,
            color=0x2b0d0d
        )

        embed.add_field(
            name="📌 Informações",
            value="""
• Responda tudo corretamente.
• Você tem 120 segundos por pergunta.
• Trollagens resultam em punição.
            """,
            inline=False
        )

        await ctx.send(
            embed=embed,
            view=Iniciar()
        )

async def setup(bot):
    await bot.add_cog(Recrutamento(bot))