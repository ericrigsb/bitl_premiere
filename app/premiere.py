import feedparser
import os
import re
import schedule
import time

class Premiere:

    def __init__(self):
        feedurl = os.environ['FEED']
        self.feedurl = feedurl
        listenurl = os.environ['LISTEN']
        self.listenurl = listenurl
        
    def job(self):
        feed = feedparser.parse(self.feedurl)
        entry = feed.entries[0]
        lastid = open("lastid", "r").read()
        self.lastid = lastid
        currentid = entry.id
        self.currentid = currentid
        episodeno = entry.itunes_episode
        title = entry.title
        self.title = title
        summary = re.sub("<.*?>", "", entry.summary)
        self.summary = summary
        announce = 'New Beers in The Lot Episode!'
        self.announce = announce
        episode = 'Episode ' + episodeno + '-' + title
        self.episode = episode
        if self.currentid != self.lastid:
            print (self.announce)
            print (self.episode)
            print (self.summary)
            open("lastid", "w").write(self.currentid)
            print (self.listenurl)
        else:
            print ('Up to date')

    def sched(self):
        schedule.every(1).minutes.do(self.job)

        while True:
            schedule.run_pending()
            time.sleep(1)

premierebot = Premiere()

premierebot.sched()