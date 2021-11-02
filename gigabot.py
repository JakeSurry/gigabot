import discord
import gigamememaker
from discord.ext import commands
import io
import os

#Init
intents = discord.Intents.default()
bot = commands.Bot(command_prefix = '=', intents = intents)
TOKEN = os.environ.get('gigatoken')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="'=giga based//example'"))

@bot.command(name = 'giga', pass_context = True)
async def giga(context):
    message = context.message
    await context.message.delete()
    text = message.content.upper().split(' ')
    text.pop(0)
    text = ' '.join(text)
    text = text.split('//')
    if len(text) < 2:
        giga = gigamememaker.main(text[0], '')
    else:
        giga = gigamememaker.main(text[0], text[1])
    with io.BytesIO() as image_binary:
        giga.save(image_binary, 'JPEG')
        image_binary.seek(0)
        await message.channel.send(file=discord.File(fp=image_binary, filename='giga.jpeg'))
        await message.channel.send(f'**By: {message.author.mention}**')

bot.run(TOKEN)
