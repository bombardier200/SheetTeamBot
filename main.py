import discord
from discord_ui import Button, UI
from discord import Intents
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import MissingRole
from discord_slash import SlashCommand,cog_ext,SlashContext
from discord_slash.utils.manage_commands import create_choice,create_option
import atexit
import json
import random
from dotenvy import load_env,read_file
import os
load_env(read_file('.env'))
TOKEN=os.environ['DISCORD_TOKEN']
#TOKEN=os.getenv('DISCORD_TOKEN')
class sheetteam(commands.Cog):
    def __init__(self,bot,data,slash):
        self.bot=bot;
        self.channel=None;
        self.testarray=data;
    test_guilds=[683572714564222978]
    @cog_ext.cog_slash(
        name="ping",
        description="Ping test",
        guild_ids=test_guilds,
        options=[
            create_option(
                name="Guild Name",
                description="Enter the guild name",
                required=True,
                option_type=3
            )
        ]
    )
    async def _ping(self,ctx:SlashContext,option:str):
        await ctx.send(option)
    @commands.command()
    async def request(self,ctx:SlashContext,*args):
        guildName=args[0]
        request=" ".join(args[1:len(args)-1])
        sheetLink=args[len(args)-1]
        ticketNumber= len(self.testarray)+random.randint(3,10)
        self.testarray[ticketNumber]={"guildName":guildName,"request":request,"Sheet Link":str(sheetLink)};
        searchRole = get(ctx.guild.roles,name="testRole")
        embed = discord.Embed(title="Sheet Team Request", description="Information regarding your request")
        embed.set_author(name="Sheet Bot", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Request Number", value=ticketNumber)
        embed.add_field(name="Guild Name", value=guildName)
        embed.add_field(name="Issue", value=request)
        embed.add_field(name="Sheet Link", value=sheetLink)
        await ctx.send(embed=embed)
        await ctx.send(f"Added request for sheet team {searchRole.mention}");
    @commands.command()
    async def seerequest(self,ctx):
        if ctx.channel.id==683572715025596428:
            embed=discord.Embed(title="Current Requests", description="This is the current requests for sheet team")
            embed.set_author(name="Sheet Bot")
            for elements in self.testarray:
                embed.add_field(name="Guild Name", value=self.testarray[elements]["guildName"], inline=True)
                embed.add_field(name="Ticket Number", value=elements, inline=True)
                embed.add_field(name='\u200b',value='\u200b',inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.reply("You do not have permission to execute this command")
    """
    @seerequest.error
    async def seerequest_error(self, ctx, error):
        if isinstance(error, MissingRole):
            await ctx.send("Sorry you do not have permission for that command");
    """
    @commands.command()
    async def clearrequest(self,ctx,arg):
        if ctx.channel.id == 683572715025596428:
            self.testarray.pop(arg)
            await ctx.reply("Successfully removed request")
        else:
            await ctx.reply("You do not have permission to execute this command")
    """
    @clearrequest.error
    async def clearrequest_error(self, ctx, error):
        if isinstance(error, MissingRole):
            await ctx.send("Sorry you do not have permission for that command");
    """
    """
    @commands.command()
    async def hello(self,ctx,name:str=None):
        name=name or ctx.author.name
        await ctx.respond(f"hello {name}!")
    """
data={}
with open("data.json","r") as file:
    for key,value in json.load(file).items():
        data[key]=value
def on_close():
    with open("data.json","w") as file:
        json.dump(data,file,indent=3)
        print("Data is dumped")
def main():
    atexit.register(on_close)
    bot = commands.Bot(command_prefix='$',intents=discord.Intents.all())
    slash = SlashCommand(bot, sync_commands=True,override_type=True)
    cogs = [sheetteam(bot,data,slash)]
    for cog in cogs:
        bot.add_cog(cog)
        print(f"Loaded \"{cog.qualified_name}\" cog!")
    bot.run(TOKEN)
if __name__=="__main__":
    main();
