#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Discord bot for managing courses.

Author: Emilia Dunfelt (emilia@dunfelt.se)
Created: 2022-02-14
Modified: 2022-02-14
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import pydoc

# envs
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# intents
intents = discord.Intents.default()
intents.members = True # subscribe to the privileged members intent

bot = commands.Bot(command_prefix=">", intents=intents, description="Your friendly shipboard robot, equipped with a GPP (Genuine People Personality) for your convenience.")

# events
@bot.event
async def on_ready():
    """Bot ready message and presence"""   
    await bot.change_presence(activity=discord.Game("the Heart of Gold"))
    print("Eddie is ready!")

@bot.event
async def on_member_join(member):
    """Sends DM to students joining the server"""
    message = f"""
Hej {member.name},
    
Welcome to the Discord server for this course! Here you can reach out for \
help from our TAs and teachers, as well as interact with other students. 

The server is meant to be a welcoming and friendly place, so please treat \
everyone with respect and patience. We also encourage you to change your \
user name in the server (the Server Profile) to your real name. If you \
need help getting started - don't hesitate to ask us!'

There might be more specific rules for this course's Discord server, so \
please read what's posted in the #rules channel before proceeding.

    
Best regards,
the Teachers and TAs
"""
    await member.create_dm()
    await member.dm_channel.send(message)

# commands
@bot.command()
async def ping(ctx, help="check if bot is up by ping"):
    """Check bot status (available to everyone)"""
    await ctx.send("pong")

@bot.command()
@commands.has_role("admin")
async def toggle(ctx, channel="queue", help="toggle queue channel"):
    """Lock/Unlock write-permissions for regular members"""
    server = ctx.guild
    
    #overwrite to apply
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = False
    
    # channel and users to change perms for
    queue = discord.utils.get(server.channels, name=channel)
    everyone = server.default_role
    
    if not queue:
        # channel not found
        await ctx.send(f"Sorry, I could not find a channel named `#{channel}` in here. Did you forget to add it?")
        return

    # lock/unlock
    if queue.permissions_synced:
        await queue.set_permissions(everyone, overwrite=overwrite)
        await ctx.send(f"I locked the channel `#{channel}`!")
    else:
        await queue.set_permissions(everyone, overwrite=None)
        await ctx.send(f"I unlocked the channel `#{channel}`!")

@bot.command()
async def docs(ctx, search, help="fetch docs"):
    """Fetch Python documentation"""
    docs = pydoc.render_doc(search, renderer=pydoc.plaintext)
    await ctx.send(f"What's {search}... Great question! Here are the docs:\n```{docs}\n```")
    
# run client using TOKEN from .env file    
bot.run(TOKEN)
