import discord
from discord.ext import commands

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="hello",
        description="Saudação simples",
    )
    async def hello(self, ctx):
        await ctx.send("Olá!")

def setup(bot):
    bot.add_cog(SlashCommands(bot))
