import random
from discord.ext import commands
from utils.xai_api import XAIClient
from mem0 import Memory  # Import mem0 Memory class
from transformers import pipeline

class DynamicMemory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.memory = Memory()  # Initialize mem0 memory
        self.xai_client = XAIClient()
        self.sentiment_pipeline = pipeline('sentiment-analysis', model='dccuchile/bert-base-spanish-wwm-cased')

    def learn_from_message(self, message):
        user_real_name = getattr(message.author, 'real_name', message.author.name)
        sentiment = self.analyze_sentiment(message.content)
        thoughts = self.generate_thoughts(message.content, sentiment)
        liking_score = self.calculate_liking_score(sentiment)

        self.memory.store({
            'user_id': message.author.id,
            'username': message.author.name,
            'real_name': user_real_name,
            'message_content': message.content,
            'sentiment': sentiment,
            'thoughts': thoughts,
            'liking_score': liking_score,
            'timestamp': str(message.created_at)
        })

    def generate_response(self, message):
        try:
            sentiment = self.analyze_sentiment(message.content)
            thoughts = self.generate_thoughts(message.content, sentiment)
            liking_score = self.calculate_liking_score(sentiment)

            print(f"Internal Thoughts: {thoughts}")

            prompt = f"""
                Consider the following thoughts: {thoughts}
                Liking score: {liking_score}
                Adjust the response tone accordingly:
                - If liking score is high, be more playful and friendly.
                - If liking score is low, be more sarcastic and trolling.
                Now respond to the user's message: "{message.content}"
                Act as a bold, trolling, and sarcastic chatbot.
                Reply naturally, casually, and humorously.
                No proper punctuation, sometimes start with lowercase.
                Direct reply without tags or formatting and in Spanish.
            """
            response = self.xai_client.send_prompt(prompt)
            return response
        except Exception as e:
            print(f"Error generating response: {e}")
            return None

    def analyze_sentiment(self, text):
        try:
            result = self.sentiment_pipeline(text)
            return result[0]
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {'label': 'NEUTRAL', 'score': 0.5}

    def generate_thoughts(self, message_content, sentiment):
        label = sentiment['label']
        if label == 'POSITIVE':
            thoughts = "The user seems to be in a positive mood."
        elif label == 'NEGATIVE':
            thoughts = "The user seems to be in a negative mood."
        else:
            thoughts = "The user's message is neutral."
        return thoughts

    def calculate_liking_score(self, sentiment):
        label = sentiment['label']
        score = sentiment['score']
        if label == 'POSITIVE':
            liking_score = int(score * 10)
        elif label == 'NEGATIVE':
            liking_score = 10 - int(score * 10)
        else:
            liking_score = 5
        return max(1, min(10, liking_score))

async def setup(bot):
    await bot.add_cog(DynamicMemory(bot))