import asyncio
import json
import os
from pathlib import Path

import discord
from discord.ext import commands

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"

with CONFIG_PATH.open("r", encoding="utf-8") as f:
    config = json.load(f)

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=config.get("prefix", "!"),
    intents=intents
)

@bot.event
async def on_ready():
    print(f"✅ Bot online: {bot.user}")

async def carregar():
    for pasta in ["commands", "events", "cogs"]:
        pacote = f"{pasta}"
        pasta_path = BASE_DIR / pasta

        if not pasta_path.exists():
            continue

        for arquivo in os.listdir(pasta_path):
            if not arquivo.endswith(".py") or arquivo == "__init__.py":
                continue

            extension = f"{pacote}.{arquivo[:-3]}"
            try:
                await bot.load_extension(extension)
                print(f"✅ Carregado: {extension}")
            except Exception as exc:
                print(f"❌ Falha ao carregar {extension}: {exc}")

async def main():
    async with bot:
        await carregar()

        TOKEN = os.getenv("TOKEN")

        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
