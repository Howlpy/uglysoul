from discord.ext import commands
from utils.general import is_in_allowed_category
import random

class Filters(commands.Cog):
    def __init__(self, bot, dynamic_memory):
        self.bot = bot
        self.response_queue = []
        self.dynamic_memory = dynamic_memory

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if not is_in_allowed_category(message):
            return

        print(f"Message received: {message.content}")
        self.dynamic_memory.learn_from_message(message)

        response = self.dynamic_memory.generate_response(message)
        if response:
            print(f"Response generated: {response}")
            self.add_response(response)

        while self.response_queue:
            response = self.response_queue.pop(0)  
            await message.reply(response)  
            
        await self.bot.process_commands(message)

    def add_response(self, response):
        self.response_queue.append(response)

async def setup(bot):
    dynamic_memory_cog = bot.get_cog("DynamicMemory")
    await bot.add_cog(Filters(bot, dynamic_memory_cog))