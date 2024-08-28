import re

import random
import discord
import aiohttp

PPLER = ["https://i.imgur.com/0S2ygVX.png", "https://i.imgur.com/ljGAfMg.jpeg", "https://i.imgur.com/MDlYUhn.png", "https://i.imgur.com/hChEtBh.png", "https://i.imgur.com/m6K8L1x.png", "https://i.imgur.com/2Pql211.png", "https://i.imgur.com/auiZpUy.png", "https://i.imgur.com/1cifm70.png", "https://i.pinimg.com/736x/fa/a7/47/faa747a3ddcd789edd288888ef259ccf.jpg", "https://i.pinimg.com/736x/a0/68/6d/a0686da7f616774cf1fa3575b720a3b1.jpg", "https://i.pinimg.com/736x/a6/db/24/a6db247e9ca34d1768a72b0957f8d634.jpg", "https://i.pinimg.com/736x/56/a2/90/56a2909fdaff7ce15b1627129483da14.jpg", "https://i.pinimg.com/736x/36/73/c7/3673c722f56b6233471ad22705f9f583.jpg", "https://i.pinimg.com/736x/2e/fb/d5/2efbd5e3258c6d4d227c5c6db32f3e5f.jpg", "https://i.pinimg.com/736x/e9/a2/73/e9a2731b29809ee7ad433a51de721ef5.jpg"]

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

def reicik():
    rei_img = [
        "https://i.pinimg.com/564x/24/98/a3/2498a3322e639efab12a5db2c9cf9f84.jpg",
        "https://i.pinimg.com/564x/a4/4d/fc/a44dfc1402806ce940d38ac25ecbb8f6.jpg",
        "https://i.pinimg.com/736x/34/4b/a4/344ba4693408d1cba4fb1535b0136690.jpg",
        "https://i.pinimg.com/736x/e9/81/f9/e981f9361413754e8b8af9ce885d0408.jpg",
        "https://i.pinimg.com/564x/a7/b4/05/a7b405d16eec58e3e74680a7a0444662.jpg",
        "https://i.pinimg.com/564x/6b/c6/2f/6bc62f54a2d9af0985cd0f3644c69011.jpg",
        "https://i.pinimg.com/564x/6b/c6/2f/6bc62f54a2d9af0985cd0f3644c69011.jpg",
        "https://i.pinimg.com/564x/6b/c6/2f/6bc62f54a2d9af0985cd0f3644c69011.jpg"
    ]
    return random.choice(rei_img)

def necocuk():
    neco_img = [
        "https://i.pinimg.com/736x/56/a2/90/56a2909fdaff7ce15b1627129483da14.jpg",
        "https://i.pinimg.com/564x/23/ed/9d/23ed9df2dbc4ecbdb5c7e5328c34b233.jpg",
        "https://i.pinimg.com/736x/a6/db/24/a6db247e9ca34d1768a72b0957f8d634.jpg",
        "https://i.pinimg.com/736x/3f/46/ca/3f46ca0e81306ed4ed341e3afddfcd1d.jpg",
        "https://i.pinimg.com/736x/a0/68/6d/a0686da7f616774cf1fa3575b720a3b1.jpg",
        "https://i.pinimg.com/736x/fa/a7/47/faa747a3ddcd789edd288888ef259ccf.jpg",
        "https://i.pinimg.com/564x/9d/71/cf/9d71cf969327a08c94f7f53514102c08.jpg",
        "https://i.pinimg.com/736x/36/73/c7/3673c722f56b6233471ad22705f9f583.jpg",
        "https://i.pinimg.com/736x/26/31/7f/26317f53ee2f871693659ad6f925bc1d.jpg",
        "https://i.pinimg.com/564x/0d/c1/ba/0dc1babea2221d912247ca059e1231dd.jpg",
        "https://i.pinimg.com/736x/e4/14/35/e414356d94bc74a63b3990f64be560cb.jpg",
        "https://i.pinimg.com/736x/2e/fb/d5/2efbd5e3258c6d4d227c5c6db32f3e5f.jpg",
        "https://i.pinimg.com/736x/7b/8a/d8/7b8ad85aa3376d37232616fd94957acd.jpg",
        "https://i.pinimg.com/736x/f3/5e/fb/f35efb2981c09d6f641686b996970216.jpg",
        "https://i.pinimg.com/736x/6c/94/ae/6c94ae413197fd00a9ed5baccedd8628.jpg",
        "https://i.pinimg.com/736x/24/82/c8/2482c85cd08e7414a026be0c85a12a81.jpg",
        "https://i.pinimg.com/736x/ff/26/84/ff26842e13212ab16be65594b67e4521.jpg",
        "https://i.pinimg.com/564x/4c/0d/d7/4c0dd78f81c2fa95c72c8c7b96e8cbd3.jpg",
        "https://i.pinimg.com/736x/e9/a2/73/e9a2731b29809ee7ad433a51de721ef5.jpg",
        "https://i.pinimg.com/564x/f2/09/98/f20998cd408b8955e07cf71a47a752a5.jpg",
        "https://v1.pinimg.com/videos/mc/720p/28/ab/cf/28abcf7ec8a6aa8352910dd1aa5aa995.mp4",
        "https://i.pinimg.com/736x/7d/c9/4e/7dc94e3123e0ff4807c7aaa4b2ed9ae6.jpg",
        "https://i.pinimg.com/564x/07/3c/65/073c65ee8e4a9a2dde3bd0f525fd0fae.jpg",
        "https://i.pinimg.com/564x/66/23/aa/6623aa9d145a4b7a18d7c93ea966d0ec.jpg",
        "https://i.pinimg.com/564x/cc/a5/f4/cca5f482577abbdd800549c25b2687a4.jpg",
        "https://i.pinimg.com/564x/c9/cc/2b/c9cc2bd5156e725bfd1c2dd95274a299.jpg",
        "https://i.pinimg.com/564x/77/1d/23/771d23be8941883d78dfc176b503c290.jpg",
        "https://i.pinimg.com/736x/79/d3/13/79d3133a9cc8f7f14dff46ba4a79b2f5.jpg",
        "https://i.pinimg.com/564x/03/0e/31/030e3155176e0e0854a542abdcd15417.jpg"
    ]
    return random.choice(neco_img)

async def search_archwiki(query: str):
    async with aiohttp.ClientSession() as session:
        url = f"https://wiki.archlinux.org/api.php?action=query&list=search&srsearch={query}&format=json"
        async with session.get(url) as response:
            data = await response.json()

    search_results = data.get("query", {}).get("search", [])
    if not search_results:
        return None, None

    best_result = search_results[0]
    page_title = best_result.get("title")
    page_url = f"https://wiki.archlinux.org/title/{page_title.replace(' ', '_')}"

    return page_title, page_url

