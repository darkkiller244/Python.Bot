from http import client
from discord.ext import commands
import discord


class Miscellaneous(commands.Cog):

    def __init__(self, client):
        self.client = client

    ## [EVENTS] ##

    # Event on [botstatus] command usage
    @commands.command()
    async def botstatus(self, ctx, status = 'online', *, activity = 'Working'):
        await client.change_presence(
            status = discord.Status.status, 
            activity = discord.Game(activity)
            )


    # Event on Member Join
    @commands.Cog.listener()
    async def on_member_join(member):
        print(f'{member} has joined the server.')


    # Event on Member Remove
    @commands.Cog.listener()
    async def on_member_remove(member):
        print(f'{member} has left the server.')


def setup(client):
    client.add_cog(Miscellaneous(client))
