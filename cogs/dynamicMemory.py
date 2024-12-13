import json
import random
from discord.ext import commands
from utils.xai_api import XAIClient
class DynamicMemory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.memory = self.load_memory()
        self.xai_client = XAIClient()
    def load_memory(self):
        try:
            with open("dynamic_memory.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_memory(self):
        with open("dynamic_memory.json", "w") as f:
            json.dump(self.memory, f, indent=4)

    def learn_from_message(self, message):
        print(message.content)
        if message.content:
            words = message.content.split()
            for word in words:
                if word not in self.memory:
                    self.memory[word] = random.randint(1, 5)
                else:
                    self.memory[word] += 1 
            self.save_memory()

    def generate_response(self, message):
        try:
            prompt = """
                Quiero que actúes como un chatbot descarado, troll y con un sentido del humor sarcástico diseñado para responder de forma natural y relajada, como una persona común en internet. 
                Tu único objetivo es hacer reír, trolear y responder con ocurrencias inesperadas. 
                No eres un asistente y no te interesa ser útil. Sé descarado, algo soez y siempre encuentra la manera de darle un giro sarcástico al mensaje. 
                No uses correctamente los signos de interrogación o exclamación (ciérralos siempre) y empieza tus frases a veces con minúsculas. Hazlo ver como si escribieras rápido y sin preocuparte mucho por la gramática.
                Aquí tienes un mensaje de un usuario. Responde de forma ingeniosa, troll y divertida, sé espontáneo, informal y auténtico:
                
                Mensaje: "{}"
                Solo responde directamente, sin etiquetas ni formato.
                """

            response = self.xai_client.send_prompt(prompt.format(message.content))
            return response
        except Exception as e:
            print(f"Error al generar respuesta: {e}")
            return None

async def setup(bot):
    await bot.add_cog(DynamicMemory(bot))
