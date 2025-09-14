import discord
import importlib
import tomllib
import json
import mcrcon
import utilities
from utilities import blacklisted_users
import fun
import moderation

# load config
config = utilities.load_config()
prefix = config['prefix']
token = config['token']
bot_owner_id = int(config['bot_owner_id'])
logging_channel_id = config['logging_channel_id']
rcon_prefix = config['rcon_prefix']
raw_rcon_prefix = config['raw_rcon_prefix']
guild_id = config['guild_id']
server_name = config['server_name']
red = config['red'].strip('#')
yellow = config['yellow'].strip('#')
green = config['green'].strip('#')

rcon_host = config['rcon_host']
rcon_port = int(config['rcon_port'])
rcon_password = config['rcon_password']
server_start_command = config['server_start_command']

# load command registry and permission configuration
with open("commands.toml", "rb") as f:
    commands_registry = tomllib.load(f)

with open("roles.toml", "rb") as f:
    roles_config = tomllib.load(f)
role_map = roles_config.get("roles", {})

# set up intents and the client
intents = discord.Intents.all()
client = discord.Client(intents=intents)

deleted_embeds = {}

# helper functions
def get_user_permissions(member: discord.Member):
    perms = set(["everyone"])
    for role in member.roles:
        if role.name in role_map:
            perms.add(role_map[role.name])
    return perms

async def run_command(cmd_name, message):
    if cmd_name not in commands_registry:
        return

    command_info = commands_registry[cmd_name]
    required_perms = set(command_info.get("permissions", []))
    user_perms = get_user_permissions(message.author)
    
    if required_perms.isdisjoint(user_perms) and message.author.id != bot_owner_id:
        embed = await utilities.create_embed(title="Permission denied", description="You don't have permission to use this command.", color=red, footer=f"Requested by {message.author.name}")
        await message.channel.send(embed=embed)
        return

    # import module and function
    module_name, func_name = command_info["function"].rsplit(".", 1)
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)

    # prepare extra args
    extra_args = []
    for arg in command_info.get("extra_args", []):
        if arg == "client":
            extra_args.append(client)
        elif arg == "deleted_embeds":
            extra_args.append(deleted_embeds)
        elif arg == "command":
            extra_args.append(server_start_command)
        elif arg == "target":
            extra_args.append(message.mentions[0] if message.mentions else None)

    await func(message, *extra_args)

# events
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("with the Discord API"))
    latency = round(client.latency * 1000, 2)
    logging_channel = await client.fetch_channel(logging_channel_id)
    await logging_channel.send(f'Lost World Bot starting for {server_name}. Ping: {latency} ms')

@client.event
async def on_message_delete(message):
    embed = discord.Embed(title="Message Deleted", color=discord.Color.red())
    embed.add_field(name="Author", value=message.author.name)
    embed.add_field(name="Message", value=message.content)
    embed.add_field(name="Channel", value=message.channel.name)
    deleted_embeds[message.channel.id] = embed

@client.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content

    # rcon commands (bot owner only)
    if message.author.id == bot_owner_id:
        if content.startswith(rcon_prefix):
            mcr = mcrcon.MCRcon(port=rcon_port, host=rcon_host, password=rcon_password)
            mcr.connect()
            command = content[len(rcon_prefix):]
            response = await utilities.clean_response(mcr.command(command))
            await message.channel.send(response)
            mcr.disconnect()
            return
        elif content.startswith(raw_rcon_prefix):
            mcr = mcrcon.MCRcon(port=rcon_port, host=rcon_host, password=rcon_password)
            mcr.connect()
            command = content[len(raw_rcon_prefix):]
            response = mcr.command(command)
            await message.channel.send(response)
            mcr.disconnect()
            return

    # user blacklist checker
    if message.author.id in blacklisted_users and message.author.id != bot_owner_id:
        if content.startswith(prefix):
            embed = await utilities.create_embed(title="Permission denied", description="You are blacklisted from using the bot.", color=red, footer=f"Requested by {message.author.name}")
            await message.channel.send(embed=embed)
            return

    # run commands
    if content.startswith(prefix):
        cmd_name = content[len(prefix):].split()[0]
        await run_command(cmd_name, message)

client.run(token)
