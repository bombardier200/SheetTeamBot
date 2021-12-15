import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import MissingRole
from discord import embeds
from dotenvy import load_env,read_file

import os
import asyncio
load_env(read_file('.env'))
TOKEN=os.getenv('DISCORD_TOKEN')
class sheetteam(commands.Cog):
    def __init__(self,bot):
        self.bot=bot;
        self.channel=None;
        self.testarray={};
    """
    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
    
        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')
    """
    @commands.command()
    async def ping(ctx):
        await ctx.reply("this worked")
    @commands.command()
    async def request(self,ctx,request,sheetLink):
        self.testarray[len(self.testarray)+1]={request,str(sheetLink)};
        searchRole = get(ctx.guild.roles,name="testRole")
        await ctx.send(f"Added request for sheet team {searchRole.mention}");

    @commands.command()
    @commands.has_role("admin")
    async def seerequest(self,ctx):
        quote_text=''
        for elements in self.testarray:
            quote_text= quote_text +str(self.testarray[elements])+'\n';
        await ctx.reply(str(quote_text));
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
    @commands.command()
    async def testembed(self,ctx):
        embed=discord.Embed(title="Sample Embed",description="This is a test")
        embed.set_author(name="Sheet Bot",icon_url=ctx.author.avatar_url)
        embed.add_field(name="Request Number",value="1")
        embed.add_field(name="Guild Name",value="Guild name")
        embed.add_field(name="Issue",value="issue")
        embed.add_field(name="sheet link",value="sheet link")
        await ctx.send(embed=embed)
bot=commands.Bot(command_prefix='$')
cogs = [sheetteam(bot)]
for cog in cogs:
    bot.add_cog(cog)
    print(f"Loaded \"{cog.qualified_name}\" cog!")
bot.run(TOKEN)
