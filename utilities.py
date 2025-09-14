import json
import discord
import re
import mcrcon
import subprocess
import sys
import os
import requests

disallow_mentions = discord.AllowedMentions.none()

# function to load configuration data from config.json
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
server_ip = config['server_ip']
server_port = config['server_port']
github_repo = 'nmctl/lostworld-rewritten'
branch = config['branch']
red = config['red'].strip('#')
yellow = config['yellow'].strip('#')
green = config['green'].strip('#')

async def create_embed(title, description, color, footer = None):
    color_int = int(color, 16)
    embed_color = discord.Color(color_int)
    embed = discord.Embed(title=title, description=description, color=embed_color)
    embed.set_footer(text=footer)

    return embed

async def check_updates_command(message):
    try:
        response = requests.get(f"https://api.github.com/repos/{github_repo}/commits/{branch}")
        latest = response.json()["sha"]
        commit_message = response.json()["commit"]["message"]

        remote_version = requests.get(f"https://raw.githubusercontent.com/nmctl/lostworld-rewritten/{branch}/VERSION").text
        remote_update = requests.get(f"https://raw.githubusercontent.com/nmctl/lostworld-rewritten/{branch}/latest.txt").text

        with open('VERSION', 'r') as versionfile:
            local_version = versionfile.read()

        print(f'Remote: {latest}')
        print(f'Commit message: {commit_message}')
        local = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
        print(f'Local: {local}')

        if local != latest:
            embed = await create_embed(title=f"Update {remote_version} Available!", description=f"Branch: {branch}\nCommit hash: {latest}\nCommit message: {commit_message}\nCurrent version: {local_version}\nChanges: {remote_update}", color=green, footer=f"Run `{pf}update` to install the update.")
            await message.channel.send(embed=embed)
        else:
            embed = await create_embed(title="Bot is up to date.", description="No new updates found.", color=green)
            await message.channel.send(embed=embed)
    except Exception as e:
        await message.channel.send(f'Checking for updates failed: {e}')

async def update_command(message):
    await message.channel.send('Checking for updates...')

    try:
        response = requests.get(f"https://api.github.com/repos/{github_repo}/commits/{branch}")
        latest = response.json()["sha"]
        local = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
        commit_message = response.json()["commit"]["message"]
        if local == latest:
            await message.channel.send(f'Bot is up to date (branch: {branch})')
        else:
            await message.channel.send(f"""
Update Available!
Branch: {branch}
Commit hash: {latest}
Commit message {commit_message}
                                       """)
            subprocess.run(['git', 'checkout', branch], check=True)
            result = subprocess.run(["git", "pull"], capture_output=True, text=True)

            await message.channel.send('Installing dependencies...')
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

            await message.channel.send('Installation finished, the bot will now restart')
            os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        await message.channel.send(f'Update failed: {e}')

async def version_command(message):
    commit_message = subprocess.check_output(['git', 'log', '-1', '--pretty=%B']).decode().strip()
    commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
    with open('VERSION', 'r') as versionfile:
        version = versionfile.read()

    with open('latest.txt', 'r') as latestfile:
        latest_update = latestfile.read()

    embed = await create_embed(title='Bot Version Info', description=f"Commit Message: {commit_message}\nCommit Hash: {commit_hash}\nVersion: {version}\nChanges: {latest_update}", color=green)

    await message.channel.send(embed=embed)

async def format_help():
    # Read the contents of the text file
    with open("help.txt", "r") as file:
        content = file.read()

    formatted_content = content.format(pf=pf, rpf=rpf, rrpf=rrpf)

    return formatted_content

# user permission management stuff

