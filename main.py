import discord
import json
import utilities
import fun

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
pf = prefix

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
        if message.content.startswith(prefix):
            
            # split the message
            content = message.content
            parts = content.split()

            if message.author.id in blacklisted_users:
                return
        
            elif message.content.startswith(f'{pf}snipe'):
                await fun.snipe(message, deleted_embeds)

            elif message.content.startswith(f"{pf}ping"):
                await utilities.ping(message, client)

            elif message.content.startswith(f"{pf}annoy"):
                target = message.mentions[0]
                await fun.annoy(message, target)

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
