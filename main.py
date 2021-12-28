import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import MissingRole
import atexit
import json
import random
from dotenvy import load_env,read_file
import os
load_env(read_file('.env'))
TOKEN=os.environ['DISCORD_TOKEN']
#TOKEN=os.getenv('DISCORD_TOKEN')
class sheetteam(commands.Cog):
    def __init__(self,bot,data):
        self.bot=bot;
        self.channel=None;
        self.testarray=data;
    @commands.command()
    async def ping(self,ctx):
        await ctx.reply("pong")
    @commands.command()
    async def request(self,ctx,*args):
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
    bot = commands.Bot(command_prefix='$')
    cogs = [sheetteam(bot,data)]
    for cog in cogs:
        bot.add_cog(cog)
        print(f"Loaded \"{cog.qualified_name}\" cog!")
    bot.run(TOKEN)
if __name__=="__main__":
    main();
