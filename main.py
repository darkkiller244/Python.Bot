from discord.ext import commands
import json
import os


# git add .
# git commit -m 'Sent'
# git push


## [CLASSES] ##


class HelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        for cog in mapping:
            await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in mapping[cog]]}')

    async def send_cog_help(self, cog):
        await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in cog.get_commands()]}')

    async def send_group_help(self, group):
        await self.get_destination().send(f'{group.name}: {[command.name for index, command in enumerate(group.commands)]}')

    async def send_command_help(self, command):
        await self.get_destination().send(command.name)


client = commands.Bot(
    command_prefix='.', help_command=commands.MinimalHelpCommand())  # HelpCommand()


## [FUNCTIONS] ##

# Change prefix for player convience
def get_prefix(client, message):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    return prefixes[str(message.guild.id)]


# Check to verify user on command usage
def verify_author(ctx):
    whitelist = {
        232236405466595328  # DarkEssentials#0001
    }

    if (ctx.author.id in whitelist):
        return True


## [BOT MISC COMMANDS/EVENTS] ##

# When bot joins the server (Creates default value)
@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    # Adds value corrasponding to guild key
    prefixes[str(guild.id)] = '.'

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)


@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    # Removes value corrasponding to guild key
    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)


@client.command(alises=['prefix', 'newprefix', 'setprefix', 'changeprefix'])
async def change_prefix(ctx, prefix=None):
    if prefix == None:
        await ctx.send(f'Incorrect Syntax:\n.prefix [New Prefix]')
    else:
        with open('prefixes.json', 'r') as file:
            prefixes = json.load(file)

        # Adds value corrasponding to guild key
        prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as file:
            json.dump(prefixes, file, indent=4)

        await ctx.send(f'Prefix has been updated to: {prefix}')

## [SERVER MANAGER COMMANDS] ##

# Event on [load] command usage


@client.command()
@commands.check(verify_author)
async def load(ctx, extension=None):
    if extension == None:
        await ctx.send(f'Incorrect Syntax\n.load [Extension]')
    else:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} has been successfully loaded.')


# Event on [unload] command usage
@client.command()
@commands.check(verify_author)
async def unload(ctx, extension=None):
    if extension == None:
        await ctx.send(f'Incorrect Syntax\n.unload [Extension]')
    else:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} has been successfully unloaded.')

# Event on [reload] command usage


@client.command()
@commands.check(verify_author)
async def reload(ctx, extension=None):
    if extension == None:
        await ctx.send(f'Incorrect Syntax\n.reload [Extension]')
    else:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'{extension} has been successfully reloaded.')


# Grabs existing cogs in cogs folder
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):

        # Removes last 3 characters of file name
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.environ["DISCORD_TOKEN"])