import discord
from discord.ext import commands
from spellcheck import spell_check
from env import secret, allowed_user_ids, allowed_channel_id
from langdetect import detect
from terminal import loading_animation
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


async def handle_message(message):
    print(f"Message received: {message.content}")
    if message.author.bot:  # Ignore messages from bots
        return

    if message.author.id in allowed_user_ids and message.channel.id in allowed_channel_ids:
        original_text = message.content

        language = detect(original_text)

        if language != 'pl':
            print(f"Message is not in Polish, but in {language}")
            return

        corrected_text, mistakes = spell_check(original_text)
        print("tst")
        if mistakes:
            initial_sent_message = await loading_animation(message)

            correction_message = (f"Hey {message.author.mention}, "
                                  f"I've spotted some possible mistakes in your message. "
                                  f"Here are my guesses for what you could have meant. "
                                  f"Just remember that I'm simply a computer program and "
                                  f"I might make mistakes too! Beep! Boop!\n")
            for mistake, correction in mistakes:
                correction_message += f"{mistake} -> {correction}\n"

            await initial_sent_message.edit(content=correction_message)

        else:
            return


@bot.event
async def on_message(message):
    # Schedule the handling function as a background task
    asyncio.create_task(handle_message(message))
    await bot.process_commands(message)  # Ensure other commands are processed

bot.run(secret)
