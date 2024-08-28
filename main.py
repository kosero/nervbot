import os
import re
import socket

import aiohttp
import discord
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random
import asyncio

import nerv

message_history = {}

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True
intents.guilds = True

bot = discord.Bot(command_prefix="!", intents=intents)

# VARiABLES
DC_TOKEN = os.getenv("DC_TOKEN")
ZN_KEY = os.getenv("ZN_KEY")

NECO_CVP=["miyav.","meow."]
KNECOPARA=["miyav","mıyav","meow","miyaw","mıyaw","ps"]

GUILD=1154598232651997214
KAYIT_LOG=1246728895957569616
ZINCIRLI=1268673900271767672

REI_CHANNEL=1268249139104448512
NECO_CHANNEL=1268228610645561415

MC_SERVER_HOST = '127.0.0.1'
MC_SERVER_PORT = 6543

@bot.event
async def on_ready():
    print(f"name: {bot.user}")

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, id=1235920675642933248)
    await member.add_roles(role)

    bekleme = bot.get_channel(1246509796329390192)
    await nerv.send_webhook_message("neco", bekleme, f"Hos geldin {member.mention}, sunucuya katilman icin bir kac soruya cevap vermelisin.\n> Yasin kac?\n> Sunucuya neden katildin? (Hangi etiketler dikkatini cekti ornek: anime, sohbet)\n> Sunucuyu nerden buldun? (Disboard fln)\nBunlara cevap verdikten sonra yetkili birisi seni kayit edicektir")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    if content.startswith("nya"):
        await nerv.send_webhook_message("neco", message.channel, "Burenyuu!")
    
    if any(content.startswith(keyword) for keyword in KNECOPARA):
        miyavlama = random.choice(NECO_CVP)
        await nerv.send_webhook_message("necopara", message.channel, miyavlama)

    if message.channel.id == ZINCIRLI:
        encrypted_message = nerv.encrypt(message.content, ZN_KEY)
        avatar_url = message.author.avatar.url if message.author.avatar else "https://i.imgur.com/CSU09SU.png"
        await nerv.send_webhook_message("custom", message.channel, encrypted_message, custom_avatar=avatar_url, custom_name=message.author.name)
        await message.delete()


# KAYIT 
@bot.slash_command(
    name="kayit",
    description="Bir üyenin kaydını yapar.",
    guild_ids=[GUILD]
)
async def kayit(ctx: discord.ApplicationContext, member: discord.Member, age: int, why: str, invite: str):
    kayit_rol = discord.utils.get(ctx.guild.roles, id=1165680635055181885)
    remove_rol = discord.utils.get(ctx.guild.roles, id=1235920675642933248)

    if kayit_rol and remove_rol:
        await member.add_roles(kayit_rol)
        await member.remove_roles(remove_rol)

    log_channel = bot.get_channel(KAYIT_LOG)

    embed = discord.Embed(
        title="Üye Kaydı Yapıldı",
        description=f"**Üye:** {member.mention}\n**Yaş:** {age}\n**Katılma Sebebi:** {why}\n**Davet:** {invite}",
        color=discord.Color.yellow()
    )

    await log_channel.send(embed=embed)
    return

# BAN
@bot.slash_command(
    name="ban",
    description="Birisini banlar iste",
    guild_ids=[GUILD]
)
async def ban(ctx, member : discord.Member, *, reason = None):
    c2V4 = 1155877544256614441
    
    if any(role.id == c2V4 for role in ctx.user.roles):
        await member.ban(reason = reason)
        await ctx.respond("banladim sex", ephemeral=True)
    else:
        await ctx.respond("sex oldu", ephemeral=True)

# ZINCIR
@bot.slash_command(
    name="encrypt",
    description="Mesaji sifreler.",
)
async def encrypt(ctx, message: str):
    try:
        encrypted_message = nerv.encrypt(message, ZN_KEY)

        await nerv.send_webhook_message("custom", ctx.channel, encrypted_message, custom_avatar=ctx.author.avatar.url, custom_name=ctx.author.name) 
        await ctx.respond("sex", ephemeral=True)

    except Exception as e:
        await ctx.respond(f"Hata: {e}", ephemeral=True)

@bot.slash_command(
    name="decrypt",
    description="Mesajin sifresini cozer.",
)
async def decrypt(ctx, message_id: str):
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

    if ctx.user.id in allowed_user_ids:
        try:
            message = await ctx.channel.fetch_message(int(message_id))
            decrypted_message = nerv.decrypt(message.content, ZN_KEY)
            await ctx.respond(decrypted_message, ephemeral=True)
        except Exception as e:
            await ctx.respond(f"{str(e)}", ephemeral=True)
    else:
        await ctx.respond("sex oldu", ephemeral=True)

@bot.slash_command(
    name="avatar",
    description="avatar",
)
async def avatar(ctx, member: discord.Member = None):
    user = member if member else ctx.author
    avatar_url = user.avatar.url if user.avatar else None

    if avatar_url:
        await ctx.respond(f"{avatar_url}")

@bot.slash_command(
    name="rei",
    description="REI REI REI REI.",
)
async def rei(ctx): 
    rei_rnd = nerv.reicik()
    await ctx.respond(rei_rnd)

@bot.slash_command(
    name="neco",
    description="NECO NECO NECO NECO.",
)
async def neco(ctx): 
    neco_rnd = nerv.necocuk()
    await ctx.respond(neco_rnd)

@bot.slash_command(
    name="archwiki",
    description="ArchWiki'de arama yapar",
)
async def archwiki(ctx, query: str):
    page_title, page_url = await nerv.search_archwiki(query)

    if page_url:
        await ctx.respond(f"{page_url}")

@bot.slash_command(
    name="send",
    description="send.",
)
async def send(ctx, message: str, avatar: str, name: str):
    allowed_user_ids = [
        1154585783529910292, # kosero
        1006190399867605072, # arexa
        1271174239696977943, # folia
        723826209691271178, # dark
        1123680439224238102, # FRST
        335882105181569024, # florina
        859752224879542282, # caklit
        1001813025302519809 # yigosa
    ]

    if ctx.user.id in allowed_user_ids:
        await nerv.send_webhook_message("custom", ctx.channel, message, custom_avatar=avatar, custom_name=name)
        await ctx.respond("sex", ephemeral=True)
    else:
        await ctx.respond("sex oldu", ephemeral=True)

@bot.slash_command(
    name="mcserverac",
    description="Minecraft Sunucusunu acar.",
)
async def mcserverac(ctx):
    await ctx.defer()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((MC_SERVER_HOST, MC_SERVER_PORT))
            
            s.sendall(b'start\n')
            response = s.recv(1024).decode('utf-8')

            await ctx.followup.send(f"Sunucu: {response}")
    except Exception as e:
        await ctx.followup.send(f"{e}")


bot.run(DC_TOKEN)
