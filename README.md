## OverTown Bot ##
Discord Bot for the Overwatch FR server, developed in Python using DiscordPy

### Features ###
* Most features are personalized for OverTown discord (static variables and such)

### Commands ###
* See embed_help function of !help command in discord

### Requirements ###
* mysql-connector-python
* apscheduler
* httplib2
* google-api-python-client
* pyshorteners
* simplejson
* discord.py


### Installation ###
* Clone git
* Copy config.json.example to config.json
* Edit config.json to fit your configuration. It will update on its own afterwards.
* execute 'python main.py'

If needed the prompt can be modified via the config.json file after the first start. 
It is `:` by default.

https://discordapp.com/oauth2/authorize?client_id=292685943566237698&scope=bot&permissions=3072

https://hackaday.com/2018/02/15/creating-a-discord-webhook-in-python/