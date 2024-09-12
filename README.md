# File Dude (Discord Bot)
It's just the File Dude, he manages your files if you ask him to do so :D

## Commands
- ### `!parse`
Let's say you need a requirements.txt, just not the file. You need it's content. Here's where `!parse` comes in. Let's say you need to parse this example:
```
    Package            Version
    ------------------ ---------
    aiohappyeyeballs   2.4.0
    aiohttp            3.10.5
    aiosignal          1.3.1
    annotated-types    0.7.0
    attrs              24.2.0
    certifi            2024.8.30
    cffi               1.17.1
    charset-normalizer 3.3.2
    cryptography       43.0.1
    Deprecated         1.2.14
    discord            2.3.2
    discord.py         2.4.0
    frozenlist         1.4.1
```
You can pass this through the bot just like:
```
    !parse Package            Version
    ------------------ ---------
    aiohappyeyeballs   2.4.0
    aiohttp            3.10.5
    aiosignal          1.3.1
    annotated-types    0.7.0
    attrs              24.2.0
    certifi            2024.8.30
    cffi               1.17.1
    charset-normalizer 3.3.2
    cryptography       43.0.1
    Deprecated         1.2.14
    discord            2.3.2
    discord.py         2.4.0
    frozenlist         1.4.1
```

The bot will return something like this:
```
    aiohappyeyeballs==2.4.0
    aiohttp==3.10.5
    aiosignal==1.3.1
    annotated-types==0.7.0
    attrs==24.2.0
    certifi==2024.8.30
    cffi==1.17.1
    charset-normalizer==3.3.2
    cryptography==43.0.1
    Deprecated==1.2.14
    discord==2.3.2
    discord.py==2.4.0
    frozenlist==1.4.1
```

- ### `!create`
Now, what happens when you just wanna create a .txt file? `!create` is the perfect command to do so.

For the clarity of speech, we will work with an example: I want to create a requirements.txt file using the output of `!parse`. The best way to do this would be:

```
    !create aiohappyeyeballs==2.4.0
    aiohttp==3.10.5
    aiosignal==1.3.1
    annotated-types==0.7.0
    attrs==24.2.0
    certifi==2024.8.30
    cffi==1.17.1
    charset-normalizer==3.3.2
    cryptography==43.0.1
    Deprecated==1.2.14
    discord==2.3.2
    discord.py==2.4.0
    frozenlist==1.4.1
```

The bot would return you a file containing your text. The default value for the filename is "requirements.txt".


- ### `!cp`
This command is basically a combination between `!create` and `!parse`:
it messages back a requirements.txt file with unparsed input

Works like this:

```
    !cp Package            Version
    ------------------ ---------
    aiohappyeyeballs   2.4.0
    aiohttp            3.10.5
    aiosignal          1.3.1
    annotated-types    0.7.0
    attrs              24.2.0
    certifi            2024.8.30
    cffi               1.17.1
    charset-normalizer 3.3.2
    cryptography       43.0.1
    Deprecated         1.2.14
    discord            2.3.2
    discord.py         2.4.0
    frozenlist         1.4.1
```

The bot would return you a requirements.txt file containing your text.


- ### `!desc`
If you need to check which commands are available and what does everyone of
them, you can run this command, it will output this message:

> HERE IS THE DESCRIPTION OF MY COMMANDS! HAVE FUN READING: 
>
> COMMANDS:
>
>!parse -> Returns a requirements-like formatted version of what you passed as a argument
>
>!create -> Creates a text file containing the text from the user input
>
>!cp -> Fusion between !create and !parse: creates a requirements.txt file from user input
>
>!desc -> Prints this message
>
>FLAGS:
>
>--name -> it goes after !create or !cp commands to indicate to the bot the file name

## Flags
These are pseudo-arguments that allow to set some info about command execution,
like the file name when creating a file.

- ### `--name`
Works with `!create` and `!cp`.
This is a flag that sets the filename of the file you're creating, you can
use it like this:

```
    !create --name hello.txt Hello, how are you?
```

Where: 

 `hello.txt` -> File name
 
 `Hello, how are you?` -> File text
 
 > _Note: if no name is provided, the file name will
 be set to the first word in the file_
