import discord
import os
import math
import random
import re
import requests
import time
from replit import db
from keep_alive import keep_alive

yt_api_url = 'https://www.googleapis.com/youtube/v3'
channel_id = 'UCJNky9LM9wx0cmWfrg5eUcw'
yt_vid_url = 'https://www.youtube.com/watch?v='

vid_list = []
pages = 0

def pull_vid_list():
  resp = requests.get(yt_api_url + '/search?channelId=' + channel_id + '&maxResults=50&key=' + os.getenv('YT_API_KEY'))
  time.sleep(3)
  if resp.status_code != 200:
    print('ERROR:' + resp.text) 
  else:
    pages = math.ceil(resp.json()['pageInfo']['totalResults']/50)
    for i in range (pages):
      for item in resp.json()['items']:
        vid_list.append(item['id']['videoId'])
      resp = requests.get(yt_api_url + '/search?channelId=' + channel_id + '&maxResults=50&page=' + str(i) +'&key=' + os.getenv('YT_API_KEY'))
      time.sleep(3)
      if resp.status_code != 200:
        print('ERROR:' + resp.text) 

pull_vid_list()

def string_found(string1, string2):
   if re.search(r"\b" + re.escape(string1) + r"\b", string2):
      return True
   return False

client = discord.Client()

@client.event
async def on_ready():
  print('HA??!')

@client.event
async def on_message(message):
  msg = message.content

  if message.author == client.user:
    return

  for x in message.mentions:
    if(x==client.user):
      if string_found('help', msg):
        await message.channel.send("$joke or $jokes will get you a random joke. If you mention me and ask for a video, you'll get a video.")
      elif string_found('vid', msg) or string_found('vids',msg) or string_found('video', msg) or string_found('videos', msg):
        if len(vid_list) > 0:
          await message.channel.send(yt_vid_url + random.choice(vid_list)) 
        else:
          await message.channel.send('I got nothin.')
      else:
        await message.channel.send("Haha well that's nice.")      

  if '$joke' in msg or '$jokes' in msg:
    await message.channel.send(random.choice(db['jokes']))

  if string_found('speak ill', msg):
    await message.channel.send('You know what they always say, speak ill of the dead.')

  if string_found('fat', msg):
    await message.channel.send('The other day I went to the doctor you know what he said? Open your mouth and say OINK.')

keep_alive()
client.run(os.getenv('TOKEN'))