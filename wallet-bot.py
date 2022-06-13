import discord
import os
import requests
import random
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    database="refraction",
    user="postgres",
    password=os.getenv('DB_PASSWORD'),
    port="5433"
)

cur = conn.cursor()


client = discord.Client()
Help = ["help"]

OS = ["!os", "!oblique", "!eno", "!strategies"]
# load oblique strategies
f = open("1.txt", "r")
oblique_strategies = []
for x in f:
  oblique_strategies.append(x)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content.lower()
    channel = str(message.channel)

    #print(message)
    user = message.author
    if msg.startswith('hello'):
        await message.channel.send('Hello!')

    
    if any(word in msg for word in OS):
        await message.channel.send(random.choice(oblique_strategies))

         
    if (channel == 'user-auth'):
        if any(word in message.content for word in Help):
            await message.channel.send("In order to add your tezos wallet, please type the following instruction: **add <tezos wallet address>** for ex: **add tz1dqkxxmq2w5g6jzJRndFJY9E3gUdioKYK1**")

        if msg.startswith("add"):
            tezos_wallet = message.content.split("add ",1)[1]
            # check if user has already submitted wallet address, update if so, insert if not
            cur.execute(
                'SELECT * FROM tezos_wallets WHERE user_id = %s', (str(user),)
            )
            record = cur.fetchall()
            if (record):
                await message.channel.send("Wallet already added for " + str(user) +". If you want to update it, please type the following instruction: **update <tezos wallet address>** for ex: **update tz1dqkxxmq2w5g6jzJRndFJY9E3gUdioKYK1**")
            else:
                cur.execute(
                    'INSERT INTO tezos_wallets (user_id, tezos_wallet) VALUES (%s, %s)', (str(user), str(tezos_wallet))
                )
                conn.commit()
                await message.channel.send("Wallet added for " + str(user) + "!")


        if msg.startswith("update"):
            tezos_wallet = message.content.split("update ",1)[1]

            cur.execute(
                'SELECT * FROM tezos_wallets WHERE user_id = %s', (str(user),)
            )
            record = cur.fetchall()
            if (record):
                cur.execute( 'UPDATE tezos_wallets SET tezos_wallet = %s WHERE user_id = %s', (str(tezos_wallet),str(user)))
                conn.commit()
                await message.channel.send("Wallet updated for " +str(user) + "!")
    

client.run(os.getenv('TOKEN'))