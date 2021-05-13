from aiohttp.client import ClientSession
import discord, json
import time
import aiohttp
import datetime
import sys
from datetime import datetime
from discord import Webhook, AsyncWebhookAdapter
from discord import client
from discord import message
from discord.ext import tasks, commands
from io import BytesIO
from colorama import Fore, Back, Style, init
from discord.ext.commands.core import Command

with open('./Settings.json') as m:
    Settings = json.load(m)
token = Settings.get('token')
webhook = Settings.get('webhook')
prefix = Settings.get('prefix')
clientid = Settings.get('client_id')
bot = commands.Bot(command_prefix=prefix, self_bot=True)
bot.remove_command("help")
bot.session = aiohttp.ClientSession()

webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(bot.session))

@bot.event
async def on_ready():
    global timestart
    timestart = datetime.now()
    init(autoreset=True)
    print(Fore.CYAN + '''
• ▌ ▄ ·.  ▄▄▄·  ▄▄·       .▄▄ · 
·██ ▐███▪▐█ ▀█ ▐█ ▌▪▪     ▐█ ▀. 
▐█ ▌▐▌▐█·▄█▀▀█ ██ ▄▄ ▄█▀▄ ▄▀▀▀█▄
██ ██▌▐█▌▐█ ▪▐▌▐███▌▐█▌.▐▌▐█▄▪▐█
▀▀  █▪▀▀▀ ▀  ▀ ·▀▀▀  ▀█▄▀▪ ▀▀▀▀                        
''')
    print(Fore.MAGENTA+' BOT INFO AND SETTINGS BELLOW!!')
    print(Fore.MAGENTA+'--------------------------------')
    print(Fore.CYAN+f' Logged in as {bot.user}!')
    print(Fore.MAGENTA+'--------------------------------')
    print(Fore.CYAN+f' Current Prefix is: {prefix}')
    print(Fore.MAGENTA+'----------------------')
    embed = discord.Embed(color=discord.Color.green(), description="Welcome to MacOS!")
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.set_author(name=bot.user, icon_url=bot.user.avatar_url)
    embed.timestamp = datetime.utcnow()
    await webhook.send(embed=embed)

#COMMANDS BELOW
@bot.command()
async def hello(ctx):
    await ctx.message.delete()
    await webhook.send("Hello World!")

@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        color = discord.Color.red()
    ) 
    embed.set_author(name='CMDS LIST FOR MACOS')
    embed.add_field(name=f'{prefix}hello', value='Says Hello World!', inline=False)
    embed.add_field(name=f'{prefix}userinfo/ui', value='Sends user info', inline=False)
    embed.add_field(name=f'{prefix}nuke', value='Deletes all channels in a server', inline=False)
    embed.add_field(name=f'{prefix}spam', value='Spams all channels with a message of your choice', inline=False)
    embed.add_field(name=f'{prefix}massrename', value='Renames all memebers', inline=False)
    embed.add_field(name=f'{prefix}emoji/e, link and then name', value='emoji stealer:)', inline=False)
    embed.add_field(name=f'{prefix}shutdown', value='logs out', inline=False)
    embed.add_field(name=f'{prefix}embed', value='embeds text', inline=False)
    embed.add_field(name=f'{prefix}statushelp', value='sends all status cmds', inline=False)
    await ctx.message.delete()
    await webhook.send(embed=embed)

@bot.command(aliases=["ui"])
async def userinfo(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    print(f"user info of {member} sent!")
    roles = [role for role in member.roles]

    embed = discord.Embed(color=discord.Color.random(), timestamp=ctx.message.created_at)
    embed.set_author(name=f"User info of - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
    embed.add_field(name="ID: ", value=member.id)
    embed.add_field(name="Username: ", value=member.display_name)
    embed.add_field(name="Account made on: ", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name=f"Roles ({len(roles)})", value= " ".join([role.mention for role in roles]))
    embed.add_field(name="Bot?:", value=member.bot)

    await ctx.message.delete()
    await webhook.send(embed=embed)
@bot.command()
async def nuke(ctx):
    await ctx.message.delete()
    msg = discord.Embed(color=discord.Color.gold(), timestamp=ctx.message.created_at)
    msg.set_author(name=f"Nuked {ctx.guild.name}!")
    msg.set_image(url="https://lh3.googleusercontent.com/proxy/0UrEOemDG11qx3UuGCCCcePPuRGnrvaPpFatFT59E3NdLSQjcpQ5HJsctpMHRdXoi-2NnQNm6o48-8XQFWYHQh7C-uJgZZ0")
    await webhook.send(embed=msg)
    for c in ctx.guild.channels:
        await c.delete()

@bot.command()
async def spam(ctx, *, msg):
    await ctx.message.delete()
    num = 10
    for x in range(num):

        for channel in ctx.guild.text_channels:
            try:
                await channel.send(msg)
            except:
                continue
    
@bot.command(pass_context=True)
async def massrename(ctx, nick):
    await ctx.message.delete()
    for guild in bot.guilds:
        for member in guild.members:
            await member.edit(nick=nick)

@bot.command(aliases=['e'])
async def emoji(ctx, url: str, *, name):
    async with bot.session.get(url) as r:
        try:
            if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                emoji = await ctx.guild.create_custom_emoji(image=bytes, name=name)
                await webhook.send(f"Emoji Made: {emoji}")
            else:
                await webhook.send("ERROR 404")
        except discord.HTTPException:
            await webhook.send("`ERROR IMAGE SIZE TOO LARGE OR WRONG FORMAT!`")


@bot.command()
async def shutdown(ctx):
    await ctx.message.delete()
    shutdown = discord.Embed(color=discord.Color.dark_red(), description="MacOS has shutdown!")
    await webhook.send(embed=shutdown)
    sys.exit(0)

@bot.command()
async def embed(ctx, msg):
    await ctx.message.delete()
    message = discord.Embed(color=discord.Color.random(), description=msg)
    await ctx.send(embed=message)

@bot.command()
async def statusP(ctx, *, status):
    await ctx.message.delete()
    statusP = discord.Embed(color=discord.Color.red(), description=f"Changed Status to Playing {status}")
    await webhook.send(embed=statusP)
    await bot.change_presence(activity=discord.Game(status))

@bot.command()
async def statusL(ctx, *, status):
    await ctx.message.delete()
    statusL = discord.Embed(color=discord.Color.red(), description=f"Changed Status to Listning to {status}")
    await webhook.send(embed=statusL)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))

@bot.command()
async def statusW(ctx, *, status):
    await ctx.message.delete()
    statusW = discord.Embed(color=discord.Color.red(), description=f"Changed Status to Watching {status}")
    await webhook.send(embed=statusW)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

@bot.command()
async def removestatus(ctx):
    await ctx.message.delete()
    remove = discord.Embed(color=discord.Color.red(), description="Removed Status!")
    await webhook.send(embed=remove)
    await bot.change_presence(activity=None)

@bot.command(pass_context=True)
async def statushelp(ctx):
    author = ctx.message.author
    status = discord.Embed(
        color = discord.Color.red()
    ) 
    status.set_author(name='STATUS OPTIONS')
    status.add_field(name=f'{prefix}statusP', value='Sets status to Playing along with text of your choice', inline=False)
    status.add_field(name=f'{prefix}statusW', value='Sets status to Watching along with text of your choice', inline=False)
    status.add_field(name=f'{prefix}statusL', value='Sets status to Listening along with text of your choice', inline=False)
    status.add_field(name=f'{prefix}removestatus', value='removes current status', inline=False)
    await ctx.message.delete()
    await webhook.send(embed=status)




bot.run(token, bot=False)
