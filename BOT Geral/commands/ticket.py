import discord
from discord.ext import commands
from discord.ui import Select, View, Button
from datetime import datetime
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# 📌 CONFIG
CATEGORIAS = {
    "Denúncia": int(config["categoria_ticket_denuncia"]),
    "Suporte": int(config["categoria_ticket_suporte"]),
    "ADV": int(config["categoria_ticket_adv"]),
    "Doação": int(config["categoria_ticket_doacao"]),
}

LOG_CHANNEL_ID = int(config["canal_logs_ticket"])

STAFF_ROLES = [

    int(config["cargo_staff_1"]),
    int(config["cargo_staff_2"]),
    int(config["cargo_staff_3"]),
    int(config["cargo_staff_4"])

]

tickets_abertos = {}

# 🔴 BOTÃO FECHAR
class FecharButton(Button):

    def __init__(self):
        super().__init__(
            label="🔒 Fechar Ticket",
            style=discord.ButtonStyle.red
        )

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=True)

        canal = interaction.channel

        log_channel = interaction.guild.get_channel(
            LOG_CHANNEL_ID
        )

        mensagens = []

        async for msg in canal.history(limit=200):

            mensagens.append(
                f"<p><b>{msg.author}</b>: {msg.content}</p>"
            )

        html = f"""
        <html>
        <body style="background:#1e1f22;color:white;font-family:Arial;">
        <h2>Transcript do Ticket</h2>
        {''.join(mensagens[::-1])}
        </body>
        </html>
        """

        with open(
            "transcript.html",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(html)

        membro = None

        for membro_ticket in canal.members:

            if not membro_ticket.bot:

                membro = membro_ticket

                break

        # 📩 DM FINAL
        embed_dm = discord.Embed(
            title="✅ Seu atendimento foi finalizado!",
            description="""
📄 Considerações finais:

Resolvido.

Obrigado por usar nosso suporte!
            """,
            color=0x00ff00
        )

        embed_dm.add_field(
            name="👮 Staff",
            value=interaction.user.mention,
            inline=False
        )

        embed_dm.add_field(
            name="🆔 ID",
            value=str(membro.id),
            inline=False
        )

        embed_dm.add_field(
            name="📌 Ticket",
            value=canal.name,
            inline=False
        )

        embed_dm.set_footer(
            text="Sistema de Tickets • Divina Rp"
        )

        view_dm = View()

        view_dm.add_item(

            discord.ui.Button(
                label="Abrir Transcript",
                style=discord.ButtonStyle.link,
                url="https://discord.com"
            )
        )

        if membro:

            try:

                await membro.send(
                    embed=embed_dm,
                    file=discord.File("transcript.html"),
                    view=view_dm
                )

            except:
                pass

        # 📄 LOG
        embed_log = discord.Embed(
            title="❌ Ticket Fechado",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )

        embed_log.add_field(
            name="👮 Staff",
            value=interaction.user.mention
        )

        embed_log.add_field(
            name="📄 Canal",
            value=canal.name
        )

        if log_channel:

            await log_channel.send(
                embed=embed_log,
                file=discord.File("transcript.html")
            )

        if membro:

            tickets_abertos.pop(membro.id, None)

        await canal.delete()

# 📩 MENU
class TicketSelect(Select):

    def __init__(self):

        options = [

            discord.SelectOption(
                label="Denúncia",
                emoji="⚠️"
            ),

            discord.SelectOption(
                label="Doação",
                emoji="💰"
            ),

            discord.SelectOption(
                label="Suporte",
                emoji="🛠️"
            ),

            discord.SelectOption(
                label="ADV",
                emoji="🚨"
            ),
        ]

        super().__init__(
            placeholder="Escolha uma opção...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer(
            ephemeral=True
        )

        escolha = self.values[0]

        guild = interaction.guild

        user = interaction.user

        if user.id in tickets_abertos:

            await interaction.followup.send(
                "❌ Você já possui um ticket aberto.",
                ephemeral=True
            )

            return

        categoria = guild.get_channel(
            CATEGORIAS[escolha]
        )

        overwrites = {

            guild.default_role:
            discord.PermissionOverwrite(
                read_messages=False
            ),

            user:
            discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True
            )
        }

        staff_mentions = []

        for role_id in STAFF_ROLES:

            role = guild.get_role(role_id)

            if role:

                overwrites[role] = discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True
                )

                staff_mentions.append(
                    role.mention
                )

        canal = await guild.create_text_channel(

            name=f"{escolha.lower()}-{user.name}",

            category=categoria,

            overwrites=overwrites
        )

        tickets_abertos[user.id] = canal.id

        log_channel = guild.get_channel(
            LOG_CHANNEL_ID
        )

        embed_log = discord.Embed(
            title="📩 Ticket Aberto",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )

        embed_log.add_field(
            name="👤 Usuário",
            value=user.mention
        )

        embed_log.add_field(
            name="📌 Tipo",
            value=escolha
        )

        embed_log.add_field(
            name="📄 Canal",
            value=canal.mention
        )

        if log_channel:

            await log_channel.send(
                embed=embed_log
            )

        view = View()

        view.add_item(
            FecharButton()
        )

        embed_ticket = discord.Embed(
            title=f"📩 Ticket de {escolha}",
            description="""
A equipe foi notificada.

⏳ Aguarde atendimento.
            """,
            color=discord.Color.green()
        )

        embed_ticket.set_footer(
            text="Sistema de Tickets • Divina Rp"
        )

        await canal.send(
            content=" ".join(staff_mentions) + f" {user.mention}",
            embed=embed_ticket,
            view=view
        )

        await interaction.followup.send(
            f"✅ Ticket criado: {canal.mention}",
            ephemeral=True
        )

# 🎛️ VIEW
class TicketView(View):

    def __init__(self):

        super().__init__(timeout=None)

        self.add_item(
            TicketSelect()
        )

# 📌 COG
class Ticket(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command()
    async def ticket(self, ctx):

        embed = discord.Embed(
            title="📩 Sistema de Tickets",
            description="""
🟢 Sistema Online

Selecione uma opção abaixo:

⚠️ Denúncia
💰 Doação
🛠️ Suporte
🚨 ADV
            """,
            color=discord.Color.green()
        )

        embed.set_footer(
            text="Sistema de atendimento Divina Rp"
        )

        await ctx.send(
            embed=embed,
            view=TicketView()
        )

async def setup(bot):

    await bot.add_cog(
        Ticket(bot)
    )