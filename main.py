import discord
import json
import utilities
import fun
from mcrcon import MCRcon

global deleted_embed

# stuff
deleted_embeds = {}
blacklisted_users = []
trusted_users = []

# function to load configuration data from config.json
def load_config():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config

# load config data and values
config = load_config()
prefix = config['prefix']
token = config['token']
logging_channel = config['logging_channel_id']
bot_owner_id = config['bot_owner_id']
rcon_prefix = config['rcon_prefix']
pf = prefix
rpf = rcon_prefix

# rcon stuff
rcon_host = config['rcon_host']
rcon_port = int(config['rcon_port'])
rcon_password = config['rcon_password']

# create an MCRcon instance
mcr = MCRcon(rcon_host, rcon_password, rcon_port)
mcr = MCRcon(host=rcon_host, password=rcon_password, port=rcon_port)

print(bot_owner_id)

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# its pretty obvious what this does
@client.event
async def on_ready():
    print(f'Now logged in as {client.user}')
    game = discord.Game("with the discord API")
    await client.change_presence(status=discord.Status.online, activity=game)
    latency = round(client.latency * 1000, 2)
    print(f'Ping: {latency} ms')

# this too
@client.event
async def on_message(message):
    try:

        if message.content.startswith(rpf) and message.author.id == bot_owner_id:
            mcr.connect()
            response = mcr.command(message.content)
            print(response)
            await message.channel.send(response)
            mcr.disconnect()
            

        if message.content.startswith(prefix):
            
            # split the message
            content = message.content
            # parts = content.split()

            if message.author.id in blacklisted_users:
                return
        
            elif content.startswith(f'{pf}snipe'):
                await fun.snipe(message, deleted_embeds)

            elif content.startswith(f"{pf}ping"):
                await utilities.ping(message, client)

            elif content.startswith(f"{pf}annoy"):
                target = message.mentions[0]
                await fun.annoy(message, target)

            elif content.startswith(f"{pf}help"):
                await utilities.help(message)

    except discord.RateLimited:
        print('Rate limit detected')

@client.event
async def on_message_delete(message):
    global deleted_embeds  # Declare global dictionary to store embeds

    # Create the embed when a message is deleted
    deleted_embed = discord.Embed(title="Message Deleted", color=discord.Color.red())
    deleted_embed.add_field(name="Author", value=message.author.name)
    deleted_embed.add_field(name="Message", value=message.content)
    deleted_embed.add_field(name="Channel", value=message.channel.name)
    
    # Store the embed in the dictionary by channel ID
    deleted_embeds[message.channel.id] = deleted_embed

client.run(token)
