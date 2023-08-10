fee = 1.02 # 2%
your_discord_user_id = 757289489373593661
your_roblox_user = "fersord"
WorkspacePath = "C:/Users/henry/AppData/Local/Packages/ROBLOXCORPORATION.ROBLOX_55nm5eh3cm0pr/AC/workspace"
bot_token = ""
ticket_channel = 1123485263834906664

import asyncio
import random
import string
import time
import discord
from discord.ext import commands
import json
import requests
import blockcypher
from pycoingecko import CoinGeckoAPI
import urllib3
import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

cg = CoinGeckoAPI()

api_key = "075825150dd640fe8de61a130208c44e"

deals = {}

def epoch_to_formatted_date(epoch_timestamp) :
    # Convert epoch timestamp to a datetime object
    datetime_obj = datetime.datetime.fromtimestamp(epoch_timestamp)

    # Format the datetime object as "Month Day Year | Hour:Minute:Second"
    formatted_date = datetime_obj.strftime("%b %d %Y | %H:%M:%S")

    return formatted_date


def userid_to_username(user_id) :
    url = f'https://users.roblox.com/v1/users/{user_id}'
    headers = {'accept' : 'application/json'}
    response = requests.get(url, headers=headers)
    return response.json()['name']
def get_ltc_to_usd_price():
    response = cg.get_price(ids='litecoin', vs_currencies='usd')
    return response['litecoin']['usd']
def usd_to_satoshis(usd_amount):
    ltc_to_usd_price = get_ltc_to_usd_price()
    ltc_price_in_satoshis = 100_000_000  # 1 LTC = 100,000,000 satoshis
    satoshis_amount = int(usd_amount / ltc_to_usd_price * ltc_price_in_satoshis)
    return satoshis_amount
def satoshis_to_usd(satoshis_amount):
    ltc_to_usd_price = get_ltc_to_usd_price()
    ltc_price_in_satoshis = 100_000_000  # 1 LTC = 100,000,000 satoshis
    usd_amount = (satoshis_amount / ltc_price_in_satoshis) * ltc_to_usd_price
    return usd_amount
def satoshis_to_ltc(satoshis_amount):
    ltc_price_in_satoshis = 100_000_000  # 1 LTC = 100,000,000 satoshis
    ltc_amount = satoshis_amount / ltc_price_in_satoshis
    return ltc_amount
def ltc_to_satoshis(ltc_amount):
    ltc_price_in_satoshis = 100_000_000  # 1 LTC = 100,000,000 satoshis
    satoshis_amount = ltc_amount * ltc_price_in_satoshis
    return int(satoshis_amount)

def create_new_ltc_address() :
    endpoint = f"https://api.blockcypher.com/v1/ltc/main/addrs?token={api_key}"

    response = requests.post(endpoint)
    data = response.json()

    # Extract the new Litecoin address and private key
    new_address = data["address"]
    private_key = data["private"]

    return new_address, private_key


def get_address_balance(address) :
    endpoint = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance?token={api_key}"

    response = requests.get(endpoint)
    data = response.json()

    balance = data.get("balance", 0)
    unconfirmed_balance = data.get("unconfirmed_balance", 0)

    return balance, unconfirmed_balance

def send_ltc(private_key, recipient_address, amount) :
    tx = blockcypher.simple_spend(from_privkey=private_key,to_address=recipient_address,to_satoshis=amount,api_key=api_key,coin_symbol="ltc")
    return tx

bot = commands.Bot(intents=discord.Intents.all(),command_prefix="<>:@:@")
def succeed(message):
    return discord.Embed(description=f":white_check_mark: {message}", color = 0x7cff6b)
def info(message):
    return discord.Embed(description=f":information_source: {message}", color = 0x57beff)
def fail(message):
    return discord.Embed(description=f":x: {message}", color = 0xff6b6b)
def suffix_to_int(s) :
    suffixes = {
        'k' : 3,
        'm' : 6,
        'b' : 9,
        't' : 12
    }

    suffix = s[-1].lower()
    if suffix in suffixes :
        num = float(s[:-1]) * 10 ** suffixes[suffix]
    else :
        num = float(s)

    return int(num)
def add_suffix(inte) :
    gems = inte
    if gems >= 1000000000000 :  # if gems are greater than or equal to 1 trillion
        gems_formatted = f"{gems / 1000000000000:.1f}t"  # display gems in trillions with one decimal point
    elif gems >= 1000000000 :  # if gems are greater than or equal to 1 billion
        gems_formatted = f"{gems / 1000000000:.1f}b"  # display gems in billions with one decimal point
    elif gems >= 1000000 :  # if gems are greater than or equal to 1 million
        gems_formatted = f"{gems / 1000000:.1f}m"  # display gems in millions with one decimal point
    elif gems >= 1000 :  # if gems are greater than or equal to 1 thousand
        gems_formatted = f"{gems / 1000:.1f}k"  # display gems in thousands with one decimal point
    else :  # if gems are less than 1 thousand
        gems_formatted = str(gems)  # display gems as is
    return gems_formatted
