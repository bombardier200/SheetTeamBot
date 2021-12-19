import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import MissingRole
import atexit
import json
import random
from discord import embeds
from dotenvy import load_env,read_file

import os
load_env(read_file('.env'))
TOKEN=os.getenv('DISCORD_TOKEN')
class sheetteam(commands.Cog):
    def __init__(self,bot):
        self.bot=bot;
        self.channel=None;
        self.testarray={};
    @commands.command()
    async def ping(self,ctx):
        print(self.testarray[0]["guildName"])
        await ctx.reply("this worked")
    @commands.command()
    async def request(self,ctx,guildName,request,sheetLink):
        #+random.randint(1,20)
        ticketNumber= len(self.testarray)
        self.testarray[ticketNumber]={"guildName":guildName,"request":request,"Sheet Link":str(sheetLink)};
        searchRole = get(ctx.guild.roles,name="testRole")
        embed = discord.Embed(title="Sample Embed", description="This is a test")
        embed.set_author(name="Sheet Bot", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Request Number", value=ticketNumber)
        embed.add_field(name="Guild Name", value=guildName)
        embed.add_field(name="Issue", value=request)
        embed.add_field(name="Sheet Link", value=sheetLink)
        await ctx.send(embed=embed)
        await ctx.send(f"Added request for sheet team {searchRole.mention}");

    @commands.command()
    @commands.has_role("admin")
    async def seerequest(self,ctx):
        quote_text=''
        embed=discord.Embed(title="Current Requests", description="This is the current requests for sheet team")
        embed.set_author(name="Sheet Bot")
        for elements in self.testarray:
            embed.add_field(name="Guild Name",value=self.testarray[elements]["guildName"])
            embed.add_field(name="Ticket Number",value=elements,inline=False)
        await ctx.send(embed=embed)
    @seerequest.error
    async def seerequest_error(self, ctx, error):
        if isinstance(error, MissingRole):
            await ctx.send("Sorry you do not have permission for that command");
    @commands.command()
    @commands.has_role("admin")
    async def clearrequest(self,ctx,arg):
        self.testarray.pop(int(arg))
        await ctx.reply("Sucesfully removed request")
    """
    @clearrequest.error
    async def clearrequest_error(self, ctx, error):
        if isinstance(error, MissingRole):
            await ctx.send("Sorry you do not have permission for that command");
    """
data={}
with open("data.json","r") as file:
    for key,value in json.load(file).items():
        data[key]=value
def on_close():
    with open("data.json","w") as file:
        json.dump(data,file,indent=3)
        print("Data is dumped")
bot=commands.Bot(command_prefix='$')
cogs = [sheetteam(bot)]
for cog in cogs:
    bot.add_cog(cog)
    print(f"Loaded \"{cog.qualified_name}\" cog!")
bot.run(TOKEN)
