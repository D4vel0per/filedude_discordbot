import io
import re
from typing import Optional
import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingFlagArgument
import os
from dotenv import load_dotenv
from commands import STORE, commands_desc, flags_desc
from utilities import create_main_channels, get_main_channels, send_yield
from datetime import datetime, timezone
import asyncio

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

    all_channels = [ guild["channel"] for guild in main_channels.values() ]
    all_channels.extend([ch async for ch in new_channels])

    for channel in all_channels:
        await channel.send("I'm online!\nSend a message with the text '!desc' to get a description of the commands available.")

    print(f"LOGGED IN AS {bot.user}")   
    print("CHANNELS:\n")
    [print(f"({ch.guild.name}) {ch.name}") for ch in all_channels]

@bot.event
async def on_disconnect ():
    print("Client disconnected.")
    

class Conditional:
    def __init__(self, cond:bool, prop:str, true, false):
        self.cond = cond
        self.prop = prop
        self.true = true
        self.false = false
    def value(self):
        return self.true if self.cond else self.false

def optionalInfo (flags:dict, default_values:dict, conditional:Conditional):
    final_values = {}
    for k in flags:
        if k in default_values and not flags[k]:
            final_values[k] = default_values[k]
        else:
            final_values[k] = flags[k]

    prop = conditional.prop
    value = conditional.value()
    final_values[prop] = value

    return final_values


class CreationFlags (commands.FlagConverter, prefix="--", delimiter="="):
    name: str = "requirements.txt"
    text: str = ""

dot_txt = lambda string: string + ('' if '.txt' in string else '.txt')
repl_separators = lambda string: re.sub(" +|-+", "_", string)

def ends_at (pattern, string):
    result = re.search(pattern, string)
    if result:
        return result.span()[1] + 1
    else:
        return 0
    
async def send_text_file(ctx, filename, text):
    folder = ""
    if "/" in filename:
        last_index = len(filename) - filename[::-1].find("/") - 1
        folder = filename[:(last_index+1)] + "/"
        filename = filename[(last_index+1):]

    text = text or " "
    bytes_text = text.encode(encoding="utf-8")
    file = io.BytesIO(bytes_text)
    STORE.submit(f"{ctx.author}/{folder}{filename}", text)

    with io.BytesIO(bytes_text) as file:
        await ctx.send(file=discord.File(file, filename))
    
@bot.command()
async def create(ctx, *, input):
    try:
        flags = await CreationFlags.convert(ctx, input)

        default_values = {"text": input[ends_at(flags.name.split()[0], input):],}

        new_flags = optionalInfo(
            {"text": flags.text},
            default_values,
            conditional=Conditional(bool(flags.text), "filename", flags.name, flags.name.split()[0])
        )

        filename = dot_txt(repl_separators(new_flags["filename"]))
        text = new_flags["text"]
        await ctx.send(f"Preparing {filename}... \nTEXT='{text}'")
        await send_text_file(ctx, filename, text)

    except MissingFlagArgument as e:
        print(e) #handle error

@bot.command()
async def desc(ctx):
    help_text = "HERE IS THE DESCRIPTION OF MY COMMANDS! HAVE FUN READING: \n\nCOMMANDS:\n"
    lines = [f"{key} -> {commands_desc[key]}" for key in commands_desc]

    help_text += "\n".join(lines) + "\n\nFLAGS:\n"

    lines = [f"{key} -> {flags_desc[key]}" for key in flags_desc]

    help_text += "\n".join(lines)

    await ctx.send(help_text)

def parse_text(text):
    lines = [ line.strip() for line in text.splitlines() if line.strip()]
    formatted = ""
    for line in lines:
        if (not re.search(r"-{3,}|Version|Package", line)):
            formatted += re.sub("\s+", "==", line) + "\n"
    return formatted

@bot.command() 
async def parse(ctx, *, text):
    if text:
        await ctx.send(parse_text(text))
    else:
        await ctx.send("I can't parse nothingness")

@bot.command()
async def cp(ctx, flag, flag_arg, *, text):
    return
    f_info = get_filename(ctx.author, flag, flag_arg, text)

    if f_info["STATUS"] == "FAILED":
        await ctx.send(f_info["content"])
        return
    
    text = parse_text(text)

    STORE.submit(f_info["content"], text)
    file_data = await get_text_file(f_info["content"], text)
    with file_data["bytes"] as file:
        await ctx.send(file=discord.File(file, file_data["filename"]))

async def check_bot():
    await asyncio.sleep(30)
    while not bot.is_closed():
        now = datetime.now(timezone.utc)
        if now.hour <= 10 and now.hour >= 6:
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

async def main():
    await asyncio.gather(
        bot.start(token),
        #check_bot()
    )
    await asyncio.sleep(605) # The server shuts down 10 minutes after disconnection

if __name__ == "__main__":
    asyncio.run(main())