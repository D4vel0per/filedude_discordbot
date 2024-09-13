import io
import discord
from commands import handle_args, get_command
from utilities import create_main_channels, get_main_channels, send_yield
from datetime import datetime, timezone
import asyncio

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
token = ""

with open("BOT-env.txt", "r") as reader:
    token = reader.read()

@client.event
async def on_ready ():
    main_channels = get_main_channels(client)
    without_main = [ 
        main_channels[g]["guild_obj"] for g in main_channels if not main_channels[g]["channel"]
    ]
    new_channels = create_main_channels(without_main)

    all_channels = [ guild["channel"] for guild in main_channels.values() ]
    all_channels.extend([ch async for ch in new_channels])

    for channel in all_channels:
        await channel.send("I'm online!\nSend a message with the text '!desc' to get a description of the commands available.")

    print(f"LOGGED IN AS {client.user}")   
    print("CHANNELS:\n")
    [print(f"({ch.guild.name}) {ch.name}") for ch in all_channels]

@client.event
async def on_disconnect ():
    print("Client disconnected.")
    
@client.event
async def on_message (message):
    if message.author != client.user and message.content.startswith("!"):
        args = handle_args(message.content)
        command, flags = get_command(args["command"])
        flag = args["flag"] if args["flag"] in flags else None
        flag_arg = args["flag_arg"] if flag else None

        if command and (args["command"] == "!create" or args["command"] == "!cp"):
            flag = flag or "--name"
            flag_arg = f"{str(message.author)}/{flag_arg or 'requirements.txt'}"

        if command:
            command_result = command(
                flag={ "name": flag, "arg": flag_arg } if flag else None,
                text=args["text_content"]
            )
            if command_result.mode == "!create" or command_result.mode == "!cp":
                bytes_text = command_result.content["text"].encode(encoding="utf-8")
                with io.BytesIO(bytes_text) as file:
                    await message.channel.send(
                        file=discord.File(file, command_result.content["filename"]))
            else:
                await message.channel.send(command_result.content["text"])

async def check_bot():
    await asyncio.sleep(30)
    while True:
        now = datetime.now(timezone.utc)
        if now.hour >= 20 or now.hour <= 6:
            print("Closing...")
            utc_formatted = now.strftime("%H:%M%p").replace("AM", "a.m.").replace("PM", "p.m.")
            link = "\nYou can search what will be your time at "
            link += "https://dateful.com/convert/utc?t=" + utc_formatted
            await send_yield(
                client=client, 
                message=f"I'm leaving for now!\nI'll be back at UTC {utc_formatted + link}"
            )

            await client.close()
            print("Succesfully closed.")
            break
        
        await asyncio.sleep(15*60)

async def main():
    await asyncio.gather(
        client.start(token),
        check_bot()
    )
        

if __name__ == "__main__":
    asyncio.run(main())
    