import discord
import gigamememaker
from discord.ext import commands
import io
import os
import sys
import time
import requests

intents = discord.Intents.default()
bot = commands.Bot(command_prefix = '=', intents = intents)
GIGATOKEN = os.environ.get('gigatoken')

TENORTOKEN = 'A6XZ04FFVXXY'

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="=help"))

@bot.event
async def on_command_error(ctx, error):
    print(error)
    try:
        await ctx.message.delete()
    except discord.errors.NotFound:
        pass

    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send(f'{ctx.message.author.mention} **That is not a command.**')
    elif isinstance(error, discord.ext.commands.CommandOnCooldown):
        await ctx.send(ctx.message.author.mention+' **Please wait {:.1f} seconds before using that command again.**'.format(error.retry_after))
    else:
        await ctx.send(f'{ctx.message.author.mention} **Something went wrong with that command. Make sure you formatted it correctly.**')

bot.remove_command('help')
@bot.command(name = 'help', pass_context = True)
@commands.cooldown(1, 1, discord.ext.commands.BucketType.user)
async def help(context):
    message = context.message
    await context.message.delete()
    help_embed = discord.Embed(title='Commands:', color=0xffc021)
    giga = discord.File("giga/giga_0.jpeg", filename="giga.jpeg")
    help_embed.set_thumbnail(url='attachment://giga.jpeg')
    help_embed.add_field(name='=help', value="Shows this list: =help", inline=False)
    help_embed.add_field(name='=giga', value="Sends a meme of giga: =giga 'top text'//'bottom text'", inline=False)
    help_embed.add_field(name='=custom', value="Sends a custom meme: =custom 'top text'//'bottom text' 'url' OR 'attachment'", inline=False)
    help_embed.add_field(name='=gif', value="Sends a custom meme: =gif 'top text'//'bottom text' 'url.gif' OR 'attachment'", inline=False)
    await message.channel.send(file=giga, embed=help_embed)

@bot.command(name = 'giga', pass_context = True)
@commands.cooldown(1, 2, commands.BucketType.user)
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
    with io.BytesIO() as buffer:
        meme.save(buffer, 'JPEG')
        buffer.seek(0)
        await message.channel.send(f'**By: {message.author.mention}**', file=discord.File(fp=buffer, filename='giga.jpeg'))

@bot.command(name = 'custom', pass_context = True)
@commands.cooldown(1, 2, commands.BucketType.user)
async def custom(context):
    message = context.message
    await context.message.delete()
    text = message.content.split(' ')
    text.pop(0)
    if len(message.attachments) > 0:
        url = message.attachments[0].url
    else:
        url = text[-1]
        text.pop(-1)
    text = ' '.join(text).upper()
    text = text.split('//')
    if len(text) < 2:
        meme = gigamememaker.custom_meme(text[0], '', url)
    else:
        meme = gigamememaker.custom_meme(text[0], text[1], url)
    if meme == 'URL_ERROR':
        await message.channel.send(f'{message.author.mention} **That is not a valid URL, or it does not contain an image.**')
    elif meme == 'TOO_LARGE':
        await message.channel.send(f'{message.author.mention} **That image/gif is too large.**')
    else:
        with io.BytesIO() as buffer: 
            meme.save(buffer, 'JPEG')
            buffer.seek(0)
            await message.channel.send(f'**By: {message.author.mention}**', file=discord.File(fp=buffer, filename='giga.jpeg'))

@bot.command(name = 'gif', pass_context = True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def gif(context):
    message = context.message
    await context.message.delete()
    text = message.content.split(' ')
    text.pop(0)
    if len(message.attachments) > 0:
        url = message.attachments[0].url
    else:
        url = text[-1]
        text.pop(-1)
    text = ' '.join(text).upper()
    text = text.split('//')
    if len(text) < 2:
        frames = gigamememaker.gif_meme(text[0], '', url)
    else:
        frames = gigamememaker.gif_meme(text[0], text[1], url)
    start = time.time()
    if frames == 'URL_ERROR':
        await message.channel.send(f'{message.author.mention} **That is not a valid URL, or it does not contain an image.**')
    elif frames == 'TOO_LARGE':
        await message.channel.send(f'{message.author.mention} **That image is too large.**')
    else:
        with io.BytesIO() as buffer:
            frames[0].save(buffer, format='GIF', save_all=True, append_images=frames[1:])
            buffer.seek(0)
            await message.channel.send(f'**By: {message.author.mention}**', file=discord.File(fp=buffer, filename='giga.gif'))

bot.run(GIGATOKEN)