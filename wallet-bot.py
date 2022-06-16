import discord
import os
import requests
import random
import json
import psycopg2
import numpy
from dotenv import load_dotenv

print("I am bot.")
load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT')
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

    if msg.startswith('gm'):
        # make it less often, ie. 20% of time
        rndm = random.choice(range(1,6))
        if (rndm == 1):
            await message.channel.send('gm!')
    
    if any(word in msg for word in OS):
        await message.channel.send(random.choice(oblique_strategies))

    # wallet-auth channel specific commands
    if ('wallet-auth' in channel):
        if any(word in msg for word in Help):
            await message.channel.send("In order to add your tezos wallet, please type the following instruction: **add + your tezos wallet address** for example: **add tz1dqkxxmq2w5g6jzJRndFJY9E3gUdioKYK1**")

        if msg.startswith("add"):
            try: 
                tezos_wallet = message.content.split("add ",1)[1]
            except:
                tezos_wallet = -1
            if (tezos_wallet == -1):
                await message.channel.send("Incorrect format. Please type the following instruction: **add + your tezos wallet address** for example: **add tz1dqkxxmq2w5g6jzJRndFJY9E3gUdioKYK1**")
            else:
                # check if user has already submitted wallet address, update if so, insert if not
                
                cur.execute(
                    'SELECT * FROM tezos_wallets WHERE user_id = %s', (str(user),)
                )
                record = cur.fetchall()
                if (record):
                    await message.channel.send("Wallet already added for " + str(user) +". If you want to update it, please type the following instruction: **update <tezos wallet address>** for example: **update tz1dqkxxmq2w5g6jzJRndFJY9E3gUdioKYK1**")
                else:
                    cur.execute(
                        'INSERT INTO tezos_wallets (user_id, tezos_wallet) VALUES (%s, %s)', (str(user), str(tezos_wallet))
                    )
                    conn.commit()
                    await message.channel.send("Wallet added for " + str(user) + "!")


        if msg.startswith("update"):
            try: 
                tezos_wallet = message.content.split("update ",1)[1]
            except:
                tezos_wallet = -1
            if (tezos_wallet == -1):
                await message.channel.send("Incorrect format. Please type the following instruction: **update <tezos wallet address>** for ex: **update tz1dqkxxmq2w5g6jzJRndFJY9E3gUdioKYK1**")
            else:
                cur.execute(
                    'SELECT * FROM tezos_wallets WHERE user_id = %s', (str(user),)
                )
                record = cur.fetchall()
                if (record):
                    cur.execute( 'UPDATE tezos_wallets SET tezos_wallet = %s WHERE user_id = %s', (str(tezos_wallet),str(user)))
                    conn.commit()
                    await message.channel.send("Wallet updated for " +str(user) + "!")
        
client.run(os.getenv('TOKEN'))