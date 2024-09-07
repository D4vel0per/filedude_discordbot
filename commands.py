import re

commands_desc = {
    "!parse": "Returns a requirements-like formatted version of what you passed as a argument",
    "!create": "Creates a text file containing the text from the user input",
    "!cp": "Fusion between !create and !parse: creates a requirements.txt file from user input",
    "!desc": "Prints this message"
}

flags_desc = {
    "--name": "it goes after !create or !cp commands to indicate to the bot the file name"
}

def _desc ():
    help_text = "HERE IS THE DESCRIPTION OF MY COMMANDS! HAVE FUN READING: \n"
    lines = []
    for key in commands_desc:
        line = f"{key} -> {commands_desc[key]}"
        lines.append(line)
    return help_text + "\n".join(lines)

def _parse (text, flag=None):
    lines = [ line.strip() for line in text.splitlines() if line.strip()]
    formatted = ""
    for line in lines[2:]:
        formatted += re.sub("\s+", "==", line) + "\n"

    return formatted

def _create(text, flag=None):
    if flag is None:
        flag = { "name": "--name", "arg": "requirements.txt" }
        filename = "requirements.txt"

    elif flag["name"] == "--name" and flag["arg"]:
        filename = flag["arg"]

    if ".txt" not in filename:
        filename += ".txt"

    if "/" in filename:
        filename = filename[(filename.find("/")+1):]

    with open(f"rep/{filename}", "w") as file:
        file.write(text)
    
    return {
        "filename": "rep/" + filename,
        "text": text
    }
        
def handle_args(text_input):
    start = re.match("![a-z]+( --[a-z]+)?( [a-z\S]+)?", text_input.strip())
    
    results = start.group().split() if start else [None, None, None]
    text_content = text_input[(start.span()[1]+1):].strip() if start else text_input.strip()
    
    return {
        "command": results[0],
        "flag": results[1] if len(results) >= 2 else None,
        "flag_arg": results[2] if len(results) >= 3 else None,
        "text_content": text_content
    }

def _cp(text, flag=None):
    parsed = _parse(text)
    return _create(text=parsed, flag=flag)

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