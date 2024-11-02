import json
import discord
import re
import mcrcon
import subprocess

# function to load configuration data from config.json, copied from main.py
def load_config():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config

# stuff
deleted_embeds = {}
blacklisted_users = []
trusted_users = []

config = load_config()
pf = config['prefix']
rpf = config['rcon_prefix']
rrpf = config['raw_rcon_prefix']
rcon_host = config['rcon_host']
rcon_port = int(config['rcon_port'])
rcon_password = config['rcon_password']
bot_owner_id = config['bot_owner_id']
server_name = config['server_name']

async def format_help():
    # Read the contents of the text file
    with open("help.txt", "r") as file:
        content = file.read()

    formatted_content = content.format(pf=pf, rpf=rpf, rrpf=rrpf)

    return formatted_content



# function to save blacklisted users to blacklisted_users.json
async def save_list(list, file):
    with open(file, 'w') as list_file:
        json.dump(list, list_file)

async def add_user(message, content, list, file, list_name):
    user_id_previous = content.split()[1]
    user_id = int(user_id_previous[2:-1])
    if user_id not in list and not user_id == bot_owner_id:
        list.append(user_id)
        await save_list(list, file)  # Save to file after adding
        await message.channel.send(f"<@{user_id}> has been added to list {list_name}.")

async def remove_user(message, content, list, file, list_name):
    user_id_previous = content.split()[1]
    user_id = user_id_previous[2:-1]
    if not "@" in user_id:
        user_id = int(content.split()[1])
    else:
        user_id = int(user_id[2:-1])
    if user_id in list:
        list.remove(user_id)
        await save_list(list, file)  # Save to file after removing
        await message.channel.send(f"<@{user_id}> has been removed from list {list_name}.")
    else:
        await message.channel.send(f"<@{user_id}> is not in list {list_name}.")



async def ping(message, client):
    latency = round(client.latency * 1000, 2)
    await message.channel.send(f'Ping: {latency} ms') 

async def help(message):
    help_message = await format_help()
    help_embed = discord.Embed(title=f'{server_name} Bot Commands', description=help_message)
    await message.channel.send(embed=help_embed)

async def startserver(message, command):
    await message.channel.send(f'Checking server status...')
    try:
        mcr = mcrcon.MCRcon(host=rcon_host, port=rcon_port, password=rcon_password)
        mcr.connect()
        mcr.disconnect()
    except ConnectionRefusedError:
        await message.channel.send(f'Thanks for starting the server, {message.author.name}!')
        subprocess.Popen(command)
    
async def clean_response(response):
    cleaned_response = re.sub(r'§[0-9a-fk-orA-FK-OR]', '', response) #use a regex to remove mc colour codes
    return cleaned_response
