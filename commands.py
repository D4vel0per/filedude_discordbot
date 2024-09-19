import asyncio
import io
import re
import discord
from github import UnknownObjectException
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
            check_file = await send_text_file(ctx, filename, text)
            print(check_file)

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

    @bot.command()
    async def get(ctx, *, input:str=None):
        try:
            plain_folders = False
            root_folder = str(ctx.author)
            file_name = input
            if input:
                dir_split = [str(ctx.author), *input.split("/")]
                file_name = dir_split.pop().strip()
                if file_name:
                    file_name = file_name.split()[0]
                root_folder = "/".join(dir_split)
                if not file_name:
                    await ctx.send(f"Trying to reach all files in {root_folder}/ folder")
                elif "--folders" in input:
                    plain_folders = True
                    root_folder = re.sub("/+$", "", root_folder)
                    if not file_name.strip().startswith("--"):
                        root_folder += "/" + file_name
                    
                    await ctx.send(f"Getting all your folders at {root_folder}/...")

                elif not re.search(r"\.[a-zA-Z]+$", file_name):
                    file_name += ".txt"
                    await ctx.send(f"Trying to reach {file_name}")
            else:
                await ctx.send(f"Searching all your files at file dude's house...")

            if plain_folders:
                results = STORE.get(root_folder)
                folders = list(filter(lambda result: result.type == "dir", results))
                folders = [ 
                    re.sub(f"^{root_folder}/", "", folder.path) + "/" for folder in folders 
                ]
                if folders:
                    await ctx.send("Your folders are the following:" if folders else "You have no folders here.")
                    await ctx.send("* " + "\n * ".join(folders))
                else:
                    await ctx.send("You have no folders here.")
            
            else:
                results = STORE.get(
                    f"{root_folder}{'/' + file_name if file_name else ''}"
                )

                if len(results) == 0:
                    await ctx.send("Sorry, file not found :C")
                    return 
                
                elif len(results) == 1:
                    result_bytes = io.BytesIO(results[0].decoded_content)
                    await ctx.send(file=discord.File(result_bytes, results[0].name))
                
                else:
                    files_found = list(map(
                        lambda content: content.path.replace(root_folder + "/", "").replace("/", " -> "),
                        filter(
                            lambda content: content.type != "dir",
                            results
                        )
                    ))

                    def key(a):
                        return len(re.findall(" -> ", a))

                    files_found.sort(key=key)

                    folders_found = list(map(
                        lambda content: content.path.replace(root_folder + "/", "") + "/",
                        filter(
                            lambda content: content.type == "dir",
                            results
                        )
                    ))

                    await ctx.send(
                        f"### I found these files in {root_folder}/:\n * " +
                        "\n * ".join(files_found)
                    )
                    if folders_found:
                        await ctx.send(
                            f"### I found these folders in {root_folder}/:\n * " + 
                            "\n * ".join(folders_found)
                        )

        except Exception as e:
            print(type(e))
            print(e)
    @bot.command()
    async def delete(ctx, *, input:str=None):
        try:
            plain_folders = False
            root_folder = str(ctx.author)
            file_name = input
            if input:
                dir_split = [str(ctx.author), *input.split("/")]
                file_name = dir_split.pop().strip().split()[0]
                root_folder = "/".join(dir_split)

                if not file_name:
                    await ctx.send(f"Trying to delete all files in {root_folder}/ folder")
                elif "--folders" in input:
                    plain_folders = True
                    root_folder = re.sub("/+$", "", root_folder)
                    if not file_name.strip().startswith("--"):
                        root_folder += "/" + file_name
                    
                    await ctx.send(f"Deleting all your folders at {root_folder}/...")

                elif not re.search(r"\.[a-zA-Z]+$", file_name):
                    file_name += ".txt"
                    await ctx.send(f"Trying to delete {file_name}...")
            else:
                await ctx.send(f"Deleting all your files at file dude's house...")

            if plain_folders:
                results = STORE.delete(root_folder, only_folders=True)
                folders = list(filter(lambda result: result.type == "dir", results))
                folders = [ 
                    re.sub(f"^{root_folder}/", "", folder.path) + "/" for folder in folders 
                ]
                await ctx.send("The following folders were deleted:" if folders else "No folders deleted.")
                await ctx.send("* " + "\n * ".join(folders))
            
            else:
                results = STORE.delete(
                    f"{root_folder}{'/' + file_name if file_name else ''}"
                )

                if len(results) == 0:
                    await ctx.send("Sorry, file not found :C")
                    return 
                
                elif len(results) == 1:
                    result_bytes = io.BytesIO(results[0].decoded_content)
                    await ctx.send(file=discord.File(result_bytes, results[0].name))
                
                else:
                    files_deleted = list(map(
                        lambda content: content["path"].replace(root_folder + "/", "").replace("/", " -> "),
                        filter(
                            lambda content: not content["is_dir"],
                            results
                        )
                    ))

                    def key(a):
                        return len(re.findall(" -> ", a))

                    files_deleted.sort(key=key)

                    folders_deleted = list(map(
                        lambda content: content["path"].replace(root_folder + "/", "") + "/",
                        filter(
                            lambda content: content["is_dir"],
                            results
                        )
                    ))

                    await ctx.send(
                        f"### These files were deleted at {root_folder}/:\n * " +
                        "\n * ".join(files_deleted)
                    )
                    if folders_deleted:
                        await ctx.send(
                            f"### These folders were deleted in {root_folder}/:\n * " + 
                            "\n * ".join(folders_deleted)
                        )

        except Exception as e:
            print(type(e))
            print(e)

    return bot

def group_list(array:list, size:int):
    result = []
    if size >= len(array):
        return [array]
    
    for i in range(0, len(array), size):
        print(i + size)
        if i + size < len(array):
            result.append(array[i:(i + size)])
        else:
            result.append(array[i:])
    return result