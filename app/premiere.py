import feedparser
import os
import re
import discord
from discord.ext import tasks
import asyncio
from datetime import datetime

# time stamping
starttime = datetime.now()

# Environment
feedurl = os.environ['FEED']
listenurl = os.environ['LISTEN']
token = os.environ['TOKEN']
channel_name = os.environ['PREMIERE_CHANNEL']

# Setup Discord
bot = discord.Client()

# Login to Discord
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    job.start()

@tasks.loop(seconds=60)
async def job():
    jobtime = datetime.now()
    restartcheck = jobtime - starttime
    # Setup feed and announcements
    feed = feedparser.parse(feedurl)
    entry = feed.entries[0]
    episodeno = entry.itunes_episode
    title = entry.title
    summary = re.sub("<.*?>", "", entry.description)
    announce = 'Episode ' + episodeno + ' - ' + title + '\n' + '\n' + \
        summary + '\n' + '\n' + \
        listenurl 
    # Get the Discord channel
    channel = discord.utils.get(bot.get_all_channels(), name=channel_name)
    # Announce new episode
    if restartcheck.total_seconds()>60:
        print (jobtime,announce)
        await channel.send(announce)
    else:
        print (jobtime,'Up to date')

@job.before_loop
async def before():
    await bot.wait_until_ready()

# Run the bot
bot.run(token)
