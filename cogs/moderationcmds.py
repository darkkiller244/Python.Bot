from http import client
from discord.ext import commands
from discord import Color
import asyncio
import discord


## [CLASSES] ##


class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]

        if amount.isdigit() and unit in ['s', 'm']:
            return (int(amount), unit)

        raise commands.BadArgument(message = 'Not a valid duration.')


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    ## [COMMANDS] ##

    # Event on [kick] command usage
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: commands.MemberConverter, *, reason = None):
        if reason == None:
            await ctx.send(f'Incorrect Syntax:\n.kick [User] [Reason]')
        else:
            await member.kick(reason=reason)
            await ctx.send(f'{member.name} has been kicked.')


    # Event on [ban] command usage

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: commands.MemberConverter, *, reason = None):
        if reason == None:
            await ctx.send(f'Incorrect Syntax:\n.ban [User] [Reason]')
        else:
            await member.ban(reason = reason)
            await ctx.send(f'{member.name} has been banned.')


    # Event on [tempban] command usage

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def tempban(self, ctx, member: commands.MemberConverter, duration: DurationConverter, *, reason = None):
        if reason == None:
            await ctx.send(f'Incorrect Syntax:\n.ban [User] [Time] [Reason]')
        else:
            multipler = {'s': 1, 'm': 60}
            amount, unit = duration

            await ctx.guild.ban(member)
            await ctx.send(f'{member} has been banned for {amount}{unit}.')
            await asyncio.sleep(amount * multipler[unit])
            await ctx.guild.unban(member)


    # Event on [unban] command usage

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()  # Guild = Server
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.name} has been unbanned.')
                return


    # Event on [clear] command usage

    @commands.command(aliases=['clear', 'purge', 'delete'])
    @commands.has_permissions(manage_messages = True)
    async def clear_chat(self, ctx, amount: int = 5, member: commands.MemberConverter = None):

        if member == None:
            await ctx.channel.purge(limit = amount, check = lambda msg: msg.id != ctx.message.id)
            await ctx.send(f'{amount} messages have been cleared.')
        else:
            print('Member not none')


    # Event on [test] command usage

    @commands.command()
    async def test(self, ctx):
        if ctx.message.content.startswith(client.command_prefix):
            print('works')
        else:
            print('doesn\'t work')


    # Event on [tannounce] command usage

    @commands.command(aliases=['tannounce', 'testembed', 'embedtest', 'tembed'])
    async def test_embed(self, ctx):

        embedded_message = discord.Embed(
            title = "Title",
            description = "This is a description",
            color = Color.light_grey())

        embedded_message.set_image(
            url = "https://cdn.discordapp.com/attachments/858185531542994984/981244192279892038/python-icon-filled-python-icon-website-design-mobile-app-development-python-icon-filled-development-collection-155362649.jpg")
        embedded_message.set_thumbnail(
            url = "https://cdn.discordapp.com/attachments/858185531542994984/981244599685230692/unknown.png")
        embedded_message.set_author(
            name = "Author Name", icon_url = "https://cdn.discordapp.com/attachments/858185531542994984/981244868724666429/unknown.png")

        embedded_message.add_field(
            name = "Field Name1", value = "Field Value", inline = False)
        embedded_message.add_field(
            name = "Field Name2", value = "Field Value2", inline = True)
        embedded_message.add_field(
            name = "Field Name3", value = "Field Value3", inline = True)

        embedded_message.set_footer(text = "Announcement by {}".format(ctx.author))

        await ctx.send(embed = embedded_message)


def setup(client):
    client.add_cog(Moderation(client))
