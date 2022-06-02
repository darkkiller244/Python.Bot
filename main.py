from email import message
import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix='.')


'''
-- [EVENTS] --
'''

@client.event
async def on_ready():
    print("{0.user}".format(client) + " initialized.")

@client.event
async def on_member_join(member):
    print(f'{member} has joined the server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

'''
-- [COMMANDS] --
'''

## General Commands ##

# Event on [tannounce] command usage
@client.command(aliases = ['tannounce', 'testembed', 'embedtest', 'tembed'])
async def test_embed():
    embedded_message = discord.Embed(
        title = "Title",
        description = "This is a description",
        color = discord.color.grey()
    )

    embedded_message.set_footer(text = "This is a footer.")
    embedded_message.set_image(url = "https://cdn.discordapp.com/attachments/858185531542994984/981244192279892038/python-icon-filled-python-icon-website-design-mobile-app-development-python-icon-filled-development-collection-155362649.jpg")
    embedded_message.set_thumbnail(url = "https://cdn.discordapp.com/attachments/858185531542994984/981244599685230692/unknown.png")
    embedded_message.set_author(name = "Author Name", icon_url="https://cdn.discordapp.com/attachments/858185531542994984/981244868724666429/unknown.png")
    embedded_message.add_field(name = "Field Name1", value="Field Value", inline=False)
    embedded_message.add_field(name = "Field Name2", value="Field Value2", inline=True)
    embedded_message.add_field(name = "Field Name3", value="Field Value3", inline=True)

    await client.say(embed = embedded_message)

# Event on [ping] command usage
@client.command(aliases = ['ping', 'latency'])
async def grab_latency(ctx):
    await ctx.send(f'{round(client.latency * 1000)}ms')

## Moderation Commands ##

# Event on [kick] command usage
@client.command()
async def kick(ctx, member: discord.Member, *, reason = None):
    await member.kick(reason = reason)

# Event on [ban] command usage
@client.command()
async def ban(ctx, member: discord.Member, *, reason = None):
    await member.ban(reason = reason)

# Event on [clear] command usage
@client.command(aliases = ['clear', 'purge', 'delete'])
async def clear_chat(ctx, amount: int = 5, member: discord.Member = None):

    if member == None:
        await ctx.channel.purge(limit = amount, check = lambda msg: msg.id != ctx.message.id)
        await ctx.send(f'{amount} messages have been cleared.')
    else:
        print('Member not none')


@client.command()
async def test(ctx):
    if ctx.message.content.startswith(client.command_prefix):
        print('works')
    else:
        print('doesn\'t work')

'''
-- [ERRORS] --
'''

@clear_chat.error
async def info(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send(error)

client.run(os.environ["DISCORD_TOKEN"])
