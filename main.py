import os

import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
import json
import feedparser

from src import nerv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True
intents.guilds = True

client = discord.Client(command_prefix="!", intents=intents)
tree = app_commands.CommandTree(client)

# VARiABLES
DC_TOKEN = os.getenv("DC_TOKEN")
ZN_KEY = os.getenv("ZN_KEY")

with open('config.json', 'r') as file:
    config = json.load(file)

NECO_CVP = config["NECO_CVP"]
KNECOPARA = config["KNECOPARA"]
KOPEKC = config["KOPEKC"]
GUILD = config["GUILD"]
KAYIT_LOG = config["KAYIT_LOG"]
ZINCIRLI = config["ZINCIRLI"]
RSS_FEED_URLS = config["RSS_FEED_URLS"]
RSS_CHANNEL = config["RSS_CHANNEL"]

shared_entries = set()

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, id=1235920675642933248)
    await member.add_roles(role)

    bekleme = client.get_channel(1246509796329390192)
    await nerv.send_webhook_message("neco", bekleme, f"Hos geldin {member.mention}, sunucuya katilman icin bir kac soruya cevap vermelisin.\n> Yasin kac?\n> Sunucuya neden katildin? (Hangi etiketler dikkatini cekti ornek: anime, sohbet)\n> Sunucuyu nerden buldun? (Disboard fln)\nBunlara cevap verdikten sonra yetkili birisi seni kayit edicektir")

@client.event
async def on_ready():
    await tree.sync()
    print(f"name: {client.user}")
    check_rss_feed.start() 

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.lower()

    if content.startswith("nya"):
        await nerv.send_webhook_message("neco", message.channel, "Burenyuu!")
    
    if any(content.startswith(keyword) for keyword in KNECOPARA):
        miyavlama = random.choice(NECO_CVP)
        await nerv.send_webhook_message("necopara", message.channel, miyavlama)

    if any(content.startswith(keyword) for keyword in KOPEKC):
        await nerv.send_webhook_message("kopek", message.channel, "hav hav.")

    if message.channel.id == ZINCIRLI:
        encrypted_message = nerv.encrypt(message.content, ZN_KEY)
        avatar_url = message.author.avatar.url if message.author.avatar else "https://i.imgur.com/CSU09SU.png"
        await nerv.send_webhook_message("custom", message.channel, encrypted_message, custom_avatar=avatar_url, custom_name=message.author.name)
        await message.delete()
    
#
##encrypt / decrypt
#
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
    allowed_user_ids = [
        1154585783529910292,  # kosero
        1006190399867605072,  # arexa
        1271174239696977943,  # folia
        723826209691271178,   # dark
        1123680439224238102,  # FRST
        335882105181569024,   # florina
        859752224879542282,   # caklit
        1001813025302519809   # yigosa
    ]

    if interaction.user.id in allowed_user_ids:
        try:
            message = await interaction.channel.fetch_message(int(message_id))
            decrypted_message = nerv.decrypt(message.content, ZN_KEY)
            await interaction.response.send_message(decrypted_message, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"{str(e)}", ephemeral=True)
    else:
        await interaction.response.send_message("sex oldu", ephemeral=True)
#
## Kayit
#
@tree.command(
    name="kayit",
    description="Bir üyenin kaydını yapar.",
    guild=discord.Object(id=GUILD)
)
async def kayit(interaction: discord.Interaction, member: discord.Member, age: int, why: str, invite: str):
    kayit_rol = discord.utils.get(interaction.guild.roles, id=1165680635055181885)
    remove_rol = discord.utils.get(interaction.guild.roles, id=1235920675642933248)

    if kayit_rol and remove_rol:
        await member.add_roles(kayit_rol)
        await member.remove_roles(remove_rol)

    log_channel = client.get_channel(KAYIT_LOG)

    embed = discord.Embed(
        title="Üye Kaydı Yapıldı",
        description=f"**Üye:** {member.mention}\n**Yaş:** {age}\n**Katılma Sebebi:** {why}\n**Davet:** {invite}",
        color=discord.Color.yellow()
    )

    await log_channel.send(embed=embed)
    await interaction.response.send_message("Kayit ettim sex", ephemeral=True)
#
## Ban/Mute/Kick/Unban/Unmute/Avatar
#
@tree.command(
    name="ban",
    description="Birisini banlar iste",
    guild=discord.Object(id=GUILD)
)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    c2V4 = 1155877544256614441

    if any(role.id == c2V4 for role in interaction.user.roles):
        await member.ban(reason=reason)
        await interaction.response.send_message("Banladim sex", ephemeral=True)
    else:
        await interaction.response.send_message("sex oldu", ephemeral=True)

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
#
## REI/NECO/...
#
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

#
## ArchWiki/send
#
@tree.command(
    name="archwiki",
    description="ArchWiki'de arama yapar"
)
async def archwiki(interaction: discord.Interaction, query: str):
    page_title, page_url = await nerv.search_archwiki(query)

    if page_url:
        await interaction.response.send_message(f"{page_url}")
    else:
        await interaction.response.send_message("sex oldu", ephemeral=True)

@tree.command(
    name="send",
    description="Mesaj gönderir."
)
async def send(interaction: discord.Interaction, message: str, avatar: str, name: str):
    allowed_user_ids = [
        1154585783529910292, # kosero
        1006190399867605072, # arexa
        1271174239696977943, # folia
        723826209691271178,  # dark
        1123680439224238102, # FRST
        335882105181569024,  # florina
        859752224879542282,  # caklit
        1001813025302519809  # yigosa
    ]

    if interaction.user.id in allowed_user_ids:
        await nerv.send_webhook_message("custom", interaction.channel, message, custom_avatar=avatar, custom_name=name)
        await interaction.response.send_message("sex", ephemeral=True)
    else:
        await interaction.response.send_message("sex oldu", ephemeral=True)



@tasks.loop(hours=12)
async def check_rss_feed():
    channel = client.get_channel(RSS_CHANNEL)

    for rss_feed_url in RSS_FEED_URLS:
        feed = feedparser.parse(rss_feed_url)

        for entry in feed.entries:
            entry_id = entry.id
            if entry_id in shared_entries:
                continue

            title = entry.title
            link = entry.link
            summary = entry.summary

            embed = discord.Embed(title=title, url=link, color=discord.Color.blue())

            await channel.send(embed=embed)

            shared_entries.add(entry_id)
            nerv.save_shared_entries(shared_entries)

client.run(DC_TOKEN)