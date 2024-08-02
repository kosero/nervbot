import os
import re

import aiohttp
import discord
from dotenv import load_dotenv
import random

import nerv
import amadeus

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
MAX_HISTORY = os.getenv("MAX_HISTORY")
#ZINCIRLI = os.getenv("ZINCIRLI")
ZINCIRLI=1268673900271767672
ZN_KEY = os.getenv("ZN_KEY")
WELCOME = os.getenv("WELCOME")

KNECOPARA=["miyav","mıyav","meow","miyaw","mıyaw"]

@bot.event
async def on_ready():
    print(f"name: {bot.user}")

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, id=1235920675642933248)
    await member.add_roles(role)

    bekleme = bot.get_channel(1246509796329390192)
    await send_webhook_msj("neco", bekleme, f"{WELCOME}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    if content.startswith("sex"):
        await nerv.send_webhook_message("neco", message.channel, "Burenyuu!")
    
    if any(content.startswith(keyword) for keyword in KNECOPARA):
        await nerv.send_webhook_message("necopara", message.channel, "miyav.")

    # Check if the bot is mentioned or the message is a DM
    if bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel) or message.content.lower().startswith('kosero'):
        # Start Typing to seem like something happened
        cleaned_text = amadeus.clean_discord_message(message.content)

        async with message.channel.typing():
            # Check for image attachments
            if message.attachments:
                print("New Image Message FROM:" + str(message.author.id) + ": " + cleaned_text)
                # Currently no chat history for images
                for attachment in message.attachments:
                    # These are the only image extensions it currently accepts
                    if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']):
                        await message.add_reaction('<:ayak:1245436100898717706>')

                        async with aiohttp.ClientSession() as session:
                            async with session.get(attachment.url) as resp:
                                if resp.status != 200:
                                    await message.channel.send('Unable to download the image.')
                                    return
                                image_data = await resp.read()
                                response_text = await amadeus.generate_response_with_image_and_text(image_data, cleaned_text)
                                # Split the Message so discord does not get upset
                                await amadeus.split_and_send_messages(message, response_text, 1700, reply_to=message)
                                return
            # Not an Image do text response
            else:
                await message.add_reaction('<:yazmak:1248267984275898378>')

                # Check if history is disabled just send response
                if(MAX_HISTORY == 0):
                    response_text = await amadeus.generate_response_with_text(cleaned_text)
                    # Add AI response to history
                    await amadeus.split_and_send_messages(message, response_text, 1700, reply_to=message)
                    return
                # Add user's question to history
                amadeus.update_message_history(message.author.id, cleaned_text)
                response_text = await amadeus.generate_response_with_text(amadeus.get_formatted_message_history(message.author.id))
                # Add AI response to history
                amadeus.update_message_history(message.author.id, response_text)
                # Split the Message so discord does not get upset

                if "@everyone" in response_text or "@here" in response_text:
                    response_clean_text = response_text.replace("@everyone", "everyone").replace("@here", "here")
                    await amadeus.split_and_send_messages(message, response_clean_text, 1700, reply_to=message)
                    return

                await amadeus.split_and_send_messages(message, response_text, 1700, reply_to=message)

    if message.channel.id == ZINCIRLI:
        encrypted_message = nerv.encrypt(message.content, ZN_KEY)
        await nerv.send_webhook_message("custom", message.channel, encrypted_message, custom_avatar=message.author.avatar.url, custom_name=message.author.name)
        await message.delete()

### SLASH COMMAND
# KAYIT 
@bot.slash_command(
    name="kayit",
    description="Bir üyenin kaydını yapar.",
    guild_ids=[1154598232651997214]
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

# AI RESET
@bot.slash_command(
    name="reset",
    description="AI'nin hafızasını siler.",
    guild_ids=[1154598232651997214]
)
async def reset(ctx: discord.ApplicationContext):
    if ctx.author.id in message_history:
        del message_history[ctx.author.id]
        await ctx.respond(f"🤖 {ctx.author.mention} mesaj geçmişiniz başarıyla sıfırlandı.")
    else:
        await ctx.respond(f"🤖 {ctx.author.mention}, mesaj geçmişiniz zaten sıfırlandı veya bulunamadı.")

# ZINCIR
@bot.slash_command(
    name="encrypt",
    description="Mesaji sifreler.",
    guild_ids=[1154598232651997214]
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
    description="Mesaji donusturur.",
    guild_ids=[1154598232651997214]
)
async def decrypt(ctx, message_id: str):
    required_role_id = 1213598172040003604

    if any(role.id == required_role_id for role in ctx.author.roles):
        try:
            message = await ctx.channel.fetch_message(int(message_id))
            decrypted_message = nerv.decrypt(message.content, ZN_KEY)
            await ctx.respond(decrypted_message, ephemeral=True)

        except Exception as e:
            await ctx.respond(f"Hata: {e}", ephemeral=True)

bot.run(DC_TOKEN)
