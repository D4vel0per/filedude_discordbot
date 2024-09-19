import io
import re
import discord
from discord.ext import commands
from repo_handlers import connect

STORE = connect()

class Conditional:
    def __init__(self, cond:bool, prop:str, true, false):
        self.cond = cond
        self.prop = prop
        self.true = true
        self.false = false
    def value(self):
        return self.true if self.cond else self.false
    
class CreationFlags (commands.FlagConverter, prefix="--", delimiter="="):
    name: str = "requirements.txt"
    text: str = ""

class ReadFlags (commands.FlagConverter, prefix="--", delimiter=" "):
    folders: str = commands.flag(positional=True, default=None)

async def send_text_file(ctx, filename, text):
    folder = ""
    if "/" in filename:
        last_index = len(filename) - filename[::-1].find("/") - 1
        folder = filename[:(last_index+1)]
        filename = filename[(last_index+1):]

    text = text or " "
    bytes_text = text.encode(encoding="utf-8")
    file = io.BytesIO(bytes_text)

    STORE.submit(f"{ctx.author}/{folder}{filename}", text)

    with io.BytesIO(bytes_text) as file:
        await ctx.send(file=discord.File(file, filename))

def parse_text(text):
    lines = [ line.strip() for line in text.splitlines() if line.strip()]
    formatted = ""
    for line in lines:
        if (not re.search(r"-{3,}|Version|Package", line)):
            formatted += re.sub("\s+", "==", line) + "\n"
    return formatted