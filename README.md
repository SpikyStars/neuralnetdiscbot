# Neural Net Discord Bot

This is a bot for the online chat service Discord that uses pre-trained neural network models from the PyTorch model zoo.

## Usage
You will need to self-host the bot as I don't have the resources to host a public bot.

You'll want to create a `token.txt` file in the main project directory, containing your Discord bot's token.

Optionally, the bot checks for a `guild_ids.txt` file. 
If there are valid guild IDs present (a guild ID is the ID of a Discord server), the bot's commands will be registered as guild commands, assuming the bot is a member of the specified servers.
Otherwise, they will be registered as global commands.
You can read what the difference is [here](https://discord.com/developers/docs/interactions/application-commands#registering-a-command).

## Screenshots

<img src="https://i.imgur.com/QNJBoaz.png" alt="Screenshot of bot output, and the command to use."/>

<img src="https://i.imgur.com/YNdfkKz.png" alt="Another screenshot of bot output"/>