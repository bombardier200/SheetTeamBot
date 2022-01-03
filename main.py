import discord
from discord_ui import Button, UI
from discord import Intents
from discord.ext import commands
from discord.ext.commands import MissingRole
from discord_slash import SlashCommand,cog_ext,SlashContext
from discord_slash.utils.manage_commands import create_choice,create_option
import atexit
from discord_components import DiscordComponents,Button,Select,SelectOption,ButtonStyle,ComponentsBot
from discord.utils import get
import json
import random
from pymongo import MongoClient
from dotenvy import load_env,read_file
import os
load_env(read_file('.env'))
TOKEN=os.environ['DISCORD_TOKEN']
MONGODB_URI=os.environ['MONGODB_URI']
client=MongoClient(MONGODB_URI)
db=client["testDB"]
mycollection=db["testDB"]
class sheetteam(commands.Cog):
    def __init__(self,bot,data,slash):
        self.bot=bot;
        self.channel=None;
        self.testarray=data;
    test_guilds=[683572714564222978]
    @commands.Cog.listener()
    async def on_ready(self):
        channel=self.bot.get_channel(683572715025596428)
        await channel.send("test")
    @cog_ext.cog_slash(
        name="ping",
        description="Ping for testing bot",
        guild_ids=test_guilds
    )
    async def _ping(self,ctx:SlashCommand):
        await ctx.send("Pong" +'\n'+ "Latency: "+ str(round(self.bot.latency*1000,1)))
        for x in mycollection.find():
            print(x)
    @cog_ext.cog_slash(
        name="request",
        description="requesting a fix for a sheet",
        guild_ids=test_guilds,
        options=[
            create_option(
                name="guild",
                description="Enter the guild name",
                required=True,
                option_type=3,
            ),
            create_option(
                name="issue",
                description="Enter the issue",
                required=True,
                option_type=3,
            ),
            create_option(
                name="sheet",
                description="Enter the sheet link",
                required=True,
                option_type=3,
            )
        ]
    )
    async def _request(self,ctx:SlashContext,guild:str,issue:str,sheet:str):
        guildName=guild
        request=issue
        sheetLink=sheet
        ticketNumber = len(self.testarray) + random.randint(3, 10)
        self.testarray[str(ticketNumber)] = {"guildName": guildName, "request": request, "Sheet_Link": str(sheetLink)};
        searchRole = get(ctx.guild.roles, name="testRole")
        embed = discord.Embed(title="Sheet Team Request", description="Information regarding your request")
        embed.set_author(name="Sheet Bot", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Request Number", value=ticketNumber)
        embed.add_field(name="Guild Name", value=guildName)
        embed.add_field(name="Issue", value=request)
        embed.add_field(name="Sheet Link", value=sheetLink)
        await ctx.send(embed=embed)
        await ctx.send(f"Added request for sheet team {searchRole.mention}");

    @cog_ext.cog_slash(
        name="seerequest",
        description="See the current requests",
        guild_ids=test_guilds
    )
    async def _seerequest(self,ctx:SlashContext):
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

    @cog_ext.cog_slash(
        name="clearrequest",
        description="clear a request",
        guild_ids=test_guilds,
        options=[
            create_option(
                name="ticketnumber",
                description="Enter the ticket number to clear",
                required=True,
                option_type=4
            )
        ]
    )
    async def _clearrequest(self,ctx:SlashContext,ticketnumber:int):
        if ctx.channel.id == 683572715025596428:
            self.testarray.pop(ticketnumber)
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
    @commands.command()
    async def testing(self,ctx):
        await ctx.send(content="raid type", components=[
                Select(
                    placeholder='SelectMenu',
                       options=[
                           SelectOption(
                               label="Normal",
                               value="Normal"
                           ),
                           SelectOption(
                               label="Heroic",
                               value="Heroic"

                           ),
                           SelectOption(
                               label="Mythic",
                               value="Mythic"
                           )

                       ],
                       custom_id="Selecttesting"
                )
            ])
    @commands.Cog.listener()
    async def on_select_option(self,interaction):
        res = interaction.values[0]
        if res == "Cancel":
            await interaction.send("You have canceled your select option")
        elif res == "Normal":
            await interaction.send("You have chosen Normal")
        elif res == "Heroic":
            await interaction.send("You have chosen Heroic")
        elif res == "Mythic":
            await interaction.send("You have chosen Mythic")

data={}
""""
with open("data.json","r") as file:
    for key,value in json.load(file).items():
        data[key]=value
file.close()
"""
@atexit.register
def on_close():
    print("Got here")
    x = mycollection.insert_one(data)
def main():
    bot = commands.Bot(command_prefix='$',intents=discord.Intents.all())
    slash = SlashCommand(bot, sync_commands=True,override_type=True)
    test1=DiscordComponents(bot)
    cogs = [sheetteam(bot,data,slash)]
    for cog in cogs:
        bot.add_cog(cog)
        print(f"Loaded \"{cog.qualified_name}\" cog!")
    bot.run(TOKEN)
if __name__=="__main__":
    main();
