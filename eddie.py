#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Discord bot for managing courses.

Author: Emilia Dunfelt (emilia@dunfelt.se)
Created: 2022-02-14
Modified: 2022-02-15
"""
import os
import discord
from discord.ext import commands
import pydoc

# envs
TOKEN = os.getenv("DISCORD_TOKEN")

# intents
intents = discord.Intents.default()
intents.members = True

# bot settings
bot = commands.Bot(command_prefix="!", intents=intents, description="Your friendly shipboard robot, equipped with a GPP (Genuine People Personality) for your convenience.")

def bot_msg(msg):
    """Check if message was sent by bot"""
    return msg.author == bot.user

def bot_perms(user):
    """Check if user has 'bots' role"""
    roles = [r.name for r in user.roles]
    if "bots" in roles:
        return True
    else:
        return False

# commands
@bot.command()
async def ping(ctx, help="check if bot is up by ping"):
    """Check bot status (available to everyone)"""
    await ctx.send("pong")

@bot.command()
@commands.has_role("bots")
async def toggle(ctx, channel="queue", help="toggle queue channel"):
    """Lock/Unlock write-permissions for regular members"""
    server = ctx.guild
    
    #overwrite to apply
    overwrite = discord.PermissionOverwrite()
    overwrite.send_messages = False
    
    # channel and users to change perms for
    queue = discord.utils.get(server.channels, name=channel)
    everyone = server.default_role
    
    # channel not found
    if not queue:
        await ctx.send(f"Sorry, I could not find a channel named `#{channel}` in here. Did you forget to add it?", delete_after=5)
        await ctx.message.delete(delay=5)
        return

    # lock/unlock
    if queue.permissions_synced:
        await queue.set_permissions(everyone, overwrite=overwrite)
        await queue.purge(limit=100, check=bot_msg)
        confirmation = f"I locked the channel `#{channel}`!"
        queue_msg = "The queue is locked for now, it will be opened again before the next lab session. Happy hacking!"
    else:
        await queue.set_permissions(everyone, overwrite=None)
        await queue.purge(limit=100, check=bot_msg)
        confirmation = f"I unlocked the channel `#{channel}`!"
        queue_msg = "The queue is now open! Please type your name and wait for a TA to call you to a voice channel."
    
    await ctx.send(confirmation)
    await queue.send(queue_msg)

@bot.command()
async def docs(ctx, search, help="fetch docs"):
    """Fetch Python documentation"""
    docs = pydoc.render_doc(search, renderer=pydoc.plaintext)
    await ctx.send(f"What does {search} do... Great question! Here are the docs:\n```{docs}\n```")

# events
@bot.event
async def on_ready():
    """Bot ready message and presence"""   
    await bot.change_presence(activity=discord.Game("the Heart of Gold"))
    print("Eddie is ready!")

@bot.event
async def on_disconnect():
    print("Eddie has left.")

@bot.listen("on_message")
async def on_message(msg):
    """Listen for TAs calling students in the queue"""
    channel = msg.channel.name

    if channel not in ["queue", "kö"] or not bot_perms(msg.author) or not msg.reference:
        return
        
    await msg.add_reaction("✅")

@bot.event
async def on_reaction_add(reaction, user):
    """Delete messages on checkmark react from TA"""
    # get message and referenced message
    msg = reaction.message
    ref = await msg.channel.fetch_message(msg.reference.message_id)
    
    if user.bot or reaction.emoji != "✅" or not bot_perms(user):
        return
    
    await ref.delete()
    await msg.delete()

@bot.event
async def on_member_join(member):
    """Sends DM to students joining the server"""
    message = f"""
Hej {member.name},
    
Welcome to the Discord server for this course! In the server you can reach \
our for help from our TAs and teachers, as well as interact with other students. 

The server is meant to be a welcoming and friendly place, so please treat \
everyone with respect and patience. We also encourage you to change your \
user name in the server (the Server Profile) to your real name. If you \
need help getting started - don't hesitate to ask!

There might be more specific rules for this course's Discord server, so \
please read what's posted in the #rules channel before proceeding.

    
Best regards,
the Teachers and TAs
"""
    await member.create_dm()
    await member.dm_channel.send(message)

@bot.event
async def on_command_error(ctx, error):
    """Basic error messages"""
    if isinstance(error, commands.MissingRole):
        msg = "Sorry, you don't have permission to do that. Ask a course responsible for help!"
    elif isinstance(error, commands.MissingRequiredArgument):
        msg = f"You forgot an argument: `{error.param}`. Please try again!"
    elif isinstance(error, commands.CommandNotFound):
        msg = "I don't know that command. Check out the `>help` for more info on what I can do!"
    else:
        msg = "Something went wrong! Ask a course responsible for help."

    await ctx.send(msg, delete_after=5)
    await ctx.message.delete(delay=5)


# run client using TOKEN from .env file    
bot.run(TOKEN)
