import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def main():
    initial_extensions = [
        "cogs.dynamicMemory",
        "cogs.filters",
        "cogs.learning",
    ]
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"Extension {extension} loaded successfully.")
        except Exception as e:
            print(f"Error loading extension {extension}: {e}")

    await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())