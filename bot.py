import io
import discord
from commands import handle_args, get_command

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
token = ""

with open("BOT-env.txt", "r") as reader:
    token = reader.read()

@client.event
async def on_ready ():
    print(f"LOGGED IN AS {client.user}")   

@client.event
async def on_message (message):
    if message.author != client.user and message.content.startswith("!"):
        args = handle_args(message.content)
        command, flags = get_command(args["command"])
        flag = args["flag"] if args["flag"] in flags else None
        flag_arg = args["flag_arg"] if flag else None

        if command and (args["command"] == "!create" or args["command"] == "!cp"):
            flag_arg = f"{str(message.author)}/{flag_arg}" if flag_arg else f"{str(message.author)}/requirements.txt"

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

client.run(token)