from asyncio import events
from logging import exception
from aiohttp.client import ClientSession, request
import discord, json, aiohttp, asyncio, datetime, requests, sys, re
import httpx
import os 
from os import system
from datetime import date, datetime
from discord.ext.commands import CommandNotFound
from discord import Webhook, AsyncWebhookAdapter
from discord import client
from discord import message
from discord.ext import tasks, commands
from io import BytesIO
from colorama import Fore, Back, Style, init
from discord.ext.commands.core import Command

version = "V.3"
system(f'title MacOS SelfBot {version}')
with open('./Settings.json') as m:
    Settings = json.load(m)
token = Settings.get('token')
webhook = Settings.get('webhook')
prefix = Settings.get('prefix')
bot = commands.Bot(command_prefix=prefix, self_bot=True)
bot.remove_command("help")

init(autoreset=True)
print(Fore.LIGHTCYAN_EX + '''
• ▌ ▄ ·.  ▄▄▄·  ▄▄·       .▄▄ · 
·██ ▐███▪▐█ ▀█ ▐█ ▌▪▪     ▐█ ▀. 
▐█ ▌▐▌▐█·▄█▀▀█ ██ ▄▄ ▄█▀▄ ▄▀▀▀█▄
██ ██▌▐█▌▐█ ▪▐▌▐███▌▐█▌.▐▌▐█▄▪▐█
▀▀  █▪▀▀▀ ▀  ▀ ·▀▀▀  ▀█▄▀▪ ▀▀▀▀                        
''')
print(Fore.LIGHTMAGENTA_EX+'--------------------------------')

@bot.event
async def on_connect():
    init(autoreset=True)
    print(Fore.LIGHTGREEN_EX+f" {bot.user} is now online..")
    print(Fore.LIGHTMAGENTA_EX+'--------------------------------')


@bot.event
async def on_ready():
    webhook = Settings.get('webhook')
    bot.session = aiohttp.ClientSession()
    webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(bot.session))
    global timestart
    timestart = datetime.now()
    init(autoreset=True)
    print(Fore.LIGHTMAGENTA_EX+' USER INFO AND SETTINGS BELLOW!!')
    print(Fore.LIGHTMAGENTA_EX+'')
    print(Fore.LIGHTCYAN_EX+f' Logged in as: {bot.user}!')
    print(Fore.LIGHTCYAN_EX+f' User id is: {bot.user.id}!')
    print(Fore.LIGHTCYAN_EX+f' Total guilds: {len(bot.guilds)}')
    print(Fore.LIGHTCYAN_EX+f' Total friends: {len(bot.user.friends)}')
    print(Fore.LIGHTMAGENTA_EX+'--------------------------------')
    print(Fore.LIGHTCYAN_EX+f' Current Prefix is | {prefix}')
    print(Fore.LIGHTMAGENTA_EX+'----------------------------')
    print(Fore.LIGHTMAGENTA_EX+f' MACOS SELFBOT VERSION | {version}')
    embed = discord.Embed(color=discord.Color.green(), description="Welcome to MacOS!")
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.set_author(name=bot.user, icon_url=bot.user.avatar_url)
    embed.timestamp = datetime.utcnow()
    await webhook.send(embed=embed, username=bot.user.name, avatar_url=bot.user.avatar_url)
#COMMANDS BELOW
@bot.command()
async def hello(ctx):
    await ctx.message.delete()
    await webhook.send("Hello World!", username=bot.user.name, avatar_url=bot.user.avatar_url)

@bot.command(pass_context=True)
async def help(ctx):
    webhook = Settings.get('webhook')
    bot.session = aiohttp.ClientSession()
    webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(bot.session))
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
    embed.add_field(name=f'{prefix}avatarhelp', value='sends all avatar cmds', inline=False)
    await ctx.message.delete()
    await webhook.send(embed=embed, username=bot.user.name, avatar_url=bot.user.avatar_url)

@bot.command(aliases=["ui"])
async def userinfo(ctx, member: discord.Member = None):
    webhook = Settings.get('webhook')
    bot.session = aiohttp.ClientSession()
    webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(bot.session))
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
    embed.add_field(name=f"Roles ({len(roles)})", value= " ".join([role.name for role in roles]))
    embed.add_field(name="Bot?:", value=member.bot)

    await ctx.message.delete()
    await webhook.send(embed=embed, username=bot.user.name, avatar_url=bot.user.avatar_url)

