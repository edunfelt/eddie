# Discord bot: Eddie the computer
A discord bot to help manage programming courses. Eddie is currently set up to run using a `.env` file to fetch and use the necessary Discord token from the machine locally. This is also stored as a repository secret for collaborators.


Bot prefix is currently set to `!` or by directly using @ to mention him.

Note that some commands/features requires the user to have a role called `bots` to work.

Pull requests welcome!

## Commands and features
Eddie is currently very limited in functionality, but it can easily be extended for future purposes. 
See the [discord.py docs](https://discordpy.readthedocs.io/en/latest/index.html) for more.

When a student joins the Discord channel, Eddie sends a DM with a general greeting and some information.
This message is currently written in a way that does not depend on the particular course.

### Commands
- `!ping`: check if bot is up.
- `!toggle [channel]`: lock/unlock a channel (defaults to `#queue`) for regular members to send messages. 
Note that this will purge all bot messages upon locking a channel.
- `!docs <keyword>`: get Python documentation for `keyword`.
- `!help [command]`: view the help

### Queue workflow
This section assumes the server has a "queue" channel where students post their name to indicate that they need help during lab hours. 
The channel is assumed to be called either `#queue` or `#kö`. The workflow then proceeds as follows:
1. When a TA is ready, they *reply* to the student's message in the queue channel
2. Eddie reacts with ✅ to the TA's message.
3. When the student joins the TA's voice channel for help, the TA also reacts with ✅ to their message.
4. Eddie deletes both the students original message and the TA's response.

This requires minimal intervention to keep the queue channel clear and easy to navigate for students and TA's.

## Testing and deploying
For testing locally, request collaborator access to get the token, clone the repo and create the `.env` file in the `eddie` folder. Finally, start the bot by simply running `python3 eddie.py` and he should wake up and be shown as active in all Discord servers.

Eddie can easily be hosted on a Heroku account on the free plan. This seems to be enough to keep him running 24/7, but it might be good to look into other options.

Instructions on how to use the Discord developer portal to invite the bot, and how to get started with the `discord.py` library can be found in [this helpful article](https://realpython.com/how-to-make-a-discord-bot-python/).

## The name
Yes, it is a hitchhikers reference. :)
