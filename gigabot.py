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
    await bot.change_presence(activity=discord.Game(name="'=commands'"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.message.delete()
        await ctx.send(f'{ctx.message.author.mention} **That is not a command.**')

@bot.command(name = 'commands', pass_context = True)
async def commands(context):
    message = context.message
    await context.message.delete()
    help_embed = discord.Embed(title='Commands:', color=0xffc021)
    giga = discord.File("giga/giga_0.jpeg", filename="giga.jpeg")
    help_embed.set_thumbnail(url='attachment://giga.jpeg')
    help_embed.add_field(name='=commands', value="To see this list, do: =commands", inline=False)
    help_embed.add_field(name='=giga', value="To send a meme of giga, do: =giga 'top text'//'bottom text'", inline=False)
    help_embed.add_field(name='=custom', value="To send a custom meme, do: =custom 'url' 'top text'//'bottom text'", inline=False)
    await message.channel.send(file=giga, embed=help_embed)

@bot.command(name = 'giga', pass_context = True)
async def giga(context):
    message = context.message
    await context.message.delete()
    text = message.content.upper().split(' ')
    text.pop(0)
    text = ' '.join(text)
    text = text.split('//')
    if len(text) < 2:
        meme = gigamememaker.giga_meme(text[0], '')
    else:
        meme = gigamememaker.giga_meme(text[0], text[1])
    with io.BytesIO() as image_binary:
        meme.save(image_binary, 'JPEG')
        image_binary.seek(0)
        await message.channel.send(f'**By: {message.author.mention}**', file=discord.File(fp=image_binary, filename='giga.jpeg'))

@bot.command(name = 'custom', pass_context = True)
async def custom(context):
    message = context.message
    await context.message.delete()
    text = message.content.split(' ')
    text.pop(0)
    url = text[0]
    text.pop(0)
    text = ' '.join(text).upper()
    text = text.split('//')
    if len(text) < 2:
        meme = gigamememaker.custom_meme(text[0], '', url)
    else:
        meme = gigamememaker.custom_meme(text[0], text[1], url)
    if meme == 'URL_ERROR':
        await message.channel.send(f'{message.author.mention} **That is not a valid URL, or it does not contain an image.**')
    else:
        with io.BytesIO() as image_binary: 
            meme.save(image_binary, 'PNG')
            image_binary.seek(0)
            await message.channel.send(f'**By: {message.author.mention}**', file=discord.File(fp=image_binary, filename='giga.png'))

bot.run(TOKEN)