def read():
    with open(WorkspacePath + "/responses.json", "r") as f:
        a = f.read()
        f.close()
        return json.loads(a)
def write(data):
    with open(WorkspacePath + "/call.json", "w") as f:
        f.write(json.dumps(data))
        f.close()

def generate_fid():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(10))

def send_command(name, args):
    fid = generate_fid()
    write({"Name": name, "Args": args, "FID": fid})
    while True:
        time.sleep(0.5)
        responses = read()
        for fid2 in responses:
            if fid2 == fid:
                return responses[fid]

def send_mail(recipient, gems, message):
    send_command("send_mail", {"Recipient" : recipient, "Gems" : gems, "Message" : message})
def check_stock():
    return add_suffix(send_command("check_gems", {})['Gems'])
def get_mail():
    return send_command("get_mail", {})['Mail']
def claim_mail(uid):
    send_command("claim_mail", {"MUID": uid})
def claim_all_mail():
    send_command("claim_all_mail", {})
class CopyPasteButtons(discord.ui.View) :
    def __init__(self, dealid, roblox, ltcad) :
        super().__init__(timeout=None)
        self.dealid = dealid
        self.roblox = roblox
        self.ltcad = ltcad
        self.setup_buttons()

    def setup_buttons(self) :
        button = discord.ui.Button(label="Copy LTC Address", custom_id=f"1", style=discord.ButtonStyle.primary)
        button.callback = self.ltc
        self.add_item(button)
        button = discord.ui.Button(label="Copy Roblox User", custom_id=f"2", style=discord.ButtonStyle.primary)
        button.callback = self.robloxF
        self.add_item(button)
        button = discord.ui.Button(label="Copy Deal Id", custom_id=f"3", style=discord.ButtonStyle.primary)
        button.callback = self.deal
        self.add_item(button)
    async def ltc(self, interaction: discord.Interaction):
        await interaction.response.send_message(ephemeral=True,content=self.ltcad)

    async def robloxF(self, interaction: discord.Interaction) :
        await interaction.response.send_message(ephemeral=True, content=self.roblox)

    async def deal(self, interaction: discord.Interaction) :
        await interaction.response.send_message(ephemeral=True, content=self.dealid)
class MiddleManButtons(discord.ui.View) :
    def __init__(self) :
        super().__init__(timeout=None)
        self.setup_buttons()

    def setup_buttons(self) :
        button = discord.ui.Button(label="Gems For LTC", custom_id=f"gemltc", style=discord.ButtonStyle.primary, emoji="💎")
        button.callback = self.gemltc
        self.add_item(button)

    async def gemltc(self, interaction: discord.Interaction):
        DEALID = generate_fid()
        deals[DEALID] = {}
        deals[DEALID]['channel'] = await interaction.guild.create_text_channel(name=f"DEAL-{DEALID}")
        overwrites = {
            interaction.user : discord.PermissionOverwrite(read_messages=True, send_messages=True),
            interaction.guild.default_role : discord.PermissionOverwrite(read_messages=False)
        }
        await deals[DEALID]['channel'].edit(overwrites=overwrites)
        address, key = create_new_ltc_address()
        deals[DEALID]['address'] = address
        deals[DEALID]['key'] = key
        deals[DEALID]['owner'] = interaction.user.id
        deals[DEALID]['gems'] = None
        deals[DEALID]['usd'] = None
        deals[DEALID]['gemsid'] = None
        deals[DEALID]['gemsuser'] = None
        deals[DEALID]['gemsadd'] = None
        deals[DEALID]['ltcid'] = None
        deals[DEALID]['ltcusername'] = None
        deals[DEALID]['ltcadd'] = None
        deals[DEALID]['stage'] = "gems"
        embed = discord.Embed(description=f"```Middleman's LTC Address: {address}\nMiddleman's Roblox User: {your_roblox_user}\nDEAL_ID: {DEALID}```")
        msg = await deals[DEALID]['channel'].send(embed=embed,view=CopyPasteButtons(dealid=DEALID,roblox=your_roblox_user,ltcad=address))
        deals[DEALID]['message'] = msg
        deals[DEALID]['embed'] = embed
        await deals[DEALID]['channel'].send(embed=succeed(f"<@{deals[DEALID]['owner']}> How Many Gems Are Being Traded?"))
        await interaction.response.send_message(ephemeral=True,content=f"<#{deals[DEALID]['channel'].id}>")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot Ready")
    channel = await bot.fetch_channel(ticket_channel)
    await channel.send(embed=discord.Embed(title="Request Automatic Middleman", description="Only Create a ticket if you have the gems.", color=0xe6e6e6),view=MiddleManButtons())
