import re
from models import CommandResponse
from repo_handlers import connect

commands_desc = {
    "!parse": "Returns a requirements-like formatted version of what you passed as a argument",
    "!create": "Creates a text file containing the text from the user input",
    "!cp": "Fusion between !create and !parse: creates a requirements.txt file from user input",
    "!desc": "Prints this message"
}

flags_desc = {
    "--name": "it goes after !create or !cp commands to indicate to the bot the file name"
}

STORE = connect()

def _desc (text=None, flag=None):
    help_text = "HERE IS THE DESCRIPTION OF MY COMMANDS! HAVE FUN READING: \n\nCOMMANDS:\n"
    lines = [f"{key} -> {commands_desc[key]}" for key in commands_desc]

    help_text += "\n".join(lines) + "\n\nFLAGS:\n"

    lines = [f"{key} -> {flags_desc[key]}" for key in flags_desc]

    content = {"text": help_text + "\n".join(lines)}
    resp = CommandResponse(mode="!desc", status="SUCCESS", content=content)
    return resp
    

def _parse (text, flag=None):
    lines = [ line.strip() for line in text.splitlines() if line.strip()]
    formatted = ""
    for line in lines:
        if (not re.search(r"-{3,}|Version|Package", line)):
            print(line)
            formatted += re.sub("\s+", "==", line) + "\n"
    
    content = {"text": formatted}
    resp = CommandResponse(mode="!parse", status="SUCCESS", content=content)
    return resp

def _create(text, flag=None):
    if flag is None:
        flag = { "name": "--name", "arg": "requirements.txt" }
        filename = "unknown/requirements.txt"

    elif flag["name"] == "--name" and flag["arg"]:
        filename = flag["arg"]

    if ".txt" not in filename:
        filename += ".txt"

    if "/" in filename:
        last_index = len(filename) - filename[::-1].find("/") - 1
        folder = filename[:(last_index+1)]
        filename = filename[(last_index+1):]

    STORE.submit(folder + filename, text)

    content = {
        "filename": filename,
        "dir": folder,
        "text": text
    }
    
    return CommandResponse(mode="!create", status="SUCCESS", content=content, flag=flag["name"])
        
def handle_args(text_input):
    start = re.match("![a-z]+( --[a-z]+ [a-z\S]+)?", text_input.strip())
    
    results = start.group().split() if start else [None, None, None]
    text_content = text_input[(start.span()[1]+1):].strip() if start else text_input.strip()
    
    return {
        "command": results[0],
        "flag": results[1] if len(results) >= 2 else None,
        "flag_arg": results[2] if len(results) >= 3 else None,
        "text_content": text_content
    }

def _cp(text, flag=None):
    parsed = _parse(text).content["text"]
    resp = _create(text=parsed, flag=flag)
    return CommandResponse(mode="!cp", status="SUCCESS", content=resp.content, flag=resp.flag)

def get_command (command_name):
    commands = {
        "!parse": _parse,
        "!create": _create,
        "!cp": _cp,
        "!desc": _desc
    }
    flags = {
        "!parse": [],
        "!create": ["--name"],
        "!cp": ["--name"],
        "!desc": []
    }
    if command_name in commands:
        return [commands[command_name], flags[command_name]]
    else:
        return [None, None]