import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
import asyncio
from commands import set_commands

from utilities import (
    create_main_channels, 
    get_main_channels, 
    send_yield
)

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
token = os.getenv("BOT_DEV_TOKEN")

@bot.event
async def on_ready ():
    main_channels = get_main_channels(bot)
    without_main = [ 
        main_channels[g]["guild_obj"] for g in main_channels if not main_channels[g]["channel"]
    ]
    new_channels = create_main_channels(without_main)

    all_channels = [ guild["channel"] for guild in main_channels.values() if guild["channel"]]
    all_channels.extend([ch async for ch in new_channels])

    for channel in all_channels:
        await channel.send("I'm online!\nSend a message with the text '!desc' to get a description of the commands available.")

    print(f"LOGGED IN AS {bot.user}")   
    print("CHANNELS:\n")
    [print(f"({ch.guild.name}) {ch.name}") for ch in all_channels]

@bot.event
async def on_disconnect ():
    print("Client disconnected.")


async def check_bot():
    await asyncio.sleep(30)
    while not bot.is_closed():
        now = datetime.now(timezone.utc)
        if now.hour < 10 and now.hour >= 6:
            print("Closing...")
            link = "\nYou can check what will be your time [here]"
            link += "(https://dateful.com/convert/utc?t=10a.m.)"
            await send_yield(
                client=bot, 
                message=f"I'm leaving for now! I'll be back at UTC 10:00a.m. {link}"
            )

            await bot.close()
            print("Succesfully closed.")
            break
        
        await asyncio.sleep(15*60)

async def main(bot):
    bot = await set_commands(bot)
    await asyncio.gather(
        bot.start(token),
        #check_bot()
    )
    await asyncio.sleep(605) # The server shuts down 10 minutes after disconnection

if __name__ == "__main__":
    asyncio.run(main(bot))