import feedparser
import os
import re
import discord
from discord.ext import tasks
import asyncio
from datetime import datetime

# Environment
feedurl = os.environ['FEED']
token = os.environ['TOKEN']
channel_name = os.environ['PREMIERE_CHANNEL']

# Setup Discord
bot = discord.Client(intents=discord.Intents.default())

# Login to Discord
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(datetime.now())
    print('------')
    job.start()

@tasks.loop(seconds=900)
async def job():
    # Setup feed and announcements
    feed = feedparser.parse(feedurl)
    entry = feed.entries[0]
    lastid = open("../../lastid", "r").read()
    currentid = entry.guid
    episodeno = entry.itunes_episode
    episodeurl = "https://beersinthelot.com"
    title = entry.title
    announce = 'Episode ' + episodeno + ' - ' + title + '\n' + '\n' + \
        episodeurl 
    # Get the Discord channel
    channel = discord.utils.get(bot.get_all_channels(), name=channel_name)
    # Announce new episode
    if currentid != lastid:
        print (datetime.now(),announce)
        await channel.send(announce)
        open("../../lastid", "w").write(currentid)
    else:
        print ('Up to date',datetime.now())

@job.before_loop
async def before():
    await bot.wait_until_ready()

# Run the bot
bot.run(token)