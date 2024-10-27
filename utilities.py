import json
import discord

# function to load configuration data from config.json, copied from main.py
def load_config():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config

config = load_config()
pf = config['prefix']
server_name = config['server_name']

async def format_help():
    # Read the contents of the text file
    with open("help.txt", "r") as file:
        content = file.read()

    formatted_content = content.format(pf=pf)

    return formatted_content

async def ping(message, client):
    latency = round(client.latency * 1000, 2)
    await message.channel.send(f'Ping: {latency} ms') 

async def help(message):
    help_message = await format_help()
    help_embed = discord.Embed(title=f'{server_name} Bot Commands', description=help_message)
    await message.channel.send(embed=help_embed)
    