@bot.command()
async def nuke(ctx):
    webhook = Settings.get('webhook')
    bot.session = aiohttp.ClientSession()
    webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(bot.session))
    await ctx.message.delete()
    msg = discord.Embed(color=discord.Color.gold(), timestamp=ctx.message.created_at)
    msg.set_author(name=f"Nuked {ctx.guild.name}!")
    msg.set_image(url="https://lh3.googleusercontent.com/proxy/0UrEOemDG11qx3UuGCCCcePPuRGnrvaPpFatFT59E3NdLSQjcpQ5HJsctpMHRdXoi-2NnQNm6o48-8XQFWYHQh7C-uJgZZ0")
    await webhook.send(embed=msg, username=bot.user.name, avatar_url=bot.user.avatar_url)
    for c in ctx.guild.channels:
        await c.delete()

@bot.command()
async def spam(ctx, *, msg):
    webhook = Settings.get('webhook')
    bot.session = aiohttp.ClientSession()
    webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(bot.session))
    await ctx.message.delete()
    num = 10
    for x in range(num):
        for channel in ctx.guild.text_channels:
            try:
                await channel.send(msg)
            except:
                continue

@bot.command(aliases=['e'])
async def emoji(ctx, url: str, *, name):
    webhook = Settings.get('webhook')
    bot.session = aiohttp.ClientSession()
    webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(bot.session))
    await ctx.message.delete()
    async with bot.session.get(url) as r:
        try:
            if r.status in range (200, 299):
                img = BytesIO(await r.read())
                bytes = img.getvalue()
                emoji = await ctx.guild.create_custom_emoji(image=bytes, name=name)
                success = discord.Embed(color=discord.Color.green(), description=F"Emoji made! {emoji}")
                await webhook.send(embed=success, username=bot.user.name, avatar_url=bot.user.avatar_url)
            else:
                error1 = discord.Embed(color=discord.Color.dark_red(), description=F"!!ERROR|UNKNOWN!!")
                await webhook.send(embed=error1, username=bot.user.name, avatar_url=bot.user.avatar_url)
        except discord.HTTPException:
            error2 = discord.Embed(color=discord.Color.red(), description=F"ERROR|UNSUPPORTED IMAGE TYPE OR FILE TOO LARGE")
            await webhook.send(embed=error2, username=bot.user.name, avatar_url=bot.user.avatar_url)


@bot.command()
async def shutdown(ctx):
    webhook = Settings.get('webhook')
    bot.session = aiohttp.ClientSession()
    webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(bot.session))
    await ctx.message.delete()
    shutdown = discord.Embed(color=discord.Color.dark_red(), description="MacOS has shutdown!")
    await webhook.send(embed=shutdown, username=bot.user.name, avatar_url=bot.user.avatar_url)
    sys.exit(0)

@bot.command()
async def embed(ctx, msg):
    await ctx.message.delete()
    message = discord.Embed(color=discord.Color.random(), description=msg)
    await ctx.send(embed=message, username=bot.user.name, avatar_url=bot.user.avatar_url)

@bot.command()
async def statusP(ctx, *, status):
    webhook = Settings.get('webhook')
    bot.session = aiohttp.ClientSession()
    webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(bot.session))
    await ctx.message.delete()
    statusP = discord.Embed(color=discord.Color.green(), description=f"Changed Status to Playing {status}")
    await webhook.send(embed=statusP, username=bot.user.name, avatar_url=bot.user.avatar_url)
    await bot.change_presence(activity=discord.Game(status))

@bot.command()
async def statusL(ctx, *, status):
    webhook = Settings.get('webhook')
    bot.session = aiohttp.ClientSession()
    webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(bot.session))
    await ctx.message.delete()
    statusL = discord.Embed(color=discord.Color.green(), description=f"Changed Status to Listning to {status}")
    await webhook.send(embed=statusL, username=bot.user.name, avatar_url=bot.user.avatar_url)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))

@bot.command()
async def statusW(ctx, *, status):
    webhook = Settings.get('webhook')
    bot.session = aiohttp.ClientSession()
    webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(bot.session))
    await ctx.message.delete()
    statusW = discord.Embed(color=discord.Color.green(), description=f"Changed Status to Watching {status}")
    await webhook.send(embed=statusW, username=bot.user.name, avatar_url=bot.user.avatar_url)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

