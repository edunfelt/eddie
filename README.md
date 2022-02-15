# Discord bot: Eddie the computer
A discord bot to help manage programming courses. Eddie is hosted on my Heroku account currently on the free plan. 
This should be enough to keep him running 24/7, but it might be good to look into other options in the future.

Bot prefix is currently set to `>`.

Note that some commands/features requires the user to have a role called `bots` to work.

## Commands and features
Eddie is currently very limited in functionality, but it can easily be extended for future purposes. 
See the [discord.py docs](https://discordpy.readthedocs.io/en/latest/index.html) for more.

When a student joins the Discord channel, Eddie sends a DM with a general greeting and some information.
This message is currently written in a way that does not depend on the particular course.

### Commands
- `>ping`: check if bot is up.
- `>toggle [channel]`: lock/unlock a channel (defaults to `#queue`) for regular members to send messages. 
Note that this will purge all bot messages upon locking a channel.
- `>docs <keyword>`: get Python documentation for `keyword`.

### Queue workflow
This section assumes the server has a "queue" channel where students post their name to indicate that they need help during lab hours. 
The channel is assumed to be called either `#queue` or `#kö`. The workflow then proceeds as follows:
1. When a TA is ready, they *reply* to the student's message in the queue channel
2. Eddie reacts with ✅ to the TA's message.
3. When the student joins the TA's voice channel for help, the TA also reacts with ✅ to their message.
4. Eddie deletes both the students original message and the TA's response.

This requires minimal intervention to keep the queue channel clear and easy to navigate for students and TA's.

## The name
Yes, it is a hitchhikers reference. :)
