import discord
import json
import utilities
import fun
import mcrcon
global deleted_embed
import importlib
import moderation

# stuff
deleted_embeds = {}
blacklisted_file = open('blacklisted_users.json')
blacklisted_file_path = 'blacklisted_users.json'
trusted_file = open('trusted_users.json')
trusted_file_path = 'trusted_users.json'
blacklisted_users = json.load(blacklisted_file)
trusted_users = json.load(trusted_file)

# load config data and values
config = utilities.load_config()
prefix = config['prefix']
token = config['token']
logging_channel = config['logging_channel_id']
bot_owner_id = int(config['bot_owner_id'])
rcon_prefix = config['rcon_prefix']
raw_rcon_prefix = config['raw_rcon_prefix']
guild_id = config['guild_id']
pf = prefix
rpf = rcon_prefix
rrpf = raw_rcon_prefix

# rcon stuff
rcon_host = config['rcon_host']
rcon_port = int(config['rcon_port'])
rcon_password = config['rcon_password']
server_start_command = config['server_start_command']

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# stuff to do at startup
@client.event
async def on_ready():
    print(f'Now logged in as {client.user}')
    game = discord.Game("with the discord API")
    await client.change_presence(status=discord.Status.online, activity=game)
    latency = round(client.latency * 1000, 2)
    print(f'Ping: {latency} ms')
    print(blacklisted_users)



# bot event for commands
@client.event
async def on_message(message):
    content = message.content
    try:

        if content.startswith(rpf) and message.author.id == bot_owner_id:
            mcr = mcrcon.MCRcon(port=rcon_port, host=rcon_host, password=rcon_password)
            mcr.connect()
            command = message.content[1:]
            response = await utilities.clean_response(mcr.command(command))
            print(f"Server Response: {response}")
            await message.channel.send(response)
            mcr.disconnect()
           
        elif content.startswith(rrpf) and message.author.id == bot_owner_id:
            mcr = mcrcon.MCRcon(port=rcon_port, host=rcon_host, password=rcon_password)
            mcr.connect()
            command = message.content[1:]
            response = mcr.command(command)
            print(f"Server Respose: {response}")
            await message.channel.send(response)
            mcr.disconnect()

        elif content.startswith(prefix) and message.author.id in blacklisted_users and not message.author.id == bot_owner_id:
            await message.channel.send('You are blacklisted.')
            return

        elif content.startswith(prefix) and not message.author.id in blacklisted_users:
            
            if content.startswith(f'{pf}snipe'):
                await fun.snipe(message, deleted_embeds)

            elif content.startswith(f"{pf}ping"):
                await utilities.ping(message, client)

            elif content.startswith(f"{pf}annoy"):
                target = message.mentions[0]
                await fun.annoy(message, target)

            elif content.startswith(f"{pf}help"):
                await utilities.help(message)

            elif content.startswith(f"{pf}reload") and message.author.id == bot_owner_id:
                await message.channel.send('Reloading...')
                importlib.reload(utilities)
                importlib.reload(fun)
                await message.channel.send('Reload complete.')

            elif content.startswith(f"{pf}startserver"):
                await utilities.startserver(message, command=server_start_command)

            elif content.startswith(f"{pf}blacklist") and (message.author.id in trusted_users or message.author.id == bot_owner_id):
                user = content.split()[1]
                if not "@" in user:
                    user = int(user)
                else:
                    user = int(user[2:-1])
                if user == bot_owner_id: await message.channel.send("You cannot blacklist the bot owner.")
                else: await utilities.add_user(message=message, content=content, user_list=blacklisted_users, file=blacklisted_file_path, list_name="blacklisted users")
    # await utilities.save_blacklisted_users(blacklisted)

            elif content.startswith(f"{pf}unblacklist") and (message.author.id in trusted_users or message.author.id == bot_owner_id):
                await utilities.remove_user(message=message, content=content, user_list=blacklisted_users, file=blacklisted_file_path, list_name="blacklisted users")
    # await utilities.save_blacklisted_users()

            elif content.startswith(f"{pf}trust") and message.author.id == bot_owner_id:
                await utilities.add_user(message=message, content=content, file=trusted_file_path, user_list=trusted_users, list_name="trusted users")

            elif content.startswith(f"{pf}untrust") and message.author.id == bot_owner_id:
                await utilities.remove_user(message=message, content=content, file=trusted_file_path, user_list=trusted_users, list_name="trusted users")

            elif content.startswith(f"{pf}status"):
                await utilities.fetch_status(message=message)

            elif content.startswith(f"{pf}ban"):
                await moderation.ban(message=message)

            elif content.startswith(f"{pf}unban"):
                await moderation.unban(message=message)

            elif content.startswith(f"{pf}addrole"):
                await moderation.add_role(message=message)

            elif content.startswith(f"{pf}delrole"):
                await moderation.remove_role(message=message)

            



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
