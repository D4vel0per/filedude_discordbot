from repo_handlers import connect
from command_helpers import (
    Conditional, 
    CreationFlags, 
    send_text_file, 
    parse_text
)
from utilities import (
    dot_txt, 
    ends_at, 
    optionalInfo, 
    repl_separators
)

commands_desc = {
    "!parse": "Returns a requirements-like formatted version of what you passed as a argument",
    "!create": "Creates a text file containing the text from the user input",
    "!cp": "Fusion between !create and !parse: creates a requirements.txt file from user input",
    "!desc": "Prints this message"
}

flags_desc = {
    "--name=": "it goes after !create or !cp commands to indicate to the bot the file name",
    "--text=": "it goes after !create or !cp commands to indicate to the bot the file content"
}

STORE = connect("DEV")

async def set_commands(bot):
    @bot.command()
    async def create(ctx, *, input):
        try:
            flags = await CreationFlags.convert(ctx, input)
            new_flags = optionalInfo(
                {"text": flags.text},
                {"text": input[ends_at(flags.name.split()[0], input):]},
                conditional=Conditional(bool(flags.text), "filename", flags.name, flags.name.split()[0])
            )

            filename = dot_txt(repl_separators(new_flags["filename"]))
            text = new_flags["text"]
            await ctx.send(f"Preparing {filename}...")
            await send_text_file(ctx, filename, text)

        except Exception as e:
            print(type(e))
            print(e) #handle error

    @bot.command()
    async def desc(ctx):
        help_text = "Hi! I'm the File Dude Bot, a list of my commands and flags are down below:\n"
        help_text += "# Commands:\n"
        lines = [f"`{key}`\n> {commands_desc[key]}\n" for key in commands_desc]

        help_text += "* " + "\n* ".join(lines) + "\n# Flags:\n"

        lines = [f"`{key}`\n> {flags_desc[key]}\n" for key in flags_desc]

        help_text += "* " + "\n* ".join(lines)

        await ctx.send(help_text)

    @bot.command() 
    async def parse(ctx, *, text):
        if text:
            await ctx.send(parse_text(text))
        else:
            await ctx.send("I can't parse nothingness")

    @bot.command()
    async def cp(ctx, *, input):
        try:
            flags = await CreationFlags.convert(ctx, input)
            new_flags = optionalInfo(
                {"text": flags.text},
                {"text": input[ends_at(flags.name.split()[0], input):]},
                conditional=Conditional(bool(flags.text), "filename", flags.name, flags.name.split()[0])
            )

            filename = dot_txt(repl_separators(new_flags["filename"]))
            text = new_flags["text"]
            await ctx.send(f"Preparing {filename}...")
            await send_text_file(ctx, filename, parse_text(text))

        except Exception as e:
            print(type(e))
            print(e) #handle error

    return bot