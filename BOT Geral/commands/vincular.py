from discord.ext import commands
import discord
import aiomysql

CARGO_ID = "1498852164192305203"

class Vincular(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if not message.content.isdigit():
            return

        player_id = int(message.content)

        try:

            conn = await aiomysql.connect(
                host="127.0.0.1",
                port=3307,
                user="root",
                password="",
                db="base"
            )

            cursor = await conn.cursor()

            await cursor.execute(
                "SELECT usado FROM whitelist WHERE id=%s",
                (player_id,)
            )

            result = await cursor.fetchone()

            if not result:
                return

            usado = result[0]

            if usado == 1:

                embed = discord.Embed(
                    title="❌ ID já utilizado",
                    color=0xff0000
                )

                return await message.reply(embed=embed)

            await cursor.execute(
                "UPDATE whitelist SET usado=1, discord=%s WHERE id=%s",
                (message.author.id, player_id)
            )

            await conn.commit()

            cargo = message.guild.get_role(CARGO_ID)

            if cargo:
                await message.author.add_roles(cargo)

            embed = discord.Embed(
                description="☑ Você foi vinculado com sucesso!",
                color=0x00ff00
            )

            await message.reply(embed=embed)

            await cursor.close()
            conn.close()

        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(Vincular(bot))