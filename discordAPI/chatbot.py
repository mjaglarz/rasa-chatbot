import os, requests
import discord
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    print(f'{message.author}: {message.content}')

    if message.author == client.user:
        return

    r = requests.post('http://localhost:5005/webhooks/rest/webhook',
                      json={"sender": str(message.author), "message": message.content})
    response = r.json()
    print(response)

    reply = ''
    for line in response:
        reply = reply + '\n' + line.get('text')
    try:
        await message.channel.send(reply)
    except:
        await message.channel.send("Oops, something went wrong...")


client.run(TOKEN)