async def final_middleman(sats, dealid):
    deal = deals[dealid]
    sats_fee = sats * fee
    await deal['channel'].send(embed=info(f"<@{deal['ltcid']}> Send {satoshis_to_ltc(sats_fee)} LTC To {deal['address']} (Go to the first message sent here to copy)"))
    while 1:
        await asyncio.sleep(5)
        bal, unconfirmed_bal = get_address_balance(deal['address'])
        if unconfirmed_bal >= sats:
            await deal['channel'].send(content=f"<@{deal['owner']}> <@{deal['ltcid']}>",embed=succeed("Payment Received! Waiting For Confirmations"))
            break
    while 1:
        await asyncio.sleep(5)
        bal, unconfirmed_bal = get_address_balance(deal['address'])
        if bal >= sats:
            await deal['channel'].send(content=f"<@{deal['owner']}> <@{deal['ltcid']}>",embed=succeed(f"Payment Confirmed! <@{deal['owner']}> Send {add_suffix(deal['gems'])} Gems To ``{your_roblox_user}`` (Go to the first message sent here to copy)"))
            break
    while 1 :
        await asyncio.sleep(5)
        b = False
        for mail in get_mail():
            if mail['Diamonds'] >= deal['gems']:
                b = True
                claim_all_mail()
                await deal['channel'].send(content=f"<@{deal['owner']}> <@{deal['ltcid']}>", embed=succeed(f"Gems Received! Your Payments Will Be Forwarded On To eachother, Thank you for using our service"))
                break
        if b:
            break
    send_mail(deal['ltcusername'],deal['gems'],"AUTO MM")
    send_ltc(deal['key'],deal['gemsadd'],sats)
print(get_mail())
@bot.event
async def on_message(message: discord.Message):
    if message.author.id == bot.user.id:
        return
    for dealid in deals:
        deal = deals[dealid]
        if deal['channel'].id == message.channel.id:
            stage = deal['stage']
            if message.author.id == deal['owner']:
                if stage == "gems":
                    if suffix_to_int(message.content) >= 1000:
                        deals[dealid]['gems'] = suffix_to_int(message.content)
                        deals[dealid]['stage'] = "usd"
                        await message.reply(embed=succeed(f"<@{deal['owner']}> How Much USD Is Being Traded"))
                    else:
                        await message.reply(embed=fail(f"<@{deal['owner']}> Min Amount Is 100b"))
                if stage == "usd":
                    try:
                        if float(message.content) >= 0.5:
                            deals[dealid]['usd'] = float(message.content)
                            deals[dealid]['stage'] = "gemsid"
                            await message.reply(embed=succeed(f"<@{deal['owner']}> What is your roblox user **id**"))
                        else:
                            await message.reply(embed=fail(f"<@{deal['owner']}> Must Be Over 0.50$"))
                    except:
                        await message.reply(embed=fail(f"<@{deal['owner']}> Remove The $ Symbol"))
                if stage == "gemsid":
                    deals[dealid]['gemsid'] = message.content
                    deals[dealid]['gemsuser'] = userid_to_username(message.content)
                    deals[dealid]['stage'] = "gemsadd"
                    await message.reply(embed=succeed(f"<@{deal['owner']}> What is your ltc address?"))
                if stage == "gemsadd":
                    deals[dealid]['gemsadd'] = message.content
                    deals[dealid]['stage'] = "ltcid"
                    await message.reply(embed=succeed(f"<@{deal['owner']}> What is the discord id of the person with the ltc?"))
                if stage == "ltcid" :
                    deals[dealid]['ltcid'] = message.content
                    deals[dealid]['stage'] = "ltcusername"

                    # Get the user object based on the provided user ID
                    user_id = int(message.content)
                    user = message.guild.get_member(user_id)
                    channel = deals[dealid]['channel']

                    overwrites = {
                        user : discord.PermissionOverwrite(read_messages=True, send_messages=True),
                        message.guild.default_role : discord.PermissionOverwrite(read_messages=False)
                    }
                    await channel.edit(overwrites=overwrites)
                    await channel.send(embed=info(f"<@{user_id}> Was Added To The Ticket"),content=f"<@{user_id}>")
                    await channel.send(embed=succeed(f"<@{message.content}> What is your Roblox username?"))
            else:
                if stage == "ltcusername":
                    deals[dealid]['ltcusername'] = message.content
                    deals[dealid]['stage'] = "ltcadd"
                    await message.reply(embed=succeed(f"<@{deals[dealid]['ltcid']}> What is your LTC Address?"))
                if stage == "ltcadd":
                    deals[dealid]['ltcadd'] = message.content
                    asyncio.create_task(final_middleman(usd_to_satoshis(deal['usd']), dealid))


