# Lost World SMP Discord Bot

Get (almost) full remote control over your minecraft server with this discord bot.  

## Setup Guide
  1. Create a discord bot  
     Go to https://discord.com/developers/applications  
     Create an application  
     Copy the token for later  
  2. Download the code  
     Download the code, or clone the repository: `git clone http://github.com/nmctl/lostworld-rewritten.git/`  
  3. Create your config file  
     Here's an example of a `config.json` file:

```json
{
  "prefix": "!",  // Command prefix for the bot (e.g., ! or $)
  "token": "YOUR_BOT_TOKEN",  // Your bot token from the Discord Developer Portal
  "logging_channel_id": "123456789012345678",  // Discord channel ID for bot logs
  "rcon_host": "server_ip_here",  // IP address of your Minecraft server
  "rcon_port": 25575,  // Port defined in your server.properties
  "rcon_password": "your_rcon_password",  // RCON password from server.properties
  "bot_owner_id": "123456789012345678",  // Your Discord user ID
  "rcon_prefix": "!mc",  // Prefix for RCON commands (customizable)
  "raw_rcon_prefix": "!raw",  // Prefix for raw RCON output (customizable)
  "server_name": "My Minecraft Server",  // A friendly name for your server
  "server_start_command": "./start_server.sh",  // Command to start your server
  "server_ip": "your.server.ip",  // IP address for server display
  "server_port": 25565,  // Port for players to connect to your server
  "guild_id": "123456789012345678",  // Your Discord server (guild) ID
  "discord_invite": "https://discord.gg/lostworld", // Your discord server invite
  "branch": "master" // The branch you want to use (master for the stable version, dev for new features)
}
```
  4. Install dependencies  
     For windows: `pip install discord mcrcon`  
     For linux (with a venv):  
     `python3 -m venv botenv`  
     `source botenv/bin/activate`  
     `pip install -r requirements.txt`  
  5. Finally, start the bot  
     `python main.py` OR `python3 main.py`
     
## Features  
- Start/stop your server from discord  
- Ban players from discord  
- Run any command from discord  
- Blacklisting system (ban people from using bot commands)  
- Trusting system (give people extra permissions)
- Moderation features
- Update command

## Coming soon  
- Plugin management  
- A custom plugin to link minecraft and discord accounts (like discordsrv)
- Discord server welcome message
- Detect people asking for the server ip

## Coming eventually (maybe)  
- A plugin database with download links and file names for each plugin (to help with plugin management)  

## Updating  
To update the bot, simply run the update command. To check for updates, run the checkupdates command.

## Need Help?
- Join our discord server: https://discord.gg/lostworld
- Or dm me on discord: @nmcli
