# SJBot
SJBot is a Discord Bot that makes the link between a guild and the FFBad database.
It relies on a set of commands that make it possible to get information about a player from his/her licence number, or list the best player of the SJB Team.

It uses the discord python sdk: https://github.com/Rapptz/discord.py


## Requirements
SJBot requires python 3.6+

## Installation
Install all the required packages by running :

```
pip install -r requirements.txt
```
You will have to set the required env variables:
- BOT_TOKEN: you will get one from the discord developper page
- STRAVA_CHANNEL: allow to post a club activity in a given channel

To make strava api works, you will have to set a credentials file containing a json conf:
```
.secret/strava_credentials.json

{
	"client_id": "",
	"client_secret": "",
	"access_token": "",
	"refresh_token": ""
}
```

## Launch
To launch the bot, just run the main script:
```
python sjbot_main.py
```

## Usage
The bot has two commands:
- $info "licence_number": displays all the available information about the player
- $top "discipline": displays the SJB top 20 players in the selected discipline ("sh", "sd", "dd", "dh", "dm") 

