import re

import random
import discord

PPLER = ["https://i.imgur.com/0S2ygVX.png", "https://i.imgur.com/ljGAfMg.jpeg", "https://i.imgur.com/MDlYUhn.png", "https://i.imgur.com/hChEtBh.png", "https://i.imgur.com/m6K8L1x.png", "https://i.imgur.com/2Pql211.png", "https://i.imgur.com/auiZpUy.png", "https://i.imgur.com/1cifm70.png"]

async def get_or_create_webhook(channel):
    webhooks = await channel.webhooks()
    webhook = discord.utils.get(webhooks, name="Neco Arc")
    if webhook is None:
        webhook = await channel.create_webhook(name="Neco Arc", reason="Bot için")
        print(f"Webhook created in {channel.name}")
    return webhook

async def send_webhook_message(character, channel, message, custom_avatar=None, custom_name=None):
    webhook = await get_or_create_webhook(channel)
    
    if character == "neco":
        avatar_url = random.choice(PPLER)
        username = "Neco Arc"
    elif character == "necopara":
        avatar_url = "https://i.imgur.com/NcqY1ff.png"
        username = "Pisi Pisi"
    else:
        avatar_url = custom_avatar
        username = custom_name
    
    await webhook.send(
        message,
        username=username,
        avatar_url=avatar_url,
        wait=False
    )

def encrypt(plaintext, key):
    def encrypt_match(match):
        return match.group(0)

    key_length = len(key)
    key_as_int = [ord(i) for i in key.upper()]
    plaintext_int = [ord(i) for i in plaintext.upper() if i.isalpha()]
    ciphertext = ''
    key_index = 0

    pattern = re.compile(r'<@\d+>')
    parts = pattern.split(plaintext)
    patterns = pattern.findall(plaintext)

    for i, part in enumerate(parts):
        for char in part:
            if char.isalpha():
                value = (ord(char.upper()) - 65 + key_as_int[key_index % key_length] - 65) % 26
                ciphertext += chr(value + 65)
                key_index += 1
            else:
                ciphertext += char
        if i < len(patterns):
            ciphertext += patterns[i]

    return ciphertext

def decrypt(ciphertext, key):
    def decrypt_match(match):
        return match.group(0)

    key_length = len(key)
    key_as_int = [ord(i) for i in key.upper()]
    plaintext = ''
    key_index = 0

    pattern = re.compile(r'<@\d+>')
    parts = pattern.split(ciphertext)
    patterns = pattern.findall(ciphertext)

    for i, part in enumerate(parts):
        for char in part:
            if char.isalpha():
                value = (ord(char.upper()) - 65 - key_as_int[key_index % key_length] + 65) % 26
                plaintext += chr(value + 65)
                key_index += 1
            else:
                plaintext += char
        if i < len(patterns):
            plaintext += patterns[i]

    return plaintext.lower()