@bot.command()
async def removestatus(ctx):
    webhook = Settings.get('webhook')
    bot.session = aiohttp.ClientSession()
    webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(bot.session))
    await ctx.message.delete()
    remove = discord.Embed(color=discord.Color.red(), description="Removed Status!")
    await webhook.send(embed=remove, username=bot.user.name, avatar_url=bot.user.avatar_url)
    await bot.change_presence(activity=None)

@bot.command(pass_context=True)
async def statushelp(ctx):
    webhook = Settings.get('webhook')
    bot.session = aiohttp.ClientSession()
    webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(bot.session))
    status = discord.Embed(
        color = discord.Color.red()
    ) 
    status.set_author(name='STATUS OPTIONS')
    status.add_field(name=f'{prefix}statusP', value='Sets status to Playing along with text of your choice', inline=False)
    status.add_field(name=f'{prefix}statusW', value='Sets status to Watching along with text of your choice', inline=False)
    status.add_field(name=f'{prefix}statusL', value='Sets status to Listening along with text of your choice', inline=False)
    status.add_field(name=f'{prefix}removestatus', value='removes current status', inline=False)
    await ctx.message.delete()
    await webhook.send(embed=status, username=bot.user.name, avatar_url=bot.user.avatar_url)

@bot.command()
async def avj(ctx, member: discord.Member = None):
    webhook = Settings.get('webhook')
    bot.session = aiohttp.ClientSession()
    webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(bot.session))
    member = ctx.author if not member else member
    await ctx.message.delete()
    jpg = discord.Embed(color=discord.Color.green(), description=f"Saved pfp of {member}")
    await member.avatar_url_as(format="jpg").save(fp=f"{member}.jpg")
    await webhook.send(embed=jpg, username=bot.user.name, avatar_url=bot.user.avatar_url)

@bot.command()
async def avg(ctx, member: discord.Member = None):
    webhook = Settings.get('webhook')
    bot.session = aiohttp.ClientSession()
    webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(bot.session))
    member = ctx.author if not member else member
    await ctx.message.delete()
    gif = discord.Embed(color=discord.Color.green(), description=f"Saved pfp of {member}")
    await member.avatar_url_as(format="gif").save(fp=f"{member}.gif")
    await webhook.send(embed=gif, username=bot.user.name, avatar_url=bot.user.avatar_url)

@bot.command(pass_context=True)
async def avatarhelp(ctx):
    webhook = Settings.get('webhook')
    bot.session = aiohttp.ClientSession()
    webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(bot.session))
    avatar = discord.Embed(
        color = discord.Color.red()
    ) 
    avatar.set_author(name='STATUS OPTIONS')
    avatar.add_field(name=f'{prefix}avj', value='Saves a users pfp as a jpg', inline=False)
    avatar.add_field(name=f'{prefix}avg', value='Saves a users pfp as a gif', inline=False)
    await ctx.message.delete()
    await webhook.send(embed=avatar, username=bot.user.name, avatar_url=bot.user.avatar_url)

@bot.command()
async def guild(ctx):
    webhook = Settings.get('webhook')
    bot.session = aiohttp.ClientSession()
    webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(bot.session))
    icon = ctx.guild.icon_url
    await ctx.message.delete()
    jpg = discord.Embed(color=discord.Color.green(), description=f"{icon}")
    await webhook.send(embed=jpg, username=bot.user.name, avatar_url=bot.user.avatar_url)

@bot.command(aliases=["av"])
async def avatar(ctx, member: discord.Member = None):
    webhook = Settings.get('webhook')
    bot.session = aiohttp.ClientSession()
    webhook = Webhook.from_url(webhook, adapter=AsyncWebhookAdapter(bot.session))
    member = ctx.author if not member else member
    show_avatar = discord.Embed(

        color = discord.Color.random()
    )
    show_avatar.set_author(icon_url=member.avatar_url, name=f"Avatar of {member}")
    show_avatar.set_image(url='{}'.format(member.avatar_url))
    await webhook.send(embed=show_avatar, username=bot.user.name, avatar_url=bot.user.avatar_url)

bot.run(token, bot=False)
