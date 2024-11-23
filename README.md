# Lost World SMP Discord Bot  

This is a discord bot that gives minecraft server admins full control over their server through discord.  
It has features like starting the server from discord, some integration with DiscordSRV, the ability to run minecraft commands on discord through rcon, moderation commands, and other fun commands.  

## How to use the bot  
To use this discord bot, you will first have to create one at https://discord.com/developers/applications  
Once you have created the bot, you must copy the token from the website and download the code from here.  
Once downloaded, you must create your config file. There is an included config generator, but it is not finished so it is recommended to write the config manually.  
Current config options include:  
prefix (the prefix to run commands with, usually something like ! or $)  
token (the bot token, copied from the website earlier)  
logging_channel_id (a channel for the bot to send logs to)  
rcon_host (the server ip to connect to with rcon, defined in server.properties)  
rcon_port (the port the bot will use to connect to with rcon, defined in server.properties)  
rcon_password (rcon password, defined in server.properties)  
bot_owner_id (your discord user id, requires developer mode to be enabled)  
rcon_prefix (the prefix to use to run minecraft commands from discord, returning a cleaned response that uses a regex to clear colour codes)  
raw_rcon_perfix (the prefix to use to run minecraft commands from discord, returning the raw output of the command)  
server_name (the name of your server)  
server_start_command (the command you use to start the server)  
server_ip (your server's ip address)  
server_port (your server's port)  
guild_id (your discord server's id, requires developer mode to be enabled in discord settings)  
  
Once you are done configuring the bot, you can install the dependencies with this command:  
`pip install discord mcrcon`  
Or if you are on linux, create a virtual environment:  
`python3 -m venv botenv`  
`source botenv/bin/activate`  
`pip install discord mcrcon`  
Once this is done, start the bot with this command:  
`python3 main.py` or `python main.py`  

## Where to get help  
Discord server: https://discord.gg/VjaNJH6M7N  
My discord username: @nmcli  
