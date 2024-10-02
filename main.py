import os

import discord
from discord import Intents, app_commands, client
from dotenv import load_dotenv
import random
import json

from src import nerv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True
intents.guilds = True

client = discord.Client(command_prefix="!", intents=intents)
tree = app_commands.CommandTree(client)

###################
#    VARiABLES    #
###################
DC_TOKEN = os.getenv("DC_TOKEN")
ZN_KEY = os.getenv("ZN_KEY")

with open('config.json', 'r') as file:
    config = json.load(file)

ROL_BEKLE = config["ROL_BEKLE"]
ROL_LUMiRIAN = config["ROL_LUMiRIAN"]

THREAD_REGISTRY = config["THREAD_REGISTRY"]
CHANNEL_MESSAGE = config["CHANNEL_MESSAGE"]
CHANNEL_ZINCIRLI = config["CHANNEL_ZINCIRLI"]
CHANNEL_BEKLE = config["CHANNEL_BEKLE"]

MIYAV_DIALOGUE = config["MIYAV_DIALOGUE"]
MIYAV_REPLY = config["MIYAV_REPLY"]

GUILD = config["GUILD"]

ROL_BEKLE = config["ROL_BEKLE"]
ROL_LUMiRIAN = config["ROL_LUMiRIAN"]

c2v4 = config["c2v4"]

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, id=ROL_BEKLE)
    await member.add_roles(role)

    bekleme = client.get_channel(CHANNEL_BEKLE)
    await nerv.send_webhook_message("neco", bekleme, f"Hos geldin {member.mention}, sunucuya katilman icin bir kac soruya cevap vermelisin.\n> Yasin kac?\n> Sunucuya neden katildin?")

@client.event
async def on_ready():
    await tree.sync()
    print(f"name: {client.user}")

@client.event
async def on_message_delete(message):
    if message.author == client.user:
        return
    if message.webhook_id:
        return

@client.event
async def on_message_delete(message):
    if message.author == client.user:
        return
    if message.webhook_id:
        return

    avatar_url = message.author.avatar.url if message.author.avatar else "https://i.imgur.com/CSU09SU.png"
    content = message.content

    attachments = message.attachments
    if attachments:
        for attachment in attachments:
            content += f"\n\n[Attachment]({attachment.url})"
   
    if "@everyone" in content:
        nerv.change_words(content, "@everyone", "#everyone")

    channel = client.get_channel(CHANNEL_MESSAGE)
    await nerv.send_webhook_message(
        "custom", 
        channel,
        content,
        custom_avatar=avatar_url,
        custom_name=f"{message.author.name} [\'{message.author.id}\' \'{message.id}\']"
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.webhook_id:
        return
        
    content = message.content.lower()

    if content.startswith("nya"):
        await nerv.send_webhook_message("neco", message.channel, "Burenyuu!")
    
    if any(content.startswith(keyword) for keyword in MIYAV_DIALOGUE):
        miyavlama = random.choice(MIYAV_REPLY)
        await nerv.send_webhook_message("necopara", message.channel, miyavlama)
    
    if message.channel.id == CHANNEL_ZINCIRLI:
        encrypted_message = nerv.encrypt(message.content, ZN_KEY)
        avatar_url = message.author.avatar.url if message.author.avatar else "https://i.imgur.com/CSU09SU.png"
        await nerv.send_webhook_message("custom", message.channel, encrypted_message, custom_avatar=avatar_url, custom_name=message.author.name)
        await message.delete()

#######################
## encrypt / decrypt ##
#######################
@tree.command(
    name="encrypt",
    description="Mesaji sifreler."
)
async def encrypt(interaction: discord.Interaction, message: str):
    try:
        encrypted_message = nerv.encrypt(message, ZN_KEY)
        await nerv.send_webhook_message("custom", interaction.channel, encrypted_message, custom_avatar=interaction.user.avatar.url, custom_name=interaction.user.name)
        await interaction.response.send_message("sex", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"{e}", ephemeral=True)

@tree.command(
    name="decrypt",
    description="Mesajin sifresini cozer."
)
async def decrypt(interaction: discord.Interaction, message_id: str):
    if interaction.user.id in c2v4:
        try:
            message = await interaction.channel.fetch_message(int(message_id))
            decrypted_message = nerv.decrypt(message.content, ZN_KEY)
            await interaction.response.send_message(decrypted_message, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"{str(e)}", ephemeral=True)
    else:
        await interaction.response.send_message("sex oldu", ephemeral=True)

###########
## KAYIT ##
###########
@tree.command(
    name="kayit",
    description="Bir üyenin kaydını yapar.",
    guild=discord.Object(id=GUILD)
)
async def kayit(interaction: discord.Interaction, member: discord.Member, age: int = 0, why: str = "None"):
    kayit_rol = discord.utils.get(interaction.guild.roles, id=ROL_LUMiRIAN)
    remove_rol = discord.utils.get(interaction.guild.roles, id=ROL_BEKLE)

    if kayit_rol and remove_rol:
        await member.add_roles(kayit_rol)
        await member.remove_roles(remove_rol)

    log_channel = client.get_channel(CHANNEL_MESSAGE)

    embed = discord.Embed(
        title="Üye Kaydı Yapıldı",
        description=f"**Üye:** {member.mention}\n**Yaş:** {age}\n**Katılma Sebebi:** {why}",
        color=discord.Color.yellow()
    )

    await log_channel.send(embed=embed)
    await interaction.response.send_message("Kayit ettim sex", ephemeral=True)

@tree.command(
    name="avatar",
    description="Avatarı gösterir."
)
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    user = member if member else interaction.user
    avatar_url = user.avatar.url if user.avatar else None

    if avatar_url:
        await interaction.response.send_message(f"{avatar_url}")
    else:
        await interaction.response.send_message("sex oldu", ephemeral=True)

##################
## REI/NECO/... ##
##################
@tree.command(
    name="rei",
    description="REI REI REI REI."
)
async def rei(interaction: discord.Interaction):
    rei_rnd = nerv.reicik()
    await interaction.response.send_message(rei_rnd)

@tree.command(
    name="neco",
    description="NECO NECO NECO NECO."
)
async def neco(interaction: discord.Interaction):
    neco_rnd = nerv.necocuk()
    await interaction.response.send_message(neco_rnd)

@tree.command(
    name="url",
    description="url ekle",
)
async def url(interaction: discord.Interaction, list_name: str, url: str):
    if list_name not in ["neco", "rei"]:
        await interaction.response.send_message("somurtmak", ephemeral=True)
        return
    
    filename = f'{list_name}.json'
    nerv.update_json(f"src/{filename}", url)
    
    await interaction.response.send_message(f"**{list_name.capitalize()}** ekledim sex")

@tree.command(
    name="send",
    description="Mesaj gönderir."
)
async def send(interaction: discord.Interaction, message: str, avatar: str, name: str):
    if "@everyone" in message or "@here" in message:
        message_clr = nerv.change_words(message, "@everyone", "#everyone")
        message_clr = nerv.change_words(message_clr, "@here", "#here")
        await nerv.send_webhook_message(
            "custom", 
            interaction.channel,
            message_clr,
            custom_avatar=avatar,
            custom_name=name
        )
    else:
        await nerv.send_webhook_message(
            "custom", 
            interaction.channel,
            message,
            custom_avatar=avatar,
            custom_name=name
        )
    await interaction.response.send_message("sex", ephemeral=True)

client.run(DC_TOKEN)

