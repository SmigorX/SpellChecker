import discord
from discord.ext import commands
from spellcheck import spell_check  # Import your spell_check function from spellcheck.py
from env import secret
from langdetect import detect

intents = discord.Intents.default()

intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='', intents=intents)

# IDs of users who should trigger spell check (replace with actual user IDs)
allowed_user_ids = [123, 123]

# ID of the channel where the bot should listen (replace with actual channel ID)
allowed_channel_id = 1234567890

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Event listener for message events

@bot.event
async def on_message(message):
    print(f"Message received: {message.content}")
    if message.author.bot:  # Ignore messages from bots
        return

    # Check if the message is from an allowed user and in the allowed channel
    if message.author.id in allowed_user_ids and message.channel.id == allowed_channel_id:
        original_text = message.content

        language = detect(original_text)
        if language != 'pl':
            print(f"Message is not in Polish, but in {language}")
            return

        # Perform spell check and get corrections and mistakes
        corrected_text, mistakes = spell_check(original_text)

        if mistakes:
            # If there are mistakes, prepare the correction message
            correction_message = f"Hey {message.author.mention}, I found some mistakes:\n"
            for mistake, correction in mistakes:
                correction_message += f"{mistake} -> {correction}\n"

            # Send the correction message
            await message.channel.send(correction_message)
        else:
            # No mistakes found, do nothing
            return

    await bot.process_commands(message)  # Ensure other commands are processed

bot.run(secret)