async def blacklist_user(message):
    """Add a user to the blacklist"""
    user_id = message.content.split()[1]
    if "@" in user_id:
        user_id = int(user_id[2:-1])
    else:
        user_id = int(user_id)

    if user_id == bot_owner_id:
        await message.channel.send("You cannot blacklist the bot owner.", allowed_mentions=disallow_mentions)
        return

    if user_id in blacklisted_users:
        await message.channel.send(f"<@{user_id}> is already blacklisted.", allowed_mentions=disallow_mentions)
        return

    blacklisted_users.append(user_id)
    with open("blacklisted_users.json", "w") as f:
        json.dump(blacklisted_users, f)
    
    await message.channel.send(f"Added <@{user_id}> to the blacklist.", allowed_mentions=disallow_mentions)


async def unblacklist_user(message):
    """Remove a user from the blacklist"""
    user_id = message.content.split()[1]
    if "@" in user_id:
        user_id = int(user_id[2:-1])
    else:
        user_id = int(user_id)

    if user_id not in blacklisted_users:
        await message.channel.send(f"<@{user_id}> is not in the blacklist.", allowed_mentions=disallow_mentions)
        return

    blacklisted_users.remove(user_id)
    with open("blacklisted_users.json", "w") as f:
        json.dump(blacklisted_users, f)
    
    await message.channel.send(f"Removed <@{user_id}> from the blacklist.", allowed_mentions=disallow_mentions)


async def trust_user(message):
    """Add a user to the trusted users list"""
    user_id = message.content.split()[1]
    if "@" in user_id:
        user_id = int(user_id[2:-1])
    else:
        user_id = int(user_id)

    if user_id == bot_owner_id:
        await message.channel.send("You cannot modify the bot owner.", allowed_mentions=disallow_mentions)
        return

    if user_id in trusted_users:
        await message.channel.send(f"<@{user_id}> is already trusted.", allowed_mentions=disallow_mentions)
        return

    trusted_users.append(user_id)
    with open("trusted_users.json", "w") as f:
        json.dump(trusted_users, f)
    
    await message.channel.send(f"Added <@{user_id}> to trusted users.", allowed_mentions=disallow_mentions)


async def untrust_user(message):
    """Remove a user from the trusted users list"""
    user_id = message.content.split()[1]
    if "@" in user_id:
        user_id = int(user_id[2:-1])
    else:
        user_id = int(user_id)

    if user_id not in trusted_users:
        await message.channel.send(f"<@{user_id}> is not trusted.", allowed_mentions=disallow_mentions)
        return

    trusted_users.remove(user_id)
    with open("trusted_users.json", "w") as f:
        json.dump(trusted_users, f)
    
    await message.channel.send(f"Removed <@{user_id}> from trusted users.", allowed_mentions=disallow_mentions)
    


async def fetch_status(message):
    mcr = mcrcon.MCRcon(host=rcon_host, port=rcon_port, password=rcon_password)
    try:
        mcr.connect()
        mcr.disconnect()
        await message.channel.send('Server status: online')
    except:
        await message.channel.send('Server status: offline')


async def ping(message, client):
    latency = round(client.latency * 1000, 2)
    await message.channel.send(f'Ping: {latency} ms') 

async def help(message):
    help_message = await format_help()
    embed = await create_embed(title=f"{server_name} Bot Commands", description=help_message, color=green, footer=f"Requested by {message.author.name}")
    await message.channel.send(embed=embed)

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
    cleaned_response = re.sub(r'§[0-9a-fk-orA-FK-OR]', '', response) # use a regex to remove mc color codes
    return cleaned_response

async def killswitch(message):
    await message.channel.send('Killing the bot.')
    exit()

async def set_status(message, client):
    parts = message.content.split()
    activity_type = parts[1]
    status_message = ' '.join(message.content[2:])
    
    if activity_type == "play":
        status = discord.Game(status_message)
        await client.change_presence(status=discord.Status.online, activity=status)
    elif activity_type == "listen":
        activity = discord.Activity(type=discord.ActivityType.listening, name=status_message)
    elif activity_type == "watch":
        activity = discord.Activity(type=discord.ActivityType.watching, name=status_message)
