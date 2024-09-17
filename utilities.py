import re
from typing import List
from discord import Client, Guild
from command_helpers import Conditional

is_main_channel = lambda channel, regex=r"(?i)file[\s-]*dude": bool(re.search(regex, channel.name))

def get_main_channels(client: Client, regex:str=r"(?i)file[\s-]*dude"):
    main_channels = {}
    for guild in client.guilds:
        main_channels[guild.name] = {
            "guild_obj": guild
        }
        for channel in guild.text_channels:
            if is_main_channel(channel, regex):
                main_channels[guild.name]["channel"] = channel
            else:
                main_channels[guild.name]["channel"] = None
    return main_channels

async def create_main_channels(guilds: List[Guild]=None):
    if guilds:  
        for guild in guilds:
            channel = await guild.create_text_channel("File Dude - Discord Bot")
            yield channel


async def send_yield(client:Client, message:str):
    main_chs = get_main_channels(client) 
    available_channels = list(filter(lambda guild: guild["channel"], main_chs.values()))
    available_channels = [ ch["channel"] for ch in available_channels ]

    for channel in available_channels:
        await channel.send(message)

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

def dot_txt(string):
    if '.txt' in string:
        return string
    else:
        return string + ".txt"
    
def repl_separators(string):
    return re.sub(" +|-+", "_", string)

def ends_at (pattern, string):
    result = re.search(pattern, string)
    if result:
        return result.span()[1] + 1
    else:
        return 0