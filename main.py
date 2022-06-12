import discord
import os
import requests
import random
import json
from tinydb import TinyDB, Query
from tinydb.operations import set
from dotenv import load_dotenv

load_dotenv()


db = TinyDB('tezos.json')
User = Query()

client = discord.Client()
Help = ["help"]
OS = ["!os", "!oblique", "!eno", "!strategies"]

f = open("1.txt", "r")
starter_encouragements = []
for x in f:
  starter_encouragements.append(x)

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content.lower()
    channel = str(message.channel)

    print(message)
    user = message.author
    if msg.startswith('hello'):
        await message.channel.send('Hello!')

    
    if any(word in msg for word in OS):
        await message.channel.send(random.choice(starter_encouragements))

    
    if (channel == 'user-auth'):
        if any(word in msg for word in Help):
            await message.channel.send("In order to add your tezos wallet, please type the following message: add <tezos wallet address>. for ex: add tz1dqkxxmq2w5g6jzJRndFJY9E3gUdioKYK1")

        if msg.startswith("add"):
            tezos_wallet = msg.split("add ",1)[1]
            # check if user has already submitted wallet address, update if so, insert if not
            
            if (db.search(User.name == str(user))):
                await message.channel.send("Wallet already added for " + str(user) +". If you want to update it, please type the following message: update <tezos wallet address> for ex: update tz1dqkxxmq2w5g6jzJRndFJY9E3gUdioKYK1")
            else:
                db.insert({'name': str(user), 'wallet_addr': str(tezos_wallet)})
                await message.channel.send("Wallet added for " + str(user) + "!")


        if msg.startswith("update"):
            tezos_wallet = msg.split("update ",1)[1]

            if (db.search(User.name == str(user))):
                db.update(set('wallet_addr',str(tezos_wallet)), User.name == str(user))
                await message.channel.send("Wallet updated for " +str(user) + "!")



client.run(os.getenv('TOKEN'))