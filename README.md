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

- ### `!get`
This command retrieves a file or a folder contents:
It messages back a downloadable file from the path given by the user.
You can also send a folder's path (it must end with '/') to get a list of it's files

Works like this:

- Getting all your files:
```
    !get
```

- Getting a single file:
```
    !get my_filename.txt
```

- Getting a single file inside a folder/folders:
```
    !get folder/folder_inside_folder/(folders...)/file.txt
```

- Getting all your files inside a folder:
```
    !get folder/
```

- ### `!delete`
This command deletes a file or a folder contents:
It messages back a list of the files and/or folders deleted from the path given by the user.
You can also send a folder's path (it must end with '/') to delete it's files

Works like this:

- Deleting all your files:
```
    !delete
```

- Deleting a single file:
```
    !delete my_filename.txt
```

- Deleting a single file inside a folder/folders:
```
    !delete folder/folder_inside_folder/(folders...)/file.txt
```

- Deleting all your files inside a folder:
```
    !delete folder/
```

- ### `!desc`
If you need to check which commands are available and what does everyone of
them, you can run this command, it will output a help message.

## Flags
These are pseudo-arguments that allow to set some info about command execution,
like the file name when creating a file.

- ### `--name`
Works with `!create` and `!cp`.
This is a flag that sets the filename of the file you're creating, you can
use it like this:

```
    !create --name=hello.txt Hello, how are you?
```

Where: 

 `hello.txt` -> File name
 
 `Hello, how are you?` -> File text content
 
 > _Note: if no name is provided, the file name will
 be set to_ `requirements.txt`

- ### `--text`
Works with `!create` and `!cp`.
This is a flag that sets the text content of the file you're creating, you can
use it like this:

```
    !create --text= package==version
```

Where: 

 File name -> `requirements.txt` (no name provided, default is `requirements.txt`)
 
 `package==version` -> File text content
 
 The ideal way to work with this flag, is using both `--name` and `--text`, just like:
 
```
    !create --name=filedude.txt --text= I AM THE FILE DUDE
```

Where: 

`filedude.txt` -> File name
 
`I AM THE FILE DUDE` -> File text content
 
> _Note: if no text is provided, the file text content will
be set to_ " "

- ### `--folders`
Works with `!get` and `!delete`.
This is a positional flag (it takes no values) that allows you to only apply the command to the folders.
Works like this:

- Without path:
```
    (!get or !delete) --folders # gets/deletes all your folders
```
It gets or deletes all your folders

- With a path:
```
    (!get or !delete) personal_stuff/passwords/ --folders 
```
In this case, it gets or deletes this path folders