def console_embed(console):
    return discord.Embed(title="Connecting To Api", description=f"```{console}```")

class ClaimButtons(discord.ui.View) :
    def __init__(self, interaction) :
        super().__init__(timeout=None)
        self.interaction = interaction
        self.setup_buttons()

    def setup_buttons(self) :
        button = discord.ui.Button(label="Claim All Mail", custom_id=f"join", style=discord.ButtonStyle.danger, emoji="⚠️")
        button.callback = self.button_join
        self.add_item(button)

    async def button_join(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user.id == your_discord_user_id:
            claim_all_mail()
            await self.interaction.edit_original_response(view=None,embed=succeed("Claimed All Mail."))

@bot.tree.command(name="check_stock",description="Check How Many Gems Are On The Bot")
async def CHECK(interaction: discord.Interaction):
    if interaction.user.id == your_discord_user_id:
        console = "> Sent Command To API"
        await interaction.response.send_message(embed=console_embed(console))
        time.sleep(0.4)
        console += "\n> Awaiting API Response"
        await interaction.edit_original_response(embed=console_embed(console))
        gems = check_stock()
        await interaction.edit_original_response(embed=info(f"The Bot Has {gems} Gems."))
    else:
        await interaction.response.send_message(embed=fail("Only Admins Can Do This"))
@bot.tree.command(name="check_mail",description="Check The Inbox Of The Middleman Agent")
async def CHECKMAIL(interaction: discord.Interaction):
    if interaction.user.id == your_discord_user_id:
        console = "> Sent Command To API"
        await interaction.response.send_message(embed=console_embed(console))
        time.sleep(0.4)
        console += "\n> Awaiting API Response"
        await interaction.edit_original_response(embed=console_embed(console))
        mail = get_mail()
        embed=discord.Embed(title="📮 Inbox", description="Viewing all mail sent to the middleman bot in Pet Simulator X", color=0xffbb29)
        Istr = ""
        for item in mail:
            Istr += f"``{add_suffix(item['Diamonds'])}`` - ``{epoch_to_formatted_date(round(item['Timestamp']))}`` - ``{item['Sender']}``\n"
        embed.add_field(name="Inbox",value=Istr)
        await interaction.edit_original_response(embed=embed,view=ClaimButtons(interaction=interaction))
    else:
        await interaction.response.send_message(embed=fail("Only Admins Can Do This"))
@bot.tree.command(name="send_ltc",description="Send LTC")
async def send_ltcC(interaction: discord.Interaction, private_key: str, recipient: str, amount_usd: float):
    if interaction.user.id == your_discord_user_id:
        send_ltc(private_key,recipient,usd_to_satoshis(amount_usd))
        await interaction.response.send_message(embed=succeed("LTC Sent"))
    else:
        await interaction.response.send_message(embed=fail("Only Admins Can Do This"))
@bot.tree.command(name="send_gems",description="Send Gems")
async def send_gemsC(interaction: discord.Interaction, recipient: str, amount: int):
    if interaction.user.id == your_discord_user_id:
        send_mail(recipient=recipient,gems=amount,message="Transaction FAIL")
        await interaction.response.send_message(embed=succeed("Gems Sent"))
    else:
        await interaction.response.send_message(embed=fail("Only Admins Can Do This"))
@bot.tree.command(name="get_private_key",description="Get The Private Key Of A Wallet")
async def GETKEY(interaction: discord.Interaction, deal_id: str):
    if interaction.user.id == your_discord_user_id:
        key = deals[deal_id]['key']
        await interaction.response.send_message(embed=info(key))
    else:
        await interaction.response.send_message(embed=fail("Only Admins Can Do This"))
@bot.tree.command(name="get_wallet_balance",description="Get The Balance Of A Wallet")
async def GETBAL(interaction: discord.Interaction, address: str):
    balsats, unbalsats = get_address_balance(address)
    balusd = satoshis_to_usd(balsats)
    balltc = satoshis_to_ltc(balsats)
    unbalusd = satoshis_to_usd(unbalsats)
    unballtc = satoshis_to_ltc(unbalsats)
    embed = discord.Embed(title=f"Address {address}",description=f"**Balance**\n\nUSD: {balusd}\nLTC: {balltc}\nSATS: {balsats}\n\n**Unconfirmed Balance**\n\nUSD: {unbalusd}\nLTC: {unballtc}\nSATS: {unbalsats}")
    await interaction.response.send_message(embed=embed)


bot.run(bot_token)