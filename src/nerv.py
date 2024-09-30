import re

import random
import discord
import json

with open('config.json', 'r') as file:
    config = json.load(file)
NECO_PPS = config["NECO_PPS"]
REI_JSON = config["REI_JSON"]
NECO_JSON = config["NECO_JSON"]

def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def update_json(filename, new_url):
    
    data = load_json(filename)
    
    if new_url not in data:
        data.append(new_url)
    
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

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
        avatar_url = random.choice(NECO_PPS)
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

def change_words(text, old_word, new_word):
    updated_text = text.replace(old_word, new_word)
    return updated_text

def reicik():
    rei_img = load_json(REI_JSON)
    return random.choice(rei_img)

def necocuk():
    neco_img = load_json(NECO_JSON)
    return random.choice(neco_img)

