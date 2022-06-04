from http import client
from discord.ext import commands
import discord


class General(commands.Cog):

    def __init__(self, client):
        self.client = client

    ## [COMMANDS] ##

    # Event on [ping] command usage
    @commands.command(aliases = ['latency'])
    async def ping(self, ctx):
        await ctx.send(f'{round(client.latency * 1000)}ms')


def setup(client):
    client.add_cog(General(client))
