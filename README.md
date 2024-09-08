# filedude_discordbot
It's just the File Dude, he manages your files if you ask him to do so :D

## requirements.txt
Now you can ask him make a requirements.txt file, you just need to give him the
output given by "pip list" on your command line

### Usage:
Run the following command on your favorite terminal:
  pip list 

If everything goes well, you'll see something like this in the console:

  Package          Version
  ---------------- -------
  aiohappyeyeballs 2.4.0
  aiohttp          3.10.5 
  aiosignal        1.3.1
  attrs            24.2.0 
  discord          2.3.2
  discord.py       2.4.0
  frozenlist       1.4.1
  idna             3.8
  markdown-it-py   3.0.0
  mdurl            0.1.2
  multidict        6.0.5
  pip              24.2
  Pygments         2.18.0
  rich             13.8.0
  setuptools       65.5.0
  yarl             1.10.0

You'll need to copy this text for later usage. Now, you can ask to the File Dude to create the requirements.txt file,
just typing this into a channel that he is part of:
  !create <your pip list results>

If there are no errors, the bot will message back a file called "requirements.txt", containing the text you need.
