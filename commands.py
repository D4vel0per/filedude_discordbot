import base64
import io
import re
import discord
from discord.ext.commands import Bot, command
from repo_handlers import connect
from command_helpers import (
    Conditional, 
    CreationFlags,
    ReadFlags, 
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
    "!get": "Returns the file specified by the user, using it's path. Add '/' at the end if it's a folder",
    "!delete": "Deletes the file specified by the user, using it's path. Add '/' at the end if it's a folder",
    "!desc": "Prints this message"
}

flags_desc = {
    "--name=": "it goes after !create or !cp commands to indicate to the bot the file name",
    "--text=": "it goes after !create or !cp commands to indicate to the bot the file content",
    "--folders": "it goes after the path entered by the user to only look for the folders in that path"
}

STORE = connect("DEV")

@command()
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
        check_file = await send_text_file(ctx, filename, text)
        print(check_file)

    except Exception as e:
        print(type(e))
        print(e) #handle error

@command()
async def desc(ctx):
    help_text = "Hi! I'm the File Dude Bot, a list of my commands and flags are down below:\n"
    help_text += "# Commands:\n"
    lines = [f"`{key}`\n> {commands_desc[key]}\n" for key in commands_desc]

    help_text += "* " + "\n* ".join(lines) + "\n# Flags:\n"

    lines = [f"`{key}`\n> {flags_desc[key]}\n" for key in flags_desc]

    help_text += "* " + "\n* ".join(lines)

    await ctx.send(help_text)

@command()
async def parse(ctx, *, text):
    if text:
        await ctx.send(parse_text(text))
    else:
        await ctx.send("I can't parse nothingness")

@command()
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

@command()
async def get(ctx, *, input:str=""):
    try:
        flags = await ReadFlags.convert(ctx, input)
        dir_info = get_dir_info(
            str(ctx.author),
            re.sub(" *--folders", "/", flags.folders) if flags.folders else input
        )
        root_folder = dir_info["folder"]
        file_name = dir_info["filename"]
        if input:
            if file_name:
                await ctx.send(f"Trying to reach {file_name}")
            elif flags.folders:
                await ctx.send(f"Getting all your folders at {root_folder}/...")
            else:
                await ctx.send(f"Trying to reach all files in {root_folder}/ folder")
        else:
            await ctx.send(f"Searching all your files at file dude's house...")

        results = STORE.get(
            f"{root_folder}/{file_name if file_name else ''}"
        )

        if not results:
            await ctx.send(f"Sorry, {'file' if file_name else 'folder'} not found :C")
                
        elif len(results) == 1:
            result_bytes = base64.b64decode(results["files"][0]["text_64"])
            await ctx.send(file=discord.File(result_bytes, results[0].name))
                
        else:
            files_found = [ path_prettify(root_folder, file["filename"], False) for file in results["files"] ]
            folders_found = [ path_prettify(root_folder, folder, False) for folder in results["folders"] ]

            message1 = (f"### I found these files in {root_folder}/:\n * " +
            "\n * ".join(files_found)) if files_found else "### No files found."
                
            message2 = (f"### I found these folders in {root_folder}/:\n * " +
            "\n * ".join(folders_found)) if folders_found else "### No folders found."

            if not flags.folders:   
                await ctx.send(message1)

            await ctx.send(message2)

    except Exception as e:
        print(type(e))
        print(e)

@command()
async def delete(ctx, *, input:str=""):
    try:
        flags = await ReadFlags.convert(ctx, input)
        dir_info = get_dir_info(
            str(ctx.author),
            re.sub(" *--folders", "/", flags.folders) if flags.folders else input
        )
        root_folder =  dir_info["folder"]
        file_name = dir_info["filename"]
        if input:
            if file_name:
                await ctx.send(f"Trying to delete {file_name}...")
            elif flags.folders:
                await ctx.send(f"Deleting all your folders at {root_folder}/...")
            else:
                await ctx.send(f"Trying to delete all files in {root_folder}/ folder")
        else:
            await ctx.send(f"Deleting all your files at file dude's house...")
            
        results = STORE.delete(
            f"{root_folder}{'/' + file_name if file_name else ''}",
            only_folders=bool(flags.folders)
        )
        if not results:
            await ctx.send(f"Sorry, {'file' if file_name else 'folder'} not found :C")
        else:
            files_deleted = [ path_prettify(root_folder, file["filename"], False) for file in results["files"] ]
            folders_deleted = [ path_prettify(root_folder, folder, False) for folder in results["folders"] ]
                
            message1 = (f"### These files were deleted at {root_folder}/:\n * " +
            "\n * ".join(files_deleted)) if files_deleted else "### No files deleted."
                
            message2 = (f"### These folders were deleted in {root_folder}/:\n * " +
            "\n * ".join(folders_deleted)) if folders_deleted else "### No folders deleted."
                
            await ctx.send(message1)
            await ctx.send(message2)

    except Exception as e:
        print(type(e))
        print(e)

async def set_commands(bot: Bot):
    bot.add_command(create)
    bot.add_command(parse)
    bot.add_command(cp)
    bot.add_command(desc)
    bot.add_command(get)
    bot.add_command(delete)

    return bot

def get_dir_info(root, path:str):
    path = f"{root}/{path}"
    is_folder = path.strip().endswith("/")
    if is_folder:
        folder = re.sub("/+$", "", path)
        filename = ""
    else:
        comps = [x for x in path.split("/") if x ]
        filename = dot_txt(comps.pop().split()[0])
        folder = "/".join(comps)

    return { "folder": folder, "filename": filename }

def path_prettify (root_folder:str, path: str, is_folder=False):
    no_root = re.sub(f"{root_folder}/", "", path)
    return no_root + "/" if is_folder else no_root.replace("/", " -> ")