import asyncio
import discord

async def snipe(message, deleted_embeds):
    if message.channel.id in deleted_embeds:
        await message.channel.send(embed=deleted_embeds[message.channel.id])
    else:
        await message.channel.send("There's nothing to snipe!")

async def annoy(message, target):
    spam_message = message.content.split(' ', 2)[2]
    for i in range(50):
        try:
            await target.send(spam_message)
        except discord.RateLimited:
            await asyncio.sleep(2)
            await target.send(spam_message)
