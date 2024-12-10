from discord.ext import commands

class Learning(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.memory = {}


async def setup(bot):
    await bot.add_cog(Learning(bot))
