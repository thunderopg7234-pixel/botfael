from flask import Flask
import threading
import os

# 1. Create a tiny web server
app = Flask(__name__)

@app.route('/')
def heartbeat():
    return "ALIVE", 200

# 2. Function to run the server on Render's port
def run_pinger():
    # Render uses port 10000 by default
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 3. Start the server in the background so it doesn't stop your bot
threading.Thread(target=run_pinger, daemon=True).start()


# main.py
import random
import asyncio
import logging
from telethon import TelegramClient, events
import json
from pypinyin import lazy_pinyin
from telethon.tl.custom.message import Message
from telethon.sessions import StringSession

rc_only_cache = {}

# ------------------ CONFIG ------------------ #
API_ID = 20865160  # Your API ID
API_HASH = "acdc2c286e50d2b9561941b3ea72c7cb"  # Your API Hash
OWNER_ID = 1873766873
OWNER_USERNAME = "faelninety1"
SPECIAL_USER_ID = 6554296968
USERBOT_VERSION = "1.0"
PREFIX = "."
MY_ID = 1873766873
# -------------------------------------------- #

SESSION_STRING = os.getenv("SESSION_STRING")

# Initialize Telethon client withouit string session
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

from telethon import TelegramClient, events
from telethon.tl.functions.contacts import GetContactsRequest, DeleteContactsRequest
import asyncio

@client.on(events.NewMessage(pattern=r"\.deletecont$"))
async def delete_contacts(event):
    await event.reply("⚠️ Deleting ALL contacts...\nPlease wait.")
    
    try:
        result = await client(GetContactsRequest(hash=0))
        contacts = result.users

        if not contacts:
            await event.reply("ℹ️ No contacts found.")
            return

        deleted = 0

        # delete in batches (safer)
        batch_size = 50
        for i in range(0, len(contacts), batch_size):
            batch = contacts[i:i + batch_size]
            try:
                await client(DeleteContactsRequest(id=batch))
                deleted += len(batch)
                await asyncio.sleep(2)  # anti flood
            except Exception as e:
                print(e)

        await event.reply(f"✅ Done. Deleted {deleted} contacts.")

    except Exception as e:
        await event.reply(f"❌ Error: {e}")


from telethon import TelegramClient, events
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.types import Channel, Chat
import asyncio

# ===== LEAVE ALL GROUPS =====
@client.on(events.NewMessage(pattern=r"\.groupleave$"))
async def leave_groups(event):
    await event.reply("⏳ Leaving all groups...")
    count = 0

    async for dialog in client.iter_dialogs():
        entity = dialog.entity

        # Group (basic group & supergroup)
        if isinstance(entity, Chat) or (
            isinstance(entity, Channel) and entity.megagroup
        ):
            try:
                await client(LeaveChannelRequest(entity))
                count += 1
                await asyncio.sleep(1.5)  # anti flood
            except Exception as e:
                print(e)

    await event.reply(f"✅ Done. Left {count} groups.")

# ===== LEAVE ALL CHANNELS =====
@client.on(events.NewMessage(pattern=r"\.channelleave$"))
async def leave_channels(event):
    await event.reply("⏳ Leaving all channels...")
    count = 0

    async for dialog in client.iter_dialogs():
        entity = dialog.entity

        # Channel only (not megagroup)
        if isinstance(entity, Channel) and not entity.megagroup:
            try:
                await client(LeaveChannelRequest(entity))
                count += 1
                await asyncio.sleep(1.5)  # anti flood
            except Exception as e:
                print(e)

    await event.reply(f"✅ Done. Left {count} channels.")

from telethon import events
import asyncio

@client.on(events.NewMessage(pattern=r"\.nayya"))
async def nayya(event):
    frames = [
        "👀",
        "👀 ᴇʜ",
        "👀👀 ᴇʜ ɴᴀʏʏᴀ",
        "👀👀 ɴᴀʏʏᴀ...",
        "👀❓ ɴᴀʏʏᴀ ᴍᴀsɪʜ ʜɪᴅᴜᴘ?",
        "📢👀 ʜᴀʟᴏ ᴛᴇs 1 2 3",
        "🚫📩 ɪɴɪ ʙᴜᴋᴀɴ sᴘᴀᴍ",
        "🎞️✨ ɪɴɪ ᴀɴɪᴍᴀsɪ",
        "👁️👁️ ᴋᴀʟᴏ ᴋᴇʙᴀᴄᴀ ʙᴇʀᴀʀᴛɪ sᴜᴋsᴇs",
        "🤷‍♂️📵 ᴋᴀʟᴏ ɢᴀ ᴋᴇʙᴀᴄᴀ ʏᴀ ɴᴀsɪʙ",
        "🧐📱 ɴᴀʏʏᴀ ʟᴀɢɪ ɴɢᴀᴘᴀɪɴ",
        "📱⬆️ sᴄʀᴏʟʟ ᴛɪᴋᴛᴏᴋ ʏᴀ?",
        "🙄💼 ᴀᴛᴀᴜ ᴘᴜʀᴀ-ᴘᴜʀᴀ sɪʙᴜᴋ",
        "🛌😴 ᴘᴀᴅᴀʜᴀʟ ʀᴇʙᴀʜᴀɴ",
        "🧠🌌 sᴀᴍʙɪʟ ᴍɪᴋɪʀ ʜɪᴅᴜᴘ",
        "😮‍💨🥲 ʜɪᴅᴜᴘ ᴇᴍᴀɴɢ ʙᴇʀᴀᴛ",
        "🔄😂 ᴛᴀᴘɪ ɪɴɪ ᴍᴀsɪʜ ʟᴀɴᴊᴜᴛ",
        "⌛👀 ʙᴇʟᴜᴍ sᴇʟᴇsᴀɪ",
        "😈👉 sᴀʙᴀʀ ᴅɪᴋɪᴛ",
        "⏳😏 ᴅɪᴋɪᴛ ʟᴀɢɪ",
        "🏁🤣 ᴏᴋ sᴇᴋᴀʀᴀɴɢ ʙᴀʀᴜ sᴇʟᴇsᴀɪ",
        "👍😎 ᴍᴀᴋᴀsɪʜ ɴᴀʏʏᴀ"
    ]

    msg = await event.respond(frames[0])
    last_text = frames[0]

    for _ in range(4):  # loop animasi
        for frame in frames:
            if frame != last_text:
                await asyncio.sleep(0.5)
                await msg.edit(frame)
                last_text = frame

from telethon import events
import asyncio

@client.on(events.NewMessage(pattern=r"\.hai"))
async def hai(event):
    if not event.is_reply:
        return await event.reply("❌ reply orang dulu woi")

    reply = await event.get_reply_message()
    name = reply.sender.first_name or "lu"
    name = name.lower()

    frames = [
        "👀",
        "👀 ᴇʜ",
        f"👀 ᴇʜ {name}",
        f"👀 {name}...",
        f"👀 {name} ᴅᴇɴɢᴇʀ ɢᴀ?",
        f"👀 {name} ᴊᴀɴɢᴀɴ ᴘᴀɴɪᴋ",
        "📢📢 ʜᴀʟᴏᴏᴏᴏ",
        "📢📢 ɪɴɪ ʙᴜᴋᴀɴ sᴘᴀᴍ",
        "🎞️✨ ɪɴɪ ᴀɴɪᴍᴀsɪ",
        "🧠⚙️ ʏᴀɴɢ ɴɢᴏᴅɪɴɢ ᴊᴜɢᴀ ᴍᴀɴᴜsɪᴀ",
        "👁️👁️ ᴊᴀᴅɪ ᴛᴏʟᴏɴɢ ᴅɪʙᴀᴄᴀ",
        "😌☕ ᴛᴀʀɪᴋ ɴᴀᴘᴀs",
        "😮‍💨☕ ʙᴜᴀɴɢ",
        "😈👉 ᴏᴋ ʟᴀɴᴊᴜᴛ",
        f"📱👀 {name} ʟᴀɢɪ ɴɢᴀᴘᴀɪɴ",
        "📱⬆️ sᴄʀᴏʟʟ ᴛɪᴋᴛᴏᴋ?",
        "🎮🔥 ᴍᴀɪɴ ɢᴀᴍᴇ?",
        "🛌😴 ʀᴇʙᴀʜᴀɴ?",
        "🙄💭 ᴀᴛᴀᴜ ᴍɪᴋɪʀɪɴ ʜɪᴅᴜᴘ",
        "🥲🧠 ʜɪᴅᴜᴘ ᴇᴍᴀɴɢ ʀɪʙᴇᴛ",
        "📉📈 ᴋᴀᴅᴀɴɢ ɴᴀɪᴋ ᴋᴀᴅᴀɴɢ ᴛᴜʀᴜɴ",
        "🫠🧠 ᴋᴀᴅᴀɴɢ ᴘᴇɴɢᴇɴ ʜɪʟᴀɴɢ",
        "😂👉 ᴛᴀᴘɪ ɢᴀ ʙɪsᴀ",
        f"😈🔥 {name} ᴍᴜʟᴀɪ ɴɢᴇʜ",
        "💀🤣 ɴᴀʜ ᴋᴀɴ",
        "⏳👀 ᴛᴇɴᴀɴɢ",
        "⏳👀 ɪɴɪ ᴍᴀsɪʜ ʙᴇʟᴜᴍ sᴇʟᴇsᴀɪ",
        "⏳👀 sᴀʙᴀʀ",
        "⏳👀 sᴀʙᴀʀ ʟᴀɢɪ",
        "😵‍💫🌀 ʙᴀᴄᴀ sᴀᴍᴘᴇ ʜᴀʙɪs",
        "😈🧪 ɪɴɪ ᴛᴇs ᴋᴇsᴀʙᴀʀᴀɴ",
        "🏁😎 ᴏᴋ sᴇᴋᴀʀᴀɴɢ ʙᴇɴᴇʀᴀɴ sᴇʟᴇsᴀɪ",
        f"👍🔥 ᴍᴀᴋᴀsɪʜ {name}"
    ]

    msg = await event.respond(frames[0])
    last_text = frames[0]

    for frame in frames[1:]:
        if frame != last_text:
            await asyncio.sleep(0.45)
            await msg.edit(frame)
            last_text = frame

import asyncio
from telethon import events 

# The roast stages using HTML bold tags
STAGES = [
    "🤬 <b>LU KONTOL!!!</b>",
    "👹 <b>LU EMANG ANAK KONTOL!</b>",
    "💀 <b>ANAK KONTOL, KONTOL BABI!</b>",
    "🔥 <b>SOKER LU KONTOL!</b>",
    "👿 <b>MATI AJA LU KONTOL!</b>",
    "🤢 <b>PANTAT LU DIMASUKIN KONTOL!</b>"
]

@client.on(events.NewMessage(pattern=r'\.toxic', outgoing=True))
async def toxic_destruction(event):
    if event.sender_id != OWNER_ID:
        return

    await event.delete()

    # Initial message with HTML parse mode enabled
    if event.is_reply:
        reply_to = await event.get_reply_message()
        msg = await reply_to.reply("🏁 <b>anjing</b>", parse_mode='html')
    else:
        msg = await event.respond("🏁 <b>anjing...</b>", parse_mode='html')

    for stage in STAGES:
        await asyncio.sleep(1.5)
        # We tell the bot to interpret <b> tags as bold
        await msg.edit(stage, parse_mode='html')

from telethon import events
import asyncio

# Gunakan variabel 'client' atau 'bot' sesuai dengan file utama kamu
@client.on(events.NewMessage(pattern=r"\.sg", outgoing=True))
async def sangmata_handler(event):
    # Mendapatkan pesan yang di-reply
    reply = await event.get_reply_message()
    
    if not reply:
        return await event.edit("`Reply ke orang yang ingin dicek history-nya!`")

    # Ambil ID orang yang di-reply
    target_id = reply.sender_id
    await event.edit(f"`🔎 Mengecek history untuk ID:` {target_id}...")

    bot_username = "@SangMata_BOT"

    try:
        async with client.conversation(bot_username) as conv:
            # Mengirim ID target ke SangMata
            await conv.send_message(f"allhistory {target_id}")
            
            # Menunggu jawaban dari bot
            response = await conv.get_response()
            await conv.mark_read()

            # Jika data tidak ada
            if "No records found" in response.text:
                await event.edit(f"❌ ID: `{target_id}`\n`Belum terdaftar di database SangMata.`")
            else:
                # Menghapus pesan ".sg" kamu dan mengirim hasil history
                await event.delete()
                hasil = f"**Riwayat Nama (History):**\n`ID: {target_id}`\n\n{response.text}"
                await client.send_message(event.chat_id, hasil)

            # Bersihkan chat dengan bot SangMata
            await client.delete_messages(bot_username, [response.id])

    except Exception as e:
        await event.edit(f"❌ Error: {str(e)} \n(Pastikan sudah klik START di @SangMata_BOT)")

import asyncio
from telethon import events

@client.on(events.NewMessage(pattern=r'\.editanim (.+)'))
async def edit_anim(event):
    # 1. Check if the sender is the owner
    if event.sender_id != OWNER_ID:
        return  # Silently ignore if someone else types it

    # 2. Delete the command message
    try:
        await event.delete()
    except Exception:
        pass

    text = event.pattern_match.group(1)
    msg = await event.respond(".") 

    current = ""
    for char in text:
        current += char
        await msg.edit(current)
        await asyncio.sleep(0.6) 

    await msg.edit(text)

from telethon import events
from telethon.tl.types import KeyboardButtonCallback
from telethon import TelegramClient, events
from telethon.tl.functions.messages import (
    GetInlineBotResultsRequest,
    SendInlineBotResultRequest
)

@client.on(events.NewMessage(pattern=r'\.catur'))
async def catur(event):
    if event.sender_id != OWNER_ID:
        return
    bot = await client.get_input_entity("gamefactorybot")

    # Step 1: Get inline results
    results = await client(GetInlineBotResultsRequest(
        bot=bot,
        peer=await event.get_input_chat(),
        query="chess",
        offset=""
    ))

    if not results.results:
        await event.reply("No inline results found")
        return

    # Step 2: Send FIRST inline result (game card)
    await client(SendInlineBotResultRequest(
        peer=await event.get_input_chat(),
        query_id=results.query_id,
        id=results.results[0].id
    ))

from telethon import TelegramClient, events
import re


@client.on(events.NewMessage(pattern=r'\.help'))
async def help_cmd(event):
    if event.sender_id != OWNER_ID:
        return  
    cmds = set()

    for handler in event.client._event_builders:
        if isinstance(handler, events.NewMessage):
            pattern = handler.pattern
            if not pattern:
                continue

            raw = pattern.pattern
            match = re.match(r'^\^?\\\.([a-zA-Z0-9_]+)', raw)
            if match:
                cmds.add(f".{match.group(1)}")

    if not cmds:
        await event.reply("No commands found")
        return

    await event.reply("**Commands:**\n" + "\n".join(sorted(cmds)))

from telethon import events
import asyncio
import re

active_seblink = {}  # Store running tasks


@client.on(events.NewMessage(pattern=r"\.seblink"))
async def seblink_cmd(event):
    raw = event.raw_text.split()

    # Remove .seblink
    raw = raw[1:]

    groups = []
    message_parts = []

    for word in raw:
        if word.startswith("@"):
            groups.append(word)
        else:
            message_parts.append(word)

    if not groups:
        return await event.reply("❗ Please include group usernames starting with @")

    final_message = " ".join(message_parts).strip()

    if not final_message:
        return await event.reply("❗ No message text found. Put your message BEFORE the @groups.")

    # Start tasks for each group
    for grp in groups:
        task = asyncio.create_task(send_loop(event, grp, final_message))
        active_seblink[grp] = task

    await event.reply(
        f"✅ Seblink started!\n"
        f"Message: *{final_message}*\n"
        f"Groups: {groups}\n"
        f"Interval: 30 seconds"
    )


async def send_loop(event, group, message):
    while True:
        try:
            await client.send_message(group, message, link_preview=False)
            await asyncio.sleep(45)
        except Exception as e:
            await event.reply(f"⚠ Error sending to {group}: {e}")
            break


@client.on(events.NewMessage(pattern=r"\.stopseblink"))
async def stop_seblink(event):
    if not active_seblink:
        return await event.reply("❗ No active seblink tasks running.")

    for grp, task in active_seblink.items():
        task.cancel()

    active_seblink.clear()
    await event.reply("🛑 All seblink loops stopped.")

from telethon import TelegramClient, events
import asyncio
import random


# smallcaps + emoticons
romantic_texts = [
    "floryn i love you ❤️",
    "floryn you’re amazing 😘",
    "floryn you make my heart smile 😊",
    "floryn thinking of you always 💭",
    "floryn my world is brighter with you 🌞",
    "floryn forever yours 💕",
    "floryn you are my sunshine ☀️",
    "floryn every moment with you is magic ✨",
    "floryn i cherish you 💖",
    "floryn you complete me 🫶",
    "floryn love you endlessly 💌",
    "floryn you are my everything 🌹",
    "floryn my heart beats for you 💓",
    "floryn my one and only 💎",
    "floryn you’re my dream come true 🌙"
]

# list emoji tambahan yang akan gonta-ganti di akhir
extra_emotes = ["😍","🥰","💘","💞","💗","💝","🫶","💖","💌","🌸","🌹"]

@client.on(events.NewMessage(pattern=r"\.floryn"))
async def floryn_animation(event):
    message = await event.reply("floryn ...")  # initial message
    
    for _ in range(5):  # repeat 5 times
        for text in random.sample(romantic_texts, len(romantic_texts)):
            # tambahkan emoji random dari list extra_emotes
            final_text = f"{text} {random.choice(extra_emotes)}"
            await message.edit(final_text.lower())  # smallcaps hardcoded
            await asyncio.sleep(1)  # jeda 1 detik



from telethon import TelegramClient, events
from telethon.tl.types import User
import asyncio

@client.on(events.NewMessage(pattern=r"\.allid(?:\s+(.+))?"))
async def allid_handler(event):
    target = event.pattern_match.group(1)

    if not target:
        await event.reply("❌ Usage:\n`.allid <group link | @username | group_id>`")
        return

    try:
        chat = await client.get_entity(target)
        msg = "📋 **Users who chatted:**\n\n"
        user_ids = set()  # avoid duplicates

        async for message in client.iter_messages(chat, limit=None):
            if message.sender_id and message.sender_id not in user_ids:
                user_ids.add(message.sender_id)
                sender = await message.get_sender()
                if isinstance(sender, User) and not sender.deleted:
                    name = f"@{sender.username}" if sender.username else sender.first_name
                    msg += f"{name} — `{sender.id}`\n"

            if len(msg) > 3500:  # Telegram max message limit
                await event.reply(msg)
                msg = ""

        if msg:
            await event.reply(msg)

        await event.reply(f"✅ Done. Total unique chatters: **{len(user_ids)}**")

    except Exception as e:
        await event.reply(f"❌ Error:\n`{str(e)}`")

from telethon import TelegramClient, events
import asyncio
import random
import os

# Personality + ciri khas (serius + lucu/kocak + toxic)
PERSONALITIES = {
    "Introvert": [
        "Suka merenung dan menikmati waktu sendiri",
        "Kadang ngomel sendiri tanpa alasan",
        "Suka tidur siang 5 jam tanpa rasa bersalah"
    ],
    "Ekstrovert": [
        "Enerjik dan senang bersosialisasi",
        "Bisa bicara nonstop sampai teman kabur",
        "Selalu rebut snack terakhir tanpa minta izin"
    ],
    "Ambivert": [
        "Seimbang antara ingin sendiri dan bersosialisasi",
        "Terkadang tiba-tiba menghilang tanpa kabar",
        "Bisa tertawa sendirian karena  konyol"
    ],
    "Pemimpi": [
        "Kreatif dan suka membayangkan kemungkinan baru",
        "Sering lupa makan karena terlalu asyik berkhayal",
        "Kadang ngomong ke tembok karena saking kreatifnya"
    ],
    "Pemimpin": [
        "Percaya diri dan mengambil inisiatif",
        "Kadang marah kalau orang lambat nge-respond chat",
        "Suka atur teman seperti sedang main game strategi"
    ],
    "Analitis": [
        "Memikirkan segala sesuatu dengan logika",
        "Bisa overthinking hal kecil sampai larut malam",
        "Kadang nyeletuk 'loh kok bisa gitu?' ke orang random"
    ],
    "Free Spirit": [
        "Menyukai kebebasan dan spontanitas",
        "Sering telat karena terlalu santai",
        "Kadang bikin onar kecil cuma untuk seru-seruan"
    ]
}

# Extra traits lucu/toxic
EXTRA_TRAITS = [
    "manja", "tengil", "nakal", "polos", "nyebelin",
    "centil", "santuy", "dramaqueen", "cuek", "gila humor",
    "pintar nyolot", "gemesin", "pemalas tapi lucu", "sok asik", "baik hati",
    "usil", "labil", "muka innocent tapi jahat", "bucin", "serba salah tapi lucu"
]

# Quotes tambahan sarkastik / candaan
QUOTES = [
    "Hidup ini terlalu singkat untuk jadi serius terus, kan?",
    "Kalau nggak bisa bikin semua happy, paling nggak bikin orang ngakak.",
    "Santai aja, dunia ini nggak bakal kelar cuma gara-gara kamu telat 5 menit.",
    "Kadang aku cuma mau ngilang, tapi eh, ketahuan juga.",
    "Jangan salahkan aku kalau aku terlalu jujur... atau terlalu sarkastik."
]

# Small caps mapping
SMALL_CAPS = str.maketrans(
    "abcdefghijklmnopqrstuvwxyz",
    "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
)

def to_small_caps(text):
    return text.lower().translate(SMALL_CAPS)

def generate_personality():
    key = random.choice(list(PERSONALITIES.keys()))
    trait = random.choice(PERSONALITIES[key])  # 1 ciri random
    extras = random.sample(EXTRA_TRAITS, 3)  # 3 sifat tambahan
    quote = random.choice(QUOTES)
    explanation = f"💎 {key.upper()} 💎\n• {trait}\n✨ Sifat tambahan: {', '.join(extras)}\n💬 Quote: {quote}"
    return explanation

@client.on(events.NewMessage(pattern=r'^\.cekpersonaliti$', outgoing=True))
async def cek_personal(event):
    # Owner check
    if event.sender_id != OWNER_ID:
        await event.reply("⚠ Hanya owner yang bisa pakai command ini.")
        return

    # Target: reply, mention, atau default sender
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        target = reply_msg.sender_id
    elif event.message.entities:
        mention = next((e for e in event.message.entities if e._class.name_ == "MessageEntityMention"), None)
        if mention:
            username = event.message.text[mention.offset:mention.offset+mention.length]
            target_entity = await client.get_entity(username)
            target = target_entity.id
        else:
            target = event.sender_id
    else:
        target = event.sender_id

    # Ambil user entity
    user_entity = await client.get_entity(target)
    personality_text = generate_personality()
    personality_text_sc = to_small_caps(personality_text)

    # Animasi small caps
    msg = await event.reply("Menganalisis kepribadian...")
    await asyncio.sleep(1.5)
    display = ""
    for c in personality_text_sc:
        display += c
        if len(display) % 10 == 0:
            await msg.edit(f"{display}")
            await asyncio.sleep(0.05)
    await msg.edit(f"{display}")

    # Kirim profile photo jika ada
    try:
        photo_path = await client.download_profile_photo(user_entity, file=os.path.join('/tmp', f'pfp_{user_entity.id}.jpg'))
        if photo_path:
            await client.send_file(event.chat_id, photo_path, caption=f"Foto profil: @{getattr(user_entity, 'username', '—')}")
            try:
                os.remove(photo_path)
            except:
                pass
    except Exception:
        pass  

from telethon import events
import asyncio

running = False

VARIASI = [
    "kasih faham bos bos bos bos bos",
    "ksih faham bos bos bos bos bos",
    "kasih fhm bos bos bos bos bos",
    "ksih fhm bos bos bos bos bos",
    "ksh fhm bos bos bos bos bos"
]

@client.on(events.NewMessage(pattern=r"\.kasihfaham"))
async def kasihfaham(event):
    global running

    # auto hapus command
    await event.delete()

    if "stop" in event.raw_text.lower():
        running = False
        return

    if running:
        return

    running = True
    i = 0

    while running:
        await event.client.send_message(
            event.chat_id,
            VARIASI[i % len(VARIASI)]
        )
        i += 1
        await asyncio.sleep(12)

from telethon import events
import asyncio
import random

running = False

SANTAI = [
    "hmm",
    "iya juga sih",
    "wkwk 😂",
    "nah itu",
    "kayaknya iya",
    "ok deh",
    "pelan-pelan aja",
    "😂😂",
    "gas dikit",
    "sebentar mikir"
]

SERIUS = [
    "kalau dipikir lebih dalam, sebenernya ada beberapa hal yang perlu dipertimbangkan",
    "menurut gue ini gak bisa diputusin buru-buru, perlu liat situasi juga",
    "gue paham maksudnya, tapi ada sisi lain yang kadang orang suka lupa",
    "secara logika sih ada benarnya, cuma implementasinya yang agak ribet",
    "ini sebenernya tergantung konteks, gak bisa disamain semua kondisi",
    "gue setuju sebagian, tapi gak sepenuhnya",
    "kalau liat jangka panjang, efeknya bisa beda",
    "menarik sih topiknya, bikin mikir lebih jauh",
    "gue gak bilang salah, cuma perlu dipikir ulang",
    "ada plus minusnya juga kalau jujur"
]

CAMPUR = [
    "jujur aja tadi ketawa sendiri tapi abis itu mikir juga 😂",
    "awalannya santai, tapi kok makin dipikir makin serius ya",
    "kayaknya sepele, tapi ternyata lumayan juga mikirinnya",
    "gue santai aja sih, tapi ada bagian yang bikin kepikiran",
    "tadi ketawa, sekarang malah mikir 😅"
]

@client.on(events.NewMessage(pattern=r"\.ngobrol"))
async def ngobrol(event):
    global running

    await event.delete()

    if "stop" in event.raw_text.lower():
        running = False
        return

    if running:
        return

    running = True

    while running:
        mode = random.choice(["santai", "serius", "campur"])

        if mode == "santai":
            teks = random.choice(SANTAI)
        elif mode == "serius":
            teks = random.choice(SERIUS)
        else:
            teks = random.choice(CAMPUR)

        await event.client.send_message(event.chat_id, teks)
        await asyncio.sleep(7)

from telethon import events, functions, types

@client.on(events.NewMessage(pattern=r'\.delrc(?:\s+(.*))?'))
async def delete_all_private_chats(event):
    # Mendapatkan argumen (ID yang dikecualikan)
    args = event.pattern_match.group(1)
    excluded_ids = []

    if args:
        # Memisahkan ID jika ada lebih dari satu, misal: .delrc @user 123456
        input_ids = args.split()
        for item in input_ids:
            try:
                # Resolve peer untuk mendapatkan ID asli jika input berupa username
                entity = await event.client.get_input_entity(item)
                if isinstance(entity, types.InputPeerUser):
                    excluded_ids.append(entity.user_id)
            except Exception:
                await event.edit(f"**Gagal mengenali ID/Username:** `{item}`")
                return

    await event.edit(f"**Memproses penghapusan semua chat pribadi...**\nKecuali: `{excluded_ids}`")

    deleted_count = 0
    async for dialog in event.client.iter_dialogs():
        # Cek jika dialog adalah Private Chat (User) dan bukan Bot
        if dialog.is_user and not dialog.entity.bot:
            user_id = dialog.entity.id
            
            # Jika ID ada di daftar pengecualian, lewati
            if user_id in excluded_ids:
                continue
            
            try:
                # Menghapus seluruh riwayat chat (untuk kedua belah pihak jika memungkinkan)
                await event.client(functions.messages.DeleteHistoryRequest(
                    peer=dialog.input_entity,
                    max_id=0,
                    revoke=True # Set True untuk menghapus di sisi lawan juga
                ))
                deleted_count += 1
            except Exception as e:
                print(f"Gagal menghapus chat dengan {user_id}: {e}")

    await event.respond(f"**Berhasil menghapus {deleted_count} chat pribadi.**")

import random
import asyncio
from telethon import events

def sc(text):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    sc_alphabet = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘqʀꜱᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘqʀꜱᴛᴜᴠᴡxʏᴢ0123456789"
    return text.translate(str.maketrans(alphabet, sc_alphabet))

@client.on(events.NewMessage(pattern=r'\.tobrut'))
async def tobrut_hardcore(event):
    if not event.is_reply:
        return await event.edit(sc(" ʀᴇᴘʟʏ ᴛᴀʀɢᴇᴛ ʏᴀɴɢ ᴍᴀᴜ ᴅɪ-sᴄᴀɴ!"))

    reply_msg = await event.get_reply_message()
    target = await event.client.get_entity(reply_msg.sender_id)
    name = target.first_name

    await event.edit(f"🔞 {sc('ᴍᴇᴍʙᴜᴋᴀ sᴇɴsᴏʀ sᴇɴsᴜɪʟ')}...")
    await asyncio.sleep(1)
    await event.edit(f"💦 {sc('ᴍᴇɴɢʜɪᴛᴜɴɢ ᴋᴇᴘᴀᴅᴀᴛᴀɴ')}...")
    await asyncio.sleep(1)

    diagnosa = [
        "ᴀsᴇᴛ ᴛɪɴɢᴋᴀᴛ ᴅᴇᴡᴀ, ʙɪᴋɪɴ ᴋᴏɴᴛᴏʟ ᴍᴇɴɢɢᴇʀᴀs sᴇᴋᴇᴊᴀᴘ ᴅᴀɴ ᴛɪsᴜ sᴇᴘᴀᴋ ʟᴀɴɢsᴜɴɢ ʟᴜɴɢsᴇ.",
        "ᴅᴇᴛᴇᴋsɪ ᴍᴇɴᴜɴᴊᴜᴋᴋᴀɴ ᴛᴇᴋsᴛᴜʀ ʏᴀɴɢ sᴀɴɢᴀᴛ sɪᴋᴜᴛ-ᴀʙʟᴇ, ᴘᴀs ʙᴀɴɢᴇᴛ ʙᴜᴀᴛ ᴅɪᴊᴀᴅɪᴋᴀɴ ʙᴀɴᴛᴀʟ sᴘᴇʀᴍᴀ.",
        "sᴜsᴜ ʙʀᴜᴛᴀʟ ʏᴀɴɢ ʙɪsᴀ ᴍᴇɴɢᴀʟɪʜᴋᴀɴ ᴅᴜɴɪᴀ sᴇʟᴜʀᴜʜ ᴘᴇᴊᴀɴᴛᴀɴ ᴄᴏʟɪ sᴇ-ᴋᴇᴄᴀᴍᴀᴛᴀɴ.",
        "ᴛᴇʀᴅᴇᴛᴇᴋsɪ ᴀsᴇᴛ ᴍᴇɴᴏɴᴊᴏʟ ʏᴀɴɢ sɪᴀᴘ ᴅɪᴀᴄᴀᴋ-ᴀᴄᴀᴋ, ʙɪᴋɪɴ ᴘɪᴋɪʀᴀɴ ᴋᴏᴛᴏʀ ᴍᴇʟᴜᴀᴘ sᴀᴍᴘᴀɪ ᴋᴇ ᴜʙᴜɴ-ᴜʙᴜɴ.",
        "ᴋᴀᴛᴇɢᴏʀɪ ʙᴏɴɢsᴏʀ ᴅᴀɴ ᴋᴇɴʏᴀʟ, sᴀɴɢᴀᴛ ʟᴀʏᴀᴋ ᴜɴᴛᴜᴋ ᴅɪᴛᴜᴍᴘᴀʜɪ ᴄᴀɪʀᴀɴ ᴘᴇʀᴊᴜᴀɴɢᴀɴ sᴇᴛɪᴀᴘ ᴍᴀʟᴀᴍ.",
        "ᴛɪɴɢᴋᴀᴛ ᴋᴇᴍᴏɴᴛᴏᴋᴀɴ ʟᴇᴠᴇʟ ɪʙʟɪs, ʙɪᴋɪɴ ɪᴍᴀɴ ʀᴏɴᴛᴏᴋ ᴅᴀɴ ᴛᴀɴɢᴀɴ ᴏᴛᴏᴍᴀᴛɪs ᴍᴇɴɢᴏᴄᴏᴋ ᴛᴀɴᴘᴀ sᴀᴅᴀʀ.",
        "ᴀsᴇᴛ ᴛᴇʀʟᴀʟᴜ ᴛᴇᴘᴏs ᴅᴀɴ ᴛɪᴅᴀᴋ ʙᴇʀɢɪᴢɪ.",
        "ᴍᴜʟᴜs, ʙᴇsᴀʀ, ᴅᴀɴ ᴍᴇɴᴀɴᴛᴀɴɢ. sᴇᴛɪᴀᴘ ɢᴇᴛᴀʀᴀɴɴʏᴀ ᴀᴅᴀʟᴀʜ ᴘᴀɴɢɢɪʟᴀɴ ᴜɴᴛᴜᴋ sᴇɢᴇʀᴀ ᴍᴇɴᴜɴᴛᴀsᴋᴀɴ ʜᴀsʀᴀᴛ.",
        "ᴅᴇғɪɴɪsɪ ᴛᴏʙʀᴜᴛ ᴘᴇᴍᴇʀᴀs ʙᴀᴛᴀɴɢ, ᴜᴋᴜʀᴀɴɴʏᴀ ʙɪᴋɪɴ sᴇsᴀᴋ ɴᴀᴘᴀs ᴅᴀɴ sᴇʟᴀɴɢᴋᴀɴɢᴀɴ ʙᴀsᴀʜ ᴋᴜʏᴜᴘ.",
        "ɢᴜɴᴜɴɢ ᴋᴇᴍʙᴀʀ ʏᴀɴɢ sᴀɴɢᴀᴛ ᴇᴋsᴘʟɪsɪᴛ, ᴍᴇɴᴜɴᴛᴜᴛ ᴜɴᴛᴜᴋ ᴅɪᴊᴇʟᴀᴊᴀʜɪ ᴅᴇɴɢᴀɴ ᴘᴇɴᴜʜ ᴋᴇʙᴇʀɪᴀsᴀɴ."
    ]

    vibe = [
        "ʟᴏɴᴛᴇ sɪᴍᴘᴀɴᴀɴ", "ᴘᴇᴍᴜsɴᴀʜ sᴀʙᴜɴ", "ʙɪɴɪ ᴏʀᴀɴɢ ᴠɪʙᴇs", 
        "ᴘᴇᴍᴀɴs ʜᴀʀᴅᴄᴏʀᴇ", "ɢᴀᴅɪs ᴄᴏʟɪ-ᴀʙʟᴇ", "ᴍᴇsɪɴ ᴘᴇɴʏᴇᴅᴏᴛ ᴘᴇʟᴜʜ"
    ]

    skor = random.randint(10, 100)
    res_vibe = random.choice(vibe)
    res_diag = random.choice(diagnosa)

    output = (
        f"**🔞 {sc('ʟᴀᴘᴏʀᴀɴ')} 🔞**\n"
        f"--- --- --- --- --- --- ---\n"
        f"{sc('ᴏʙᴊᴇᴋ sᴄᴀɴ')}: [{name}](tg://user?id={target.id})\n"
        f"{sc('sᴋᴏʀ ᴛᴏʙʀᴜᴛ')}: {skor}% \n"
        f"{sc('ᴋᴀᴛᴇɢᴏʀɪ')}: `{sc(res_vibe)}`\n"
        f"{sc('ᴅɪᴀɢɴᴏsᴀ ʙᴇᴊᴀᴛ')}: \n`{sc(res_diag)}`\n"
        f"--- --- --- --- --- --- ---\n"
    )

    await event.edit(output)

import random
import asyncio
from telethon import events

# Fungsi pembantu untuk mengubah teks menjadi Small Caps
def sc(text):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    sc_alphabet = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘqʀꜱᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘqʀꜱᴛᴜᴠᴡxʏᴢ0123456789"
    return text.translate(str.maketrans(alphabet, sc_alphabet))

@client.on(events.NewMessage(pattern=r'\.k'))
async def k_brutal(event):
    if not event.is_reply:
        return await event.edit(sc("ɢᴀɢᴀʟ: ʀᴇᴘʟʏ ʟᴏɴᴛᴇ ʏᴀɴɢ ᴍᴀᴜ ᴅɪ-ʙᴇʟᴀʜ ᴍᴇᴍᴇᴋɴʏᴀ!"))

    reply_msg = await event.get_reply_message()
    
    try:
        target = await event.client.get_entity(reply_msg.sender_id)
    except Exception:
        return await event.edit(sc("ɢᴀɢᴀʟ"))
        
    name = target.first_name

    # Animasi Loading Brutal
    await event.edit(f"🔞 {sc('ᴍᴇᴍᴀsᴀɴɢ ᴋᴀᴍᴇʀᴀ ᴘᴇɴɢɪɴᴛᴀɪ sᴇʟᴀɴɢᴋᴀɴɢᴀɴ')}...")
    await asyncio.sleep(1)
    await event.edit(f"💦 {sc('ᴍᴇɴᴅᴇᴛᴇᴋsɪ ᴀʀᴏᴍᴀ ᴅᴀɴ ʟᴇɴᴅɪʀ ᴠᴇɴᴀ sʏᴀʜᴡᴀᴛ')}...")
    await asyncio.sleep(1)

    # Database Diagnosa - Level Brutal
    diagnosa = [
        "ᴍᴇᴍᴇᴋ ʟᴇʙᴀᴛ ʙᴇʀᴅᴇɴɢʏᴜᴛ ɴᴀᴋᴀʟ, sɪᴀᴘ ᴍᴇɴᴊᴇᴘɪᴛ ʙᴀᴛᴀɴɢ sᴀᴍᴘᴀɪ ᴍᴜɴᴄʀᴀᴛ sᴘᴇʀᴍᴀ ʙᴇʀᴋᴀʟɪ-ᴋᴀʟɪ.",
        "ʟᴏʙᴀɴɢ ɴɪᴋᴍᴀᴛ ᴘᴇɴʏᴇᴅᴏᴛ ᴘᴇʟᴜʜ, sᴀɴɢᴀᴛ ʙᴇᴄᴇᴋ ᴅᴀɴ ʙᴇᴘᴇᴋ ʜɪɴɢɢᴀ ʙɪᴋɪɴ sᴇʟᴀɴɢᴋᴀɴɢᴀɴ ʟᴇᴘᴏᴛᴀɴ.",
        "ʙᴇɴᴛᴜᴋ ᴛᴇᴍʙᴇᴍ ᴍᴇɴᴀɴᴛᴀɴɢ, ᴅɪᴘʀᴇᴅɪᴋsɪ sᴀɴɢᴀᴛ ɢᴜʀɪʜ ᴜɴᴛᴜᴋ ᴅɪᴋᴏᴄᴏᴋ ᴘᴀᴋᴀɪ ᴋᴏɴᴛᴏʟ ʙᴇʀᴜʀᴀᴛ sᴀᴍᴘᴀɪ ᴋᴇʟᴏᴊᴏᴛᴀɴ.",
        "ᴛᴇʀᴅᴇᴛᴇᴋsɪ ʟᴏʙᴀɴɢ ʏᴀɴɢ ʜᴀᴜs sᴇᴍᴘᴏʀᴛᴀɴ ᴍᴀɴɪ, sɪᴀᴘ ᴅɪᴛᴜsᴜᴋ ʙʀᴜᴛᴀʟ sᴀᴍᴘᴀɪ ᴅᴇsᴀʜ ᴀᴍᴘᴜɴ-ᴀᴍᴘᴜɴᴀɴ.",
        "ᴍᴇᴍᴇᴋ ᴘɪɴᴋʏ ᴍᴜʟᴜs ᴋᴇɴʏᴀʟ, sᴇᴛɪᴀᴘ ᴊɪʟᴀᴛᴀɴ ᴀᴋᴀɴ ᴍᴇɴɢᴇʟᴜᴀʀᴋᴀɴ ᴄᴀɪʀᴀɴ ᴋᴇɴɪᴋᴍᴀᴛᴀɴ ʏᴀɴɢ ᴍᴇʟᴜᴘᴀʜ.",
        "ᴋᴏɴᴅɪsɪ ʙᴇᴄᴇᴋ ᴘᴀʀᴀʜ, sɪᴀᴘ ᴅɪᴊᴀᴅɪᴋᴀɴ ᴛᴇᴍᴘᴀᴛ ᴘᴇᴍʙᴜᴀɴɢᴀɴ sᴘᴇʀᴍᴀ ᴍᴀssᴀʟ ᴘᴀʀᴀ ᴘᴇᴊᴀɴᴛᴀɴ sᴀɴɢɴɢᴇ.",
        "ᴛᴇʀʟᴀʟᴜ ʟᴏɴɢɢᴀʀ sᴇᴘᴇʀᴛɪ ɢᴏᴀ ʜᴀɴᴛᴜ, ʙᴜᴛᴜʜ ʙᴀᴛᴀɴɢ ᴋᴜᴅᴀ ᴜɴᴛᴜᴋ ʙɪsᴀ ᴍᴇɴʏᴇɴᴛᴜʜ ᴅɪɴᴅɪɴɢ ʀᴀʜɪᴍɴʏᴀ.",
        "ᴊᴇᴘɪᴛᴀɴ sᴇᴛᴀɴ ʏᴀɴɢ ᴍᴇᴍᴀᴛɪᴋᴀɴ, sᴇ sekali ᴍᴀsᴜᴋ ᴏᴛᴏᴍᴀᴛɪs ᴋᴇʟᴜᴀʀ ᴅᴀʟᴀᴍ ʜɪᴛᴜɴɢᴀɴ ᴅᴇᴛɪᴋ ᴋᴀʀᴇɴᴀ ᴛᴇʀʟᴀʟᴜ ᴇɴᴀᴋ.",
        "ʙɪʙɪʀ ᴍᴇᴍᴇᴋ ʏᴀɴɢ ᴊᴇʙᴇʀ ᴅᴀɴ ʙᴇʀɢᴀɪʀᴀʜ, sᴀɴɢᴀᴛ ᴄᴏᴄᴏᴋ ᴜɴᴛᴜᴋ ᴅɪᴛᴀᴍᴘᴀʀ ᴘᴀᴋᴀɪ ᴋᴇᴘᴀʟᴀ ᴋᴏɴᴛᴏʟ sᴀᴍᴘᴀɪ ᴍᴇʀᴀɴɢsᴀɴɢ.",
        "ᴀsᴇᴛ ʙᴀᴡᴀʜ ᴘᴇɴᴅᴏsᴀ ʏᴀɴɢ sɪᴀᴘ ᴅɪɢᴇʟᴏʀᴀᴋᴀɴ ᴅᴇɴɢᴀɴ sᴏᴅᴏᴋᴀɴ ᴍᴀᴜᴛ ᴛᴀɴᴘᴀ ᴀᴍᴘᴜɴ sᴇᴍᴀʟᴀᴍ sᴜɴᴛᴜᴋ."
    ]

    vibe = [
        "ʟᴏɴᴛᴇ ᴄᴏʟɪ-ᴀʙʟᴇ", "ᴍᴇsɪɴ ᴘᴇʀᴇᴍᴇs ʙᴀᴛᴀɴɢ", "ɢᴜᴀ ʟᴇɴᴅɪʀ", 
        "ᴘᴇᴍᴀɴs sᴘᴇʀᴍᴀ", "ᴊᴀʟᴀɴɢ ʙᴇᴄᴇᴋ ", "ᴘᴇɴʏᴇᴅᴏᴛ"
    ]

    skor = random.randint(30, 100)
    res_vibe = random.choice(vibe)
    res_diag = random.choice(diagnosa)

    # Output Final Brutal
    output = (
        f"**🔞 {sc('ʟᴀᴘᴏʀᴀɴ')} 🔞**\n"
        f"--- --- --- --- --- --- ---\n"
        f"👤 {sc('ᴛᴀʀɢᴇᴛ')}: [{name}](tg://user?id={target.id})\n"
        f"🔥 {sc('ᴋᴇʙᴇᴄᴇᴋᴀɴ ʟᴏʙᴀɴɢ')}: {skor}% \n"
        f"🎭 {sc('sᴛᴀᴛᴜs')}: `{sc(res_vibe)}`\n"
        f"📝 {sc('ᴀɴᴀʟɪsɪs ʙᴇᴊᴀᴛ')}: \n`{sc(res_diag)}`\n"
        f"--- --- --- --- --- --- ---\n"
        f"😈 _{sc('sɪᴀᴘᴋᴀɴ ᴀᴍᴜɴɪsɪ ᴍᴀɴɪ ᴀɴᴅᴀ ᴅᴀɴ sɪᴋᴀᴛ ᴛᴀɴᴘᴀ ᴀᴍᴘᴜɴ')}_"
    )

    await event.edit(output)

from telethon import events
from telethon.tl.types import User
import asyncio
from telethon.errors import MessageNotModifiedError

@client.on(events.NewMessage(pattern=r"\.leave"))
async def fake_leave(event):
    # auto delete command
    await event.delete()

    chat = await event.get_chat()

    # tentukan nama (group / user)
    if isinstance(chat, User):
        group_name = chat.first_name or "pengguna ini"
    else:
        group_name = chat.title or "grup ini"

    msg = await event.client.send_message(
        event.chat_id,
        "ᴍᴇᴍᴘʀᴏꜱᴇꜱ ᴋᴇʟᴜᴀʀ"
    )

    dots = ["", ".", "..", "..."]
    last_text = ""

    for _ in range(2):  # durasi proses
        for d in dots:
            teks = f"ᴍᴇᴍᴘʀᴏꜱᴇꜱ ᴋᴇʟᴜᴀʀ{d}"

            if teks != last_text:
                await asyncio.sleep(1)
                try:
                    await msg.edit(teks)
                    last_text = teks
                except MessageNotModifiedError:
                    pass  # abaikan error telegram

    await asyncio.sleep(1)
    try:
        await msg.edit(
            f"✅ ʙᴇʀʜᴀꜱɪʟ ᴋᴇʟᴜᴀʀ ᴅᴀʀɪᴘᴀᴅᴀ {group_name}"
        )
    except MessageNotModifiedError:
        pass

from telethon import events
from telethon.tl.types import MessageEntityMention, MessageEntityMentionName
import random

autorep_on = False

PENDEK = [
    "iya?",
    "ya?",
    "kenapa?",
    "ada apa?",
    "hai",
    "hm?",
    "oi",
    "iya kenapa",
    "apa?",
    "kenapa tuh"
]

SEDERHANA = [
    "iya kenapa?",
    "hai, ada apa?",
    "kenapa bro?",
    "ada apa ya?",
    "iya manggil?",
    "kenapa tag gue?",
    "iya gue baca",
    "apa yang bisa?",
    "kenapa tuh bro?",
    "iya ada apa"
]

NATURAL = [
    "iya, kenapa? ada apa?",
    "hai, kenapa manggil?",
    "ada apa ya? bilang aja",
    "kenapa? gue denger kok",
    "iya bro, ada apa?",
    "hai, mau nanya apa?",
    "kenapa tuh? jelasin dikit",
    "iya gue di sini",
    "ada masalah apa?",
    "kenapa tag gue?"
]

@client.on(events.NewMessage(pattern=r"\.autorep"))
async def autorep_cmd(event):
    global autorep_on
    # auto delete command
    await event.delete()

    if "stop" in event.raw_text.lower():
        autorep_on = False
        return

    autorep_on = True

@client.on(events.NewMessage)
async def autorep(event):
    global autorep_on

    if not autorep_on:
        return

    me = await event.client.get_me()

    # cek reply ke bot
    is_reply_to_bot = False
    if event.is_reply:
        reply = await event.get_reply_message()
        if reply and reply.sender_id == me.id:
            is_reply_to_bot = True

    # cek tag bot
    is_tagged = False
    if event.message.entities:
        for e in event.message.entities:
            if isinstance(e, (MessageEntityMention, MessageEntityMentionName)):
                if me.username and f"@{me.username.lower()}" in event.raw_text.lower():
                    is_tagged = True

    if not (is_reply_to_bot or is_tagged):
        return

    mode = random.choice(["pendek", "sederhana", "natural"])

    if mode == "pendek":
        teks = random.choice(PENDEK)
    elif mode == "sederhana":
        teks = random.choice(SEDERHANA)
    else:
        teks = random.choice(NATURAL)

    await event.reply(teks)

ghosted_users = set()

from telethon import TelegramClient, events

def luxury(text: str) -> str:
    """Convert normal text to luxury small caps."""
    normal = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    luxury = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return text.translate(str.maketrans(normal, luxury))

@client.on(events.NewMessage(pattern=r"\.ghost(?:\s+(.+))?"))
async def ghost_user(event):
    if not event.is_private:
        return await event.reply(luxury("This command only works in private chats ✨"))
    
    target = event.pattern_match.group(1)
    user = None

    if event.is_reply:
        reply = await event.get_reply_message()
        user = await reply.get_sender()
    elif target:
        try:
            user = await client.get_entity(target)
        except:
            return await event.reply(luxury("Could not find that user ⚠"))
    else:
        return await event.reply(luxury("Reply or tag a user to ghost 👻"))

    ghosted_users.add(user.id)
    await event.reply(luxury(f"Ghost activated 👻\nMessages from {user.first_name} will be silently deleted for you."))
    await event.delete()

@client.on(events.NewMessage(pattern=r"\.unghost(?:\s+(.+))?"))
async def unghost_user(event):
    if not event.is_private:
        return await event.reply(luxury("This command only works in private chats ✨"))
    
    target = event.pattern_match.group(1)
    user = None

    if event.is_reply:
        reply = await event.get_reply_message()
        user = await reply.get_sender()
    elif target:
        try:
            user = await client.get_entity(target)
        except:
            return await event.reply(luxury("Could not find that user ⚠"))
    else:
        return await event.reply(luxury("Reply or tag a user to unghost 🌙"))

    ghosted_users.discard(user.id)
    await event.reply(luxury(f"Ghost deactivated 💫\nMessages from {user.first_name} will no longer be deleted."))
    await event.delete()

@client.on(events.NewMessage())
async def auto_delete(event):
    if not event.is_private:
        return
    if event.sender_id in ghosted_users:
        await event.delete()

import random
import asyncio
from telethon import events

@client.on(events.NewMessage(pattern=rf"^{PREFIX}cjelek"))
async def setoxic(event):
    if event.sender_id != OWNER_ID:
        return

    # Ambil nama target
    if event.is_reply:
        reply = await event.get_reply_message()
        if reply.sender:
            name = reply.sender.first_name
        else:
            name = "Orang ini"
    else:
        me = await event.client.get_me()
        name = me.first_name

    # Small caps converter
    def small_caps(text):
        normal = "abcdefghijklmnopqrstuvwxyz"
        small = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
        table = str.maketrans(normal + normal.upper(), small + small.upper())
        return text.translate(table)

    # Animasi proses cek jelek
    steps = [
        "🔍 riksa fitur jelek...",
        "🧪 menilai level keburukan wajah...",
        "💀 menghitung skor ngentod jelek parah...",
        "⚠ menyiapkan persen toxic..."
    ]

    msg = await event.reply(small_caps(f"💀 sedang cek jelek {name}..."))

    for step in steps:
        await asyncio.sleep(1.2)
        await msg.edit(small_caps(step))

    # Random persen jelek/toxic
    percent = random.randint(80, 100)

    # Daftar komentar toxic panjang
    toxic_comments = [
        "ngeliat lu bikin gue pengen nangis seharian, jelek bgt ngentod",
        "jelek bgt lu sampe kucing tetangga juga kabur liat muka lu",
        "wajah lu itu definisi kegagalan visual, seriusan ngentod",
        "parah sih lu, jelek minta ampun, semua orang ngakak liat lu",
        "jelek level dewa, ngentod, jangan sampe ada orang jatuh cinta sama lu",
        "ngeliat lu bikin gue trauma seumur hidup, jelek bgt tolol",
        "goblok banget jeleknya, ngentod, muka lu sampe bikin trauma",
        "jeleknya luar biasa, sekelas monster tapi masih manusia",
        "lu itu definisi 'jelek parah', ngentod, jangan muncul di publik",
        "bener-bener jelek bgt, ngentod, semua orang bakal ngehindar"
    ]
    comment = random.choice(toxic_comments)

    # Hasil akhir
    result = f"💀  {small_caps('JELEK BGT NGENTOD')} {small_caps(name)}: {percent}%\n🗯  {small_caps(comment)} 💀"

    # Tampilkan hasil akhir
    await asyncio.sleep(1.5)
    await msg.edit(result)

from telethon import events
import asyncio

@client.on(events.NewMessage(pattern=r'\.tagall(?: |$)(.*)'))
async def tagall_reply_to_target(event):
    if event.is_private:
        return await event.reply("❌ Hanya bisa di grup!")

    # ambil pesan teks setelah .tagall
    msg = event.pattern_match.group(1) or "🔥 Semua sini dulu!"
    reply_target = await event.get_reply_message()  # pesan yang direply

    if not reply_target:
        return await event.reply("⚠ Balas ke pesan seseorang dulu baru ketik .tagall.")

    mentions = []
    total = 0
    chat = await event.get_input_chat()

    await event.reply("🔍 Mengambil daftar member...")

    try:
        async for user in client.iter_participants(chat):
            if user.bot or not user.first_name:
                continue

            tag = f"[{user.first_name}](tg://user?id={user.id})"
            mentions.append(tag)
            total += 1

            # kirim setiap 5 mention biar aman dari spam flood
            if len(mentions) == 5:
                text = f"{msg}\n\n" + " ".join(mentions)
                await reply_target.reply(text, link_preview=False)
                mentions = []
                await asyncio.sleep(2)

        # sisa terakhir
        if mentions:
            text = f"{msg}\n\n" + " ".join(mentions)
            await reply_target.reply(text, link_preview=False)

        await event.reply(f"✅ Tagall selesai! Total {total} member ditandai, semua balas ke pesan target.")

    except Exception as e:
        await event.reply(f"⚠ Error: {e}")

from telethon import TelegramClient, events
import asyncio
import random
# -----------------------------
# FORMAT NOMINAL
# -----------------------------
def format_nominal(n):
    if n < 1000:
        return f"{n} perak"
    return f"Rp {n:,}".replace(",", ".")

# -----------------------------
# VARIAN TEMA
# -----------------------------
themes = [
    ("💎 SISTEM TRANSFER DIAMOND INDONESIA 💎", "Perisai Diamond-Class v12.4"),
    ("✨ PROTOKOL EMAS NUSANTARA ✨", "Firewall Auric Imperial v9.8"),
    ("🌌 TRANSFER CYBERPUNK NEO-JAKARTA 🌌", "NeonNet CyberCore v6.6")
]

# BANK INDONESIA (FANTASI SUPER LUXURY)
banks = [
    "BCA Diamond Premier",
    "BRI Galaxy Signature",
    "Mandiri Quantum+",
    "BNI Emerald Raya",
    "CIMB Niaga HyperNova",
    "Danamon Royal Core",
    "BTN Stellar Shield"
]

# -----------------------------
# HANDLER COMMAND
# -----------------------------
@client.on(events.NewMessage(pattern=r"\.tf (\d+)(?: (\S+))?"))
async def transfer_mewah(event):
    jumlah = int(event.pattern_match.group(1))
    receiver_manual = event.pattern_match.group(2)

    # Nama pengirim otomatis
    me = await client.get_me()
    pengirim = me.first_name

    # Auto penerima jika reply
    if event.is_reply:
        rep = await event.get_reply_message()
        if rep.sender_id:
            penerima = f"<a href='tg://user?id={rep.sender_id}'>{rep.sender.first_name}</a>"
        else:
            penerima = "Tidak diketahui"
    else:
        penerima = receiver_manual or "Tidak diketahui"

    formatted = format_nominal(jumlah)

    # Random tema & bank
    judul_tema, proteksi = random.choice(themes)
    bank = random.choice(banks)
    norek = f"{random.randint(1000000000, 9999999999)}"
    saldo_fake = f"Rp {random.randint(10_000_000, 900_000_000):,}".replace(",", ".")

    # -----------------------------
    # ANIMASI LUXURY INDONESIA
    # -----------------------------
    msg = await event.reply(f"{judul_tema}\n🌐 Menginisialisasi jalur transaksi premium...")
    await asyncio.sleep(1.4)

    await msg.edit("🔍 Memverifikasi identitas pengirim...\n🔸 Memindai biometrik digital...")
    await asyncio.sleep(1.6)

    await msg.edit(f"👤 Pengirim Diverifikasi: {pengirim}\n🔐 Mengaktifkan segel keamanan tingkat nasional...")
    await asyncio.sleep(1.5)

    await msg.edit(f"🏦 Menghubungkan ke {bank}...\n💳 Nomor Rekening: {norek}")
    await asyncio.sleep(1.6)

    await msg.edit("💼 Menghubungkan node vault keuangan tingkat tinggi...")
    await asyncio.sleep(1.5)

    await msg.edit("🌌 Mengirim paket transaksi melalui jaringan satelit Nusantara...")
    await asyncio.sleep(1.5)

    await msg.edit(f"🔒 Lapisan Keamanan Aktif: {proteksi}\n🧬 Menstabilkan partikel enkripsi...")
    await asyncio.sleep(1.6)

    await msg.edit("💳 Menyelesaikan sinkronisasi antar-bank nasional...")
    await asyncio.sleep(1.4)

    # -----------------------------
    # OUTPUT LUXURY SUPER MEWAH
    # -----------------------------
    hasil = f"""
{judul_tema}
━━━━━━━━━━━━━━━━━━━━━━

👑 Pengirim: {pengirim}
🎁 Penerima: {penerima}

🏦 Bank: {bank}
💳 Rekening: {norek}
💼 Saldo Saat Ini: {saldo_fake}

💰 Jumlah Transfer: {formatted}
🔐 Keamanan: {proteksi}
🚀 Status: BERHASIL – Ultra Aman

🕒 Durasi: 0.0019 detik  
📡 Routing: Satelit Nusantara VII  
🌙 Integritas: 100% Stabil

━━━━━━━━━━━━━━━━━━━━━━
💎 Terima kasih telah menggunakan Sistem Transfer Premium Indonesia
"""

    await msg.edit(hasil, parse_mode="html")


@client.on(events.NewMessage(pattern=r'^\.setmode (\w+)$', outgoing=True))
async def setmode_handler(event):
    global current_mode

    sender = await event.get_sender()
    if sender.id != OWNER_ID:
        return

    mode = event.pattern_match.group(1).lower()
    if mode not in ["indo", "english", "chinese"]:
        await event.reply("⚙ available modes: indo / english / chinese")
        return

    current_mode = mode
    save_mode(mode)

    # ----- LUXURY OUTPUT -----
    emoji = "🌐"
    label = "Mode updated to"

    # Apply smallcaps only once here
    def safe_smallcaps(text):
        # If text already contains smallcaps letters, skip conversion
        if any(ord(c) > 127 for c in text):
            return text
        return to_smallcaps(text)

    label_smallcaps = safe_smallcaps(label)
    mode_text = f"{mode}"  # monospace, untouched

    text = f"💠 {emoji} {label_smallcaps} {mode_text} 💠"
    await event.reply(text, link_preview=False)

from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
from datetime import datetime

@client.on(events.NewMessage(pattern=r'^\.whois(?:\s+.+)?$', outgoing=True))
async def whois_handler(event):
    sender = await event.get_sender()
    if sender.id != OWNER_ID:
        return  # Silent untuk non-owner

    args = event.message.text.split()[1:] if len(event.message.text.split()) > 1 else []
    targets = []

    # Jika reply ke user
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        targets.append(reply.sender_id)

    # Parse argumen (username / ID)
    for arg in args:
        if arg.startswith("@"):
            try:
                user = await client.get_entity(arg)
                targets.append(user.id)
            except:
                pass
        elif arg.isdigit():
            targets.append(int(arg))

    # Jika tidak ada target, pakai diri sendiri
    if not targets:
        targets.append(sender.id)

    results = []
    for uid in targets:
        try:
            user_full = await client(GetFullUserRequest(uid))
            u = user_full.user

            name = f"{u.first_name or ''} {u.last_name or ''}".strip()
            username = f"@{u.username}" if u.username else "—"
            bio = user_full.about or "—"
            photo_count = u.profile_photo_count or 0
            date = datetime.now().strftime("%d %b %Y")

            result = (
                f"👤 ɴᴀᴍᴇ: *{name}*\n"
                f"🆔 ɪᴅ: {u.id}\n"
                f"🌐 ᴜsᴇʀɴᴀᴍᴇ: {username}\n"
                f"📸 ᴘʜᴏᴛᴏs: {photo_count}\n"
                f"💬 ʙɪᴏ: {bio}\n"
                f"🕓 ᴅᴀᴛᴇ: *{date}*\n"
            )
            results.append(result)
        except Exception as e:
            results.append(f"⚠ ғᴀɪʟᴇᴅ ᴛᴏ ɢᴇᴛ ᴜsᴇʀ: {uid}")

    msg = "\n━━━━━━━━━━━━━━━\n".join(results)
    msg += f"\n\nᴍᴀᴅᴇ ʙʏ {OWNER_USERNAME}"

    await event.edit(msg, link_preview=False)

from telethon import TelegramClient, events
from telethon.tl.custom.message import Message
from pypinyin import lazy_pinyin
import json

# ---------------- .ID HANDLER ---------------- #
@client.on(events.NewMessage(pattern=r'^\.id(?:\s+(@\w+))?$', outgoing=True))
async def id_handler(event):
    sender = await event.get_sender()

    # Only owner can use
    if sender.id != OWNER_ID:
        return

    # Determine target: reply, username, or self
    input_username = event.pattern_match.group(1)
    if input_username:
        try:
            user = await client.get_entity(input_username)
        except:
            await event.reply("⚠ User not found.")
            return
    elif event.reply_to_msg_id:
        reply_msg = await event.get_reply_message()
        user = await reply_msg.get_sender()
    else:
        user = sender

    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    username = f"@{user.username}" if user.username else "—"
    mention = f"[{full_name}](tg://user?id={user.id})"

    # Translate labels according to mode
    name_label = to_smallcaps(await translate_label("Name"))
    id_label = to_smallcaps(await translate_label("ID"))
    username_label = to_smallcaps(await translate_label("Username"))
    made_by_label = to_smallcaps(await translate_label("Made by"))

    # Build luxury text
    text = (
        f" 𝙿𝚁𝙾𝙵𝙸𝙻𝙴 𝙸𝙽𝙵𝙾 \n"
        f" {name_label}: {mention}\n"
        f" {id_label}: {user.id}\n"
        f" {username_label}: {username}\n\n"
        f" {made_by_label} [@{OWNER_USERNAME}](https://t.me/{OWNER_USERNAME})"
    )

    await event.reply(text, link_preview=False)

import asyncio
from telethon import events

# Fungsi konverter Small Caps otomatis
def to_sc(text):
    n = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    s = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return text.translate(str.maketrans(n, s))

@events.register(events.NewMessage(pattern=r"\.maaf", outgoing=True))
async def animasi_maaf(event):
    sender = await event.get_sender()
    if sender.id != OWNER_ID:
        return
    # 1. Cek apakah kita me-reply pesan seseorang
    reply = await event.get_reply_message()
    
    # Ambil nama depan orang yang di-reply jika ada
    target = ""
    if reply:
        user = await event.client.get_entity(reply.sender_id)
        target = f" {user.first_name}"

    # 2. Daftar kalimat animasi (dengan variabel target)
    percakapan = [
        to_sc("ʜᴀʟᴏ") + target + "...",
        to_sc("ʙᴏʟᴇʜ ᴍɪɴᴛᴀ ᴡᴀᴋᴛᴜɴʏᴀ sᴇʙᴇɴᴛᴀʀ?"),
        to_sc("ᴀᴋᴜ ᴛᴀᴜ ᴀᴋᴜ ᴍᴜɴɢᴋɪɴ sᴀʟᴀʜ,"),
        to_sc("ᴀᴋᴜ ᴍᴜɴɢᴋɪɴ ʙɪᴋɪɴ ᴋᴀᴍᴜ ᴋᴇsᴇʟ,"),
        to_sc("ᴀᴛᴀᴜ ʙɪᴋɪɴ ᴋᴀᴍᴜ sᴇᴅɪʜ..."),
        to_sc("ᴊᴀᴅɪ ᴅᴀʀɪ ʜᴀᴛɪ ʏᴀɴɢ ᴘᴀʟɪɴɢ ᴅᴀʟᴀᴍ,"),
        to_sc("ᴀᴋᴜ ᴍᴀᴜ ᴍɪɴᴛᴀ ᴍᴀᴀꜰ ʏᴀ") + target + " 🥺❤️",
        "**ᴊᴀɴᴊɪ ɢᴀᴋ ʙᴀᴋᴀʟ ᴜʟᴀɴɢɪ ʟᴀɢɪ. 🤗**"
    ]

    # 3. Kirim pesan baru sebagai pengganti (agar bersih)
    # Jika reply, pesan animasi akan membalas pesan orang tersebut
    msg = await event.respond(percakapan[0], reply_to=reply.id if reply else None)

    # 5. Jalankan animasi pada pesan baru
    for i in range(1, len(percakapan)):
        await asyncio.sleep(1.8)
        try:
            await msg.edit(percakapan[i])
        except Exception:
            break

client.add_event_handler(animasi_maaf)

import random
from telethon import TelegramClient, events

# Daftar balasan random curhat
CURHAT_REPLIES = [
    # Toxic / nyindir
    "😈 Hah lu mau curhat sama gw? Sama bot? Miris banget hidup lu 😂",
    "💀 Lah elu cerita ke bot? Fix hidup lu udah sepi banget.",
    "🤡 Curhat ke bot? Keren juga elu, next level kesepian nih.",
    "😹 Sumpah gw ngakak, curhatnya ke bot, elu baik-baik aja ga?",
    "👀 Aduh, kalo gw jadi lu sih mending curhat ke tembok sekalian.",
    "🙄 Ckckck… hidup elu sampe curhat ke bot. Respect dah.",

    # Perhatian / care
    "🥰 Kenapa boss? Ayo kita cerita di tempat lu koding gw aja.",
    "💖 Sini ceritain, gw dengerin walau gw cuma bot.",
    "🌸 Santai aja, kadang ngomong ke bot juga lumayan lega kok.",
    "😇 Gpp boss, aku selalu siap jadi tempat curhat kamu.",
    "🤗 Aku mungkin bot, tapi aku bisa dengerin kamu kok.",
    "💌 Yuk cerita aja, anggap aja gw temen chat random.",

    # Lucu / netral
    "😅 Oke, bot siap jadi tong sampah virtual lu!",
    "🙃 Wah menarik juga nih, cerita dong…",
    "😂 Serius? Curhat ke gw? Yaudah sini gw jadi psikolog dadakan.",
    "🤔 Gak masalah kok, kadang ke bot juga lebih aman.",
    "🫶 Santai bro, lu cerita gw baca sambil ngopi virtual.",
    "🐧 Oke bro, gw dengerin nih walau gw cuma skrip Python.",
]

@client.on(events.NewMessage(outgoing=True, pattern=r'bot mau curhat'))
async def curhat_handler(event):
    reply_text = random.choice(CURHAT_REPLIES)
    await event.reply(reply_text)

import asyncio
import random
from telethon import TelegramClient, events

# Maximum number of bombard messages
MAX_BOMBARD = 20

# List of base love messages (short) to build extra dramatic long ones
BASE_MESSAGES = [
    "Fael wants you to know that every second I think of you feels like a thousand shining stars",
    "Every smile of yours lights up the world and makes my heart race uncontrollably",
    "My heart belongs only to you, filled with unstoppable love and passion",
    "If love could speak, it would endlessly whisper your name in every breath I take",
    "I can’t stop imagining us together, every moment becomes an unforgettable love story"
    "I love you VERY MUCH"
]

# List of emojis to sprinkle
EMOJIS = "💖💘💞🔥✨🥰😍💝💌💟💓💗💫💜💛💚💙🫶🌹💐🌸🌺🌼"

def create_extra_dramatic_message():
    """Combine base message + repeated emojis + extra text for long effect"""
    base = random.choice(BASE_MESSAGES)
    emoji_chunk = ''.join(random.choices(EMOJIS, k=50))  # 50+ emojis
    extra = random.choice(BASE_MESSAGES)
    message = f"{emoji_chunk} {base}, {extra}! {emoji_chunk}"
    return message

@client.on(events.NewMessage(outgoing=True, pattern=r'\.love\b'))
async def love_handler(event):
    if not event.is_reply:
        await event.reply("❌ Reply to someone in the group to use .love.")
        return

    replied_msg = await event.get_reply_message()
    target_id = replied_msg.sender_id

    if not target_id:
        await event.reply("❌ Cannot find the user you replied to.")
        return

    # Step 1: Send surprise message
    surprise_msg = f"📣 Fael has a surprise for you on PC!"
    await event.reply(surprise_msg)
    await asyncio.sleep(1.0)

    # Step 2: Bombard love messages (extra dramatic)
    for i in range(MAX_BOMBARD):
        love_msg = create_extra_dramatic_message()
        await client.send_message(target_id, love_msg)
        await asyncio.sleep(1.0 + random.random() * 0.7)  # random delay 1–1.7s

    await event.reply(f"✅ Finished love bombard 💖 ({MAX_BOMBARD} messages)")

import random
from telethon import TelegramClient, events

PICKUP_LINES = [
    "Are you French? Because Eiffel for you.",
    "Do you have a map? I keep getting lost in your eyes.",
    "Are you a magician? Because whenever I look at you, everyone else disappears.",
    "Is your name Wi-Fi? Because I'm feeling a connection.",
    "Are you a parking ticket? Because you’ve got FINE written all over you.",
    "Do you believe in love at first sight—or should I walk by again?",
    "Are you a time traveler? Because I see you in my future.",
    "Are you a loan? Because you have my interest.",
    "Do you have a Band-Aid? Because I just scraped my knee falling for you.",
    "If you were a vegetable, you’d be a cutecumber."
]

@client.on(events.NewMessage(outgoing=True, pattern=r'\.flirt\b'))
async def flirt_handler(event):
    line = random.choice(PICKUP_LINES[:])

    if event.is_reply:
        # Get the original message being replied to
        replied_msg = await event.get_reply_message()
        if replied_msg.sender_id:
            # reply to the original sender
            await replied_msg.reply(f"💘 {line}")
        else:
            # fallback: reply to yourself if no sender found
            await event.reply(f"💘 {line}")
    else:
        # If not a reply, reply to your own command as fallback
        await event.reply(f"💘 {line}")

gombalan = [
    "Atheyya kok cantik bgt, cocok bgt sama boss gw Fael 😏",
    "Waduh Atheyya, makin cantik aja, Fael pasti bangga punya kamu 😍",
    "Atheyya, pesona lu tuh nempel sama boss Fael, serius deh 🥰",
    "Gila Atheyya, cantiknya kayak dibuat spesial buat Fael 💖",
    "Boss Fael tuh pasti senyum terus liat Atheyya 😘",
]

@client.on(events.NewMessage(pattern=r"\.atheyya"))
async def atheyya_handler(event):
    # Kirim pesan awal dan simpan objek pesan
    msg = await event.respond("Mulai gombalin Atheyya...")
    
    # Pastikan msg sudah terdefinisi sebelum loop edit
    if msg:
        for _ in range(10):  # jumlah edit
            await asyncio.sleep(2)  # jeda 2 detik
            new_text = random.choice(gombalan)
            try:
                await msg.edit(new_text)
            except Exception as e:
                print(f"Gagal edit pesan: {e}")

import random
from telethon import events

@client.on(events.NewMessage(pattern=rf"^{PREFIX}ccantik"))
async def cekcantik(event):
    if event.sender_id != OWNER_ID:
        return

    # Ambil nama target
    if event.is_reply:
        reply = await event.get_reply_message()
        name = reply.sender.first_name if reply.sender else "Orang ini"
    else:
        me = await client.get_me()
        name = me.first_name

    # Random stats
    percent = random.randint(1, 100)
    height = random.randint(150, 180)
    weight = random.randint(45, 75)

    # Future predictions
    futures_good = [
        "akan menjadi ceo sukses yang menginspirasi banyak orang",
        "bakal hidup mewah dengan liburan keliling dunia",
        "akan menemukan passion di bidang seni dan jadi terkenal",
        "hidup penuh cinta dan kebahagiaan bersama keluarga",
        "menjadi influencer terkenal dengan banyak penggemar"
    ]
    futures_bad = [
        "menghadapi banyak rintangan dalam karier, bersabarlah",
        "hidup penuh tantangan dan cobaan berat",
        "akan kehilangan sesuatu yang berharga, tetap semangat",
        "perjalanan cinta akan rumit, jangan putus asa",
        "masa depan kadang tidak sesuai rencana, tetap tegar"
    ]
    future = random.choice(futures_good + futures_bad)

    # Soulmate
    soulmates = [
        "jodohmu adalah orang yang sabar, setia, dan romantis",
        "kamu akan bertemu jodoh saat sedang perjalanan jauh",
        "jodohmu akan datang dari lingkungan kerja",
        "seseorang yang memahami passionmu akan menjadi pasangan ideal",
        "cinta sejati menunggu di tempat yang tak terduga"
    ]
    soulmate = random.choice(soulmates)

    # Aura & comment
    if percent > 90:
        aura = "aura cantik memancar seperti bintang di malam gelap"
        comment = "pesonamu tiada tanding"
    elif percent > 75:
        aura = "aura lembut dan elegan mengelilingimu"
        comment = "cantik banget, bak ratu yang sona"
    elif percent > 50:
        aura = "energi positifmu terasa"
        comment = "lumayan cantik"
    elif percent > 30:
        aura = "sedikit aura misterius"
        comment = "biasa aja, tapi punya pesona"
    else:
        aura = "aura agak redup"
        comment = "santai, semua orang unik"

    # Small caps
    def small_caps(text):
        normal = "abcdefghijklmnopqrstuvwxyz"
        small = "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
        table = str.maketrans(normal + normal.upper(), small + small.upper())
        return text.translate(table)

    label_width = 14
    line_name = f"👤  {'ɴᴀᴍᴇ'.ljust(label_width)}: {small_caps(name)}"
    line_beauty = f"💖  {'ᴄᴀɴᴛɪᴋ'.ljust(label_width)}: {percent}%"
    line_height = f"📏  {'ᴛɪɴɢɢɪ'.ljust(label_width)}: {height} cm"
    line_weight = f"⚖  {'ʙᴇʀᴀᴛ'.ljust(label_width)}: {weight} kg"
    line_aura = f"🌟  {'ᴀᴜʀᴀ'.ljust(label_width)}: {small_caps(aura)}"
    line_comment = f"📝  {'ᴄᴏᴍᴍᴇɴᴛ'.ljust(label_width)}: {small_caps(comment)}"
    line_future = f"🔮  {'ᴍᴀsᴀ ᴅᴇᴘᴀɴ'.ljust(label_width)}: {small_caps(future)}"
    line_soulmate = f"💌  {'ᴊᴏᴅᴏʜ'.ljust(label_width)}: {small_caps(soulmate)}"

    # Build gray box message
    message = (
        f"💠  {small_caps('prediksi kecantikan & masa depan')} {small_caps(name)}  💠\n\n"
        f"{line_name}\n{line_beauty}\n{line_height}\n{line_weight}\n"
        f"{line_aura}\n{line_comment}\n{line_future}\n{line_soulmate}\n\n"
        f"🩵  ᴍᴀᴅᴇ ʙʏ @{small_caps('faelninety1')}"
    )
    message = f"```\n{message}\n```"

    # Send to chat without replying
    await client.send_message(event.chat_id, message, parse_mode="markdown")

from telethon import TelegramClient, events
import asyncio

# ASCII joget frames
frames = [
r""" (\./) 
  (o.o) 
  /)  )╯""",
r""" (\./) 
  (o.o) 
 ╰(  (\ """,
r""" (\./) 
  (o.o) 
  /)  )╯""",
r""" (\./) 
  (o.o) 
 ╰(  (\ """,
r""" (\./) 
  (o.o) 
  /)  )╯""",
r""" (\./) 
  (o.o) 
 ╰(  (\ """,
r""" (\./) 
  (o.o) 
  /)  )╯""",
r""" (\./) 
  (o.o) 
 ╰(  (\ """,
]

# Lirik alay small caps rapat
lyrics = [
"🎶 aku sayang kamu 💖",
"🎶 jangan tinggalin aku 😭",
"🎶 kamu cantik ✨",
"🎶 aku mau peluk kamu 🤗",
"🎶 kita joget bareng 💃🕺",
"🎶 jangan sedih ya 😘",
"🎶 senyum dikit lah 😁",
"🎶 aku sayang kamu terus 💖",
]

async def typewriter(message, text, delay=0.05):
    out = ''
    for c in text:
        out += c
        try:
            await message.edit(out)
        except ValueError:
            continue
        await asyncio.sleep(delay)

@client.on(events.NewMessage(pattern=r'\.joget'))
async def joget(event):
    # kirim frame pertama
    msg = await event.respond(frames[0])
    
    # loop animasi
    for _ in range(3):  # loop 3x biar panjang
        for f, l in zip(frames, lyrics):
            # edit ASCII frame dulu
            try:
                await msg.edit(f)
            except ValueError:
                f = f.replace("\\", "")  # escape backslash kalau error
                await msg.edit(f)
            # edit lirik huruf per huruf
            await typewriter(msg, f + "\n" + l, delay=0.05)
            await asyncio.sleep(0.1)  # 10 FPS


import random
from telethon import events

@client.on(events.NewMessage(pattern=rf"^{PREFIX}cekganteng"))
async def cekganteng(event):
    if event.sender_id != OWNER_ID:
        return

    # Ambil nama target
    if event.is_reply:
        reply = await event.get_reply_message()
        name = reply.sender.first_name if reply.sender else "Orang ini"
    else:
        me = await event.client.get_me()
        name = me.first_name

    # Random stats
    percent = random.randint(1, 100)
    height = random.randint(160, 195)
    weight = random.randint(55, 90)

    # Future predictions
    futures_good = [
        "akan menjadi pengusaha sukses yang dihormati banyak orang",
        "bakal hidup mewah dengan mobil dan rumah keren",
        "akan menemukan passion di bidang olahraga dan jadi terkenal",
        "hidup penuh cinta dan kebahagiaan bersama keluarga",
        "menjadi influencer terkenal dengan banyak penggemar"
    ]
    futures_bad = [
        "menghadapi banyak rintangan dalam karier, tetap semangat",
        "hidup penuh tantangan dan cobaan berat",
        "akan kehilangan sesuatu yang berharga, jangan putus asa",
        "perjalanan cinta akan rumit, bersabarlah",
        "masa depan kadang tidak sesuai rencana, tetap tegar"
    ]
    future = random.choice(futures_good + futures_bad)

    # Soulmate prediction
    soulmates = [
        "jodohmu adalah seseorang yang sabar, setia, dan romantis",
        "kamu akan bertemu jodoh saat sedang perjalanan jauh",
        "jodohmu akan datang dari lingkungan kerja",
        "seseorang yang memahami passionmu akan menjadi pasangan ideal",
        "cinta sejati menunggu di tempat yang tak terduga"
    ]
    soulmate = random.choice(soulmates)

    # Aura
    if percent > 90:
        aura = "aura gagah memancar seperti bintang di malam gelap"
        comment = "pesonamu tiada tanding"
    elif percent > 75:
        aura = "aura kuat dan elegan mengelilingimu"
        comment = "ganteng banget, bak raja sona"
    elif percent > 50:
        aura = "energi positifmu terasa"
        comment = "lumayan ganteng"
    elif percent > 30:
        aura = "sedikit aura misterius"
        comment = "biasa aja, tapi punya pesona"
    else:
        aura = "aura agak redup"
        comment = "santai, semua orang unik"

    # Small caps converter
    def small_caps(text):
        normal = "abcdefghijklmnopqrstuvwxyz"
        small = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
        table = str.maketrans(normal + normal.upper(), small + small.upper())
        return text.translate(table)

    # Justified labels
    label_width = 14
    lines = [
        f"👤  {'ɴᴀᴍᴇ'.ljust(label_width)}: {small_caps(name)}",
        f"💖  {'ɢᴀɴᴛᴇɴɢ'.ljust(label_width)}: {percent}%",
        f"📏  {'ᴛɪɴɢɢɪ'.ljust(label_width)}: {height} cm",
        f"⚖  {'ʙᴇʀᴀᴛ'.ljust(label_width)}: {weight} kg",
        f"🌟  {'ᴀᴜʀᴀ'.ljust(label_width)}: {small_caps(aura)}",
        f"📝  {'ᴄᴏᴍᴍᴇɴᴛ'.ljust(label_width)}: {small_caps(comment)}",
        f"🔮  {'ᴍᴀsᴀ ᴅᴇᴘᴀɴ'.ljust(label_width)}: {small_caps(future)}",
        f"💌  {'ᴊᴏᴅᴏʜ'.ljust(label_width)}: {small_caps(soulmate)}"
    ]

    result = f"💠  {small_caps('prediksi ganteng & masa depan')} {small_caps(name)}  💠\n\n"
    result += "\n".join(lines)
    result += f"\n\n🩵  ᴍᴀᴅᴇ ʙʏ @{small_caps('faelninety1')}"

    # Wrap in triple backticks for gray code block
    result = f"```\n{result}\n```"

    # Send as normal message (not reply)
    await event.respond(result, parse_mode="markdown")

from telethon import events
import random
import asyncio
from telethon import events
import random
import asyncio

# --- Mapping small caps Unicode ---
SMALL_CAPS_MAP = {
    "a": "ᴀ", "b": "ʙ", "c": "ᴄ", "d": "ᴅ", "e": "ᴇ", "f": "ꜰ",
    "g": "ɢ", "h": "ʜ", "i": "ɪ", "j": "ᴊ", "k": "ᴋ", "l": "ʟ",
    "m": "ᴍ", "n": "ɴ", "o": "ᴏ", "p": "ᴘ", "q": "ǫ", "r": "ʀ",
    "s": "s", "t": "ᴛ", "u": "ᴜ", "v": "ᴠ", "w": "ᴡ", "x": "x",
    "y": "ʏ", "z": "ᴢ",
    "A": "ᴀ", "B": "ʙ", "C": "ᴄ", "D": "ᴅ", "E": "ᴇ", "F": "ꜰ",
    "G": "ɢ", "H": "ʜ", "I": "ɪ", "J": "ᴊ", "K": "ᴋ", "L": "ʟ",
    "M": "ᴍ", "N": "ɴ", "O": "ᴏ", "P": "ᴘ", "Q": "ǫ", "R": "ʀ",
    "S": "s", "T": "ᴛ", "U": "ᴜ", "V": "ᴠ", "W": "ᴡ", "X": "x",
    "Y": "ʏ", "Z": "ᴢ",
}

def to_small_caps(text):
    return "".join(SMALL_CAPS_MAP.get(c, c) for c in text)

# --- Kalimat pelet luxury ---
PELET_PHRASES_LUX = [
    "💖 nah, gw udah bantu lu; skrg si {} bakal kecintaan ama lu 😏✨",
    "🌹 udah gw cast spellnya, hati-hati {} bakal selalu kepikiran sama lu 💌🔥",
    "💌 tugas gw selesai! {} bakal kebawa vibes cinta ama lu 💕💫",
    "✨ aura cinta magis aktif! {} bakal makin sayang sama lu 😍🌟",
    "💕 cupid kerja keras buat lu, {} siap kena panah cinta lu 💘😎",
    "💫 udah gw set, sekarang {} bakal sulit nolak pesona lu 🌀💖",
    "🔥 bom pelet aktif! {} bakal melting kalo liat lu 😜💞",
    "😎 mantap! {} bakal selalu kepikiran lu, sukses peletnya ✅✨",
    "🌸 udah gw kasih sentuhan magis, {} bakal klepek-klepek ama lu 😆💗",
    "⚡ eh, magic jalan! {} bakal ngerasa vibes cinta lu terus 😍💥",
]

# --- Step casting luxury ---
CASTING_STEPS_LUX = [
    "✨ mengumpulkan energi cinta...",
    "💫 menyalakan aura pelet...",
    "🌹 mengirim panah cupid...",
    "🔥 memperkuat getaran hati...",
]

# --- Fungsi animasi step ---
async def cinematic_edit(msg, text, speed=0.3):
    """Efek typing dots cinematic"""
    base_text = to_small_caps(text)
    for dots in range(4):
        await msg.edit(base_text + "." * dots)
        await asyncio.sleep(speed)
    await asyncio.sleep(0.7)

# --- Event Telethon ---
@client.on(events.NewMessage(pattern=r"\.pelet", outgoing=True))
async def pelet_cinematic(event):
    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("balas ke pesan seseorang dulu buat pakai .pelet ✨")
        return

    target_name = reply_msg.sender.first_name or "temanmu"

    # Kirim pesan awal
    msg = await event.reply("🔮 sedang casting pelet...")

    # Animasi cinematic step
    for step in CASTING_STEPS_LUX:
        await cinematic_edit(msg, step)

    # Hasil akhir small caps langsung
    phrase = random.choice(PELET_PHRASES_LUX).format(target_name)
    await msg.edit(to_small_caps(phrase))

from telethon import events
from telethon.tl.types import Message

# --- Fonts dictionary ---
FONTS = {
    "bold": str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇"
        "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭0123456789"
    ),
    "italic": str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻"
        "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡0123456789"
    ),
    "small_caps": str.maketrans(
        "abcdefghijklmnopqrstuvwxyz",
        "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘꞯʀsᴛᴜᴠᴡxʏᴢ"
    ),
    # Add more fonts here
}

# --- Command handler ---
@client.on(events.NewMessage(pattern=r"\.font (\w+)", outgoing=True))
async def font_change(event: Message):
    if not event.is_reply:
        await event.reply("Reply to a message to change its font!")
        return

    font_name = event.pattern_match.group(1).lower()

    if font_name not in FONTS:
        await event.reply(
            f"Font not found! Available fonts: {', '.join(FONTS.keys())}"
        )
        return

    reply_msg = await event.get_reply_message()
    original_text = reply_msg.text or ""
    if not original_text:
        await event.reply("The replied message has no text!")
        return

    # Apply the font
    translated_text = original_text.translate(FONTS[font_name])
    await event.reply(translated_text)

from telethon import TelegramClient, events
import random


# Jawaban random kalau ada yang ketik "ngapain ya bot"
saran_ngapain = [
    "Main game aja dulu biar pikiran lo fresh, tapi jangan lupa mandi juga ya bau ketek lo udah kayak naga.",
    "Tidur lah, daripada scroll tiktok sampe subuh terus besoknya nyesel sendiri.",
    "Belajar bentar, jangan males mulu. Hidup lo tuh bukan cuma rebahan doang!",
    "Olahraga lah bego! Minimal jalan keluar beli gorengan biar ada gerak dikit.",
    "Coba keluar rumah hirup udara segar, jangan tiap hari ngurung diri di kamar kayak vampir.",
    "Ngapain? Ya belajar bersyukur lah tolol. Hidup lo masih mending dibanding banyak orang.",
]

@client.on(events.NewMessage(pattern=r"(?i)ngapain ya bot"))
async def handler_ngapain(event):
    await event.reply(random.choice(saran_ngapain))

# pastikan modul asyncio dan telethon.events sudah di-load di file utama
import asyncio
from telethon import events

@client.on(events.NewMessage(pattern=r'^\.autodelete(?:\s+(.+))?$', outgoing=True))
async def fake_autodelete(event):
    """
    .autodelete [@username atau nama] atau reply ke user
    """
    reply = await event.get_reply_message()
    arg = event.pattern_match.group(1)
    target = None

    if reply:
        sender = await reply.get_sender()
        target = sender.username or (sender.first_name if sender.first_name else str(reply.sender_id))
    elif arg:
        target = arg.strip()
    else:
        await event.reply("❗Reply ke pesan atau sertakan nama/@username. Contoh: .autodelete @nama")
        return

    # Kirim pesan awal
    msg = await event.reply(
        f"🗑 Memulai proses auto-delete semua BBC milik {target} di perangkat...\nHarap tunggu.",
        parse_mode='md'
    )
    await asyncio.sleep(1.0)

    # Edit bertahap untuk efek realistis
    await msg.edit("🔎 Mendeteksi perangkat terkait...")
    await asyncio.sleep(0.9)
    await msg.edit("🔐 Mengautentikasi sesi dan izin akses...")
    await asyncio.sleep(1.1)
    await msg.edit("📁 Mengumpulkan daftar file dan pesan yang berkaitan (0/128)...")
    await asyncio.sleep(0.8)
    await msg.edit("📁 Mengumpulkan daftar file dan pesan yang berkaitan (32/128)...")
    await asyncio.sleep(0.9)
    await msg.edit("📁 Mengumpulkan daftar file dan pesan yang berkaitan (89/128)...")
    await asyncio.sleep(1.0)
    await msg.edit("🧹 Memulai penghapusan terjadwal pada folder pesan, media, dan cache...")
    await asyncio.sleep(1.2)
    await msg.edit("⏳ Proses encrypt-wipe dan overwrite (fase 1/3)...")
    await asyncio.sleep(1.0)
    await msg.edit("⏳ Proses encrypt-wipe dan overwrite (fase 2/3)...")
    await asyncio.sleep(1.0)
    await msg.edit("⏳ Proses encrypt-wipe dan overwrite (fase 3/3)...")
    await asyncio.sleep(1.0)

    # Final "fake success" message — sekarang memuat kalimat yang kamu minta
    final_text = (
        "✅ SUKSES — Auto-delete selesai.\n\n"
        "skrg automatis menghapus bbc baru user ini di hp kamu\n\n"
        f"Target: {target}\n"
        "Items terhapus: 128 (pesan, media, cache, backup lokal)\n"
        "Status: TERHAPUS PERMANEN\n\n"
        "Ref: AD-20250923-001\n"
        "Waktu: 2025-09-23 15:28 \n\n"
    )
    await msg.edit(final_text, parse_mode='md')

# pastikan modul asyncio dan telethon.events sudah ada di file utama
import asyncio
from telethon import events

import asyncio

@client.on(events.NewMessage(pattern=r'^\.blokpermanen(?:\s+(.+))?$', outgoing=True))
async def fake_perma_block(event):
    """
    .blokpermanen [@username atau ID] atau reply ke user
    """
    if event.sender_id != OWNER_ID:
        return  # hanya owner yang bisa pakai

    reply = await event.get_reply_message()
    arg = event.pattern_match.group(1)
    target_text = None

    if reply:
        target_text = f"{reply.sender_id}" if not reply.sender else (reply.sender.username or f"{reply.sender_id}")
    elif arg:
        target_text = arg.strip()
    else:
        await event.reply("❗ reply ke pesan user atau sertakan @username / user_id")
        return

    # Proses bertahap dengan delay
    msg = await event.reply(f"⏳ ᴍᴇᴍᴘʀᴏsᴇs ʙʟᴏᴋ ᴘᴇʀᴍᴀɴᴇɴ ᴜɴᴛᴜᴋ {target_text}...")
    await asyncio.sleep(1.2)

    await msg.edit("🔒 ᴍᴇɴɢʜᴜʙᴜɴɢɪ sᴇʀᴠᴇʀ...")
    await asyncio.sleep(0.9)
    await msg.edit("🔒 ᴍᴇɴᴏɴᴀᴋᴛɪꜰᴋᴀɴ ᴀᴋꜱᴇꜱ...")
    await asyncio.sleep(1.0)
    await msg.edit("🔒 ᴍᴇɴɢʜᴀᴘᴜꜱ sᴇꜱɪ ᴀᴋᴛɪꜰ...")
    await asyncio.sleep(0.9)

    # Final message minimal, symmetrical
    final = (
        "✅ sᴜᴋsᴇs\n\n"
        f"ᴀᴋᴜɴ {target_text} ᴛᴇʟᴀʜ ᴅɪʙʟᴏᴋ ᴘᴇʀᴍᴀɴᴇɴ.\n"
        "sᴛᴀᴛᴜs: ᴛᴇʀᴋᴜɴᴄɪ • ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴅɪʙᴜᴋᴀ ʟᴀɢɪ\n\n"
    )
    await msg.edit(final)

import random
from telethon import TelegramClient, events

# Kata-kata bucin untuk Diva
LOVEDIVA_RESPONSES = [
    "celia, aku ga bisa sehari tanpa mikirin kamu 😍",
    "Kalau ada 100 alasan buat nyerah, aku tetap pilih celia 💖",
    "Setiap detik berlalu cuma buat celia tercinta 💕",
    "Apapun yang terjadi, celia tetap di hati aku selamanya ❤",
    "Matahari aja kalah terang sama senyumnya celia ☀✨",
    "Hidup aku hampa kalau ga ada celia 😘",
    "celia, kamu alasan aku buat terus bertahan 🌹",
]

# Hinaan default kalau non-owner makai
DEFAULT_RESPONSES = [
    "Apaan sih? Command ini bukan buat lo.",
    "Lu kira bisa pake? cuma boss gw yg boleh.",
    "Ngapain coba? ga guna.",
    "Wkwk sok asik, command ini khusus owner bego.",
]

@client.on(events.NewMessage(pattern=r"\.lovecelia"))
async def lovediva_cmd(event):
    if event.sender_id in [OWNER_ID, SPECIAL_USER_ID]:
        await event.reply(random.choice(LOVEDIVA_RESPONSES))
    else:
        await event.reply(random.choice(DEFAULT_RESPONSES))


@client.on(events.NewMessage(pattern=r"\.lovemaya"))
async def lovemaya_cmd(event):
    await event.reply("no komen")

import random
from telethon import TelegramClient, events

# Hinaan khusus buat .lovekilap
LOVEKILAP_RESPONSES = [
    "hokcuh! Seriusan lu mau love in dia? gamau gw.",
    "Love kilap? Halah, kaya lu bakal diterima aja.",
    "Kilap? wkwk, kasian amat naksir sekelas lampu neon.",
    "Serius bro? LOVE KILAP?? ga ada target lain gitu?",
    "Cieee, love kilap… besok patah hati juga.",
    "Love kilap tuh kayak mimpi basah, bangun ilang.",
]

# Hinaan default kalau non-owner makai
DEFAULT_RESPONSES = [
    "Apaan sih? Command ini bukan buat lo.",
    "Lu kira bisa pake? cuma boss gw yg boleh.",
    "Ngapain coba lu .lovekilap? ga guna.",
    "Wkwk sok asik, command ini khusus owner bego.",
]

@client.on(events.NewMessage(pattern=r"\.lovekilap"))
async def lovekilap_cmd(event):
    if event.sender_id == OWNER_ID:
        await event.reply(random.choice(LOVEKILAP_RESPONSES))
    else:
        await event.reply(random.choice(DEFAULT_RESPONSES))

import random
from telethon import TelegramClient, events

# Kumpulan kata-kata random
RESPONSES = [
    "Seperti ya mana ge tau lah bego? lu kira gw dukun?",
    "Ngapain nanya gw? Tanya google sono.",
    "Lu pikir gw cenayang?",
    "Mungkin itu mantan lu, coba tanya hati kecil lu.",
]

@client.on(events.NewMessage(pattern=r"\.inisiapa"))
async def handler(event):
    await event.reply(random.choice(RESPONSES))

from telethon import events
import random

BOT_ANGRY_AT_OWNER = [
    "😡 Lah malah nyuruh benci Diva? Aku yang benci sama KAMU sekarang!",
    "😤 Jangan nyuruh-nyuruh bot, dasar bikin emosi!",
    "🙄 Kamu pikir aku robot suruhan? Sana urus sendiri!",
    "😠 Aku marah sama kamu, bukan sama Diva!",
    "😡 Aku nggak mau nurut! Sekarang aku nge-hate KAMU!"
]

@client.on(events.NewMessage(pattern=r'^\.hatediva$', outgoing=True))
async def hate_diva(event):
    sender = await event.get_sender()
    if sender.id != OWNER_ID:
        await event.reply("❌ Hanya owner yang bisa pakai command ini.")
        return

    reply = random.choice(BOT_ANGRY_AT_OWNER)
    await event.reply(reply)

import asyncio
from telethon import events

@client.on(events.NewMessage(pattern=r'^\.sembuh$'))
async def sembuh(event):
    if event.sender_id != OWNER_ID:
        return

    reply = await event.get_reply_message()

    steps = [
        "⟡ ᴍᴇɴʏɪᴀᴘᴋᴀɴ ᴘᴇʀᴀʟᴀᴛᴀɴ ᴍᴇᴅɪs...",
        "⟡ ᴍᴇɴɢɪsɪ ᴄᴀɪʀᴀɴ ɪɴꜰᴜꜱ ᴅᴇɴɢᴀɴ ᴋᴏᴍᴘᴏꜱɪꜱɪ ᴇʟᴇᴋᴛʀᴏʟɪᴛ ʏᴀɴɢ sᴇɪᴍʙᴀɴɢ...",
        "⟡ ᴍᴇᴍᴀsᴀɴɢ ɪɴꜰᴜꜱ ᴅɪ ᴛᴀɴɢᴀɴ ᴋɪʀɪ...",
        "⟡ ᴍᴇᴍᴇʀɪᴋsᴀ ᴛᴇᴋᴀɴᴀɴ ᴅᴀʀᴀʜ ᴅᴀɴ ᴅᴇɴʏᴜᴛ ɴᴀᴅɪ...",
        "⟡ 💠 ʙᴇᴇᴘ... ʙᴇᴇᴘ... ʙᴇᴇᴘ... sɪsᴛᴇᴍ ᴍᴇᴍᴏɴɪᴛᴏʀ ᴊᴀʟᴀɴ...",
        "⟡ ᴄᴀɪʀᴀɴ ᴍᴜʟᴀɪ ᴍᴇɴɢᴀʟɪʀ ᴘᴇʟᴀɴ...",
        "⟡ sᴜʜᴜ ᴛᴜʙᴜʜ ᴍᴇɴᴜʀᴜɴ, ᴅᴇɴʏᴜᴛ ᴛᴇʀᴀᴛᴜʀᴀʟ ᴋᴇᴍʙᴀʟɪ...",
        "⟡ ᴘᴇɴɢᴜᴋᴜʀᴀɴ ᴛᴇʀᴀᴋʜɪʀ ᴅɪʟᴀᴋᴜᴋᴀɴ...",
        "⟡ 💉 ᴘʀᴏsᴇs ᴛᴇʀᴀᴋʜɪʀ: ᴘᴀsɪᴇɴ sᴇᴍʙᴜʜ.",
    ]

    for i, step in enumerate(steps):
        if i == 0:
            msg = await event.reply(step, reply_to=reply)
        else:
            await msg.edit(step)
        await asyncio.sleep(1.5)

from telethon import events
import asyncio
import random

@client.on(events.NewMessage(pattern=r'\.sora'))
async def sora_handler(event):
    if event.sender_id != OWNER_ID:
        return
    
    gibah_sora = [
        "Eh sumpah ya, si Sora itu kalo ngomong gede banget gayanya, padahal isinya kosong 🤭",
        "Lo sadar gak sih, Sora tuh tiap nongol vibes-nya kayak NPC error muter-muter 😆",
        "Kadang suka ngakak, Sora itu sok jago padahal semua orang ngomongin dia di belakang 😂",
        "Beneran deh, bahan gibah paling enak tuh Sora, hinaannya tuh unlimited 🙄",
        "Sora tuh kalo jalan kayak bawa beban dunia, tapi sebenernya beban grup doang 🤣",
        "Gua rasa Sora lahir emang ditakdirin buat jadi bahan ketawaan orang wkwkwk 😏",
        "Woi jangan kaget, Sora tuh kalo diem doang orang-orang udah ilfeel sama auranya 🤣",
        "Ada yg sadar ga, Sora kalo ngetik tuh kayak robot error keyboardnya stuck 😂"
    ]
    
    # kirim pesan awal
    msg = await event.respond("Ngomongin Sora dulu bentar... 😏")
    
    # loop edit
    for i in range(20):  # jumlah loop (20x ganti hinaan)
        await asyncio.sleep(2)  # delay antar edit
        await msg.edit(random.choice(gibah_sora))
    
    # closing message
    await msg.edit("Udah cukup gibahin Sora, kasian juga si NPC error 🤭")

from collections import Counter
import re
from telethon import events

@client.on(events.NewMessage(pattern=r'\.stats'))
async def stats_handler(event):
    chat = await event.get_chat()
    msg = await event.reply("📊 Mengumpulkan statistik, tunggu sebentar...")

    # Ambil peserta dan pesan
    all_participants = await client.get_participants(chat)
    messages = await client.get_messages(chat, limit=1000)

    # Hitung statistik
    total_members = len(all_participants)
    admins = len([p for p in all_participants if p.admin_rights or p.is_admin])
    bots = len([p for p in all_participants if p.bot])

    users_counter = Counter()
    words_counter = Counter()
    emoji_counter = Counter()
    hours_counter = Counter()

    for msg_item in messages:
        if msg_item.sender_id:
            users_counter[msg_item.sender_id] += 1
        if msg_item.message:
            words = re.findall(r'\w+', msg_item.message.lower())
            words_counter.update(words)
            emoji_counter.update(c for c in msg_item.message if c in '😀😂🤣😍😎😉👍🔥💀❤💔😭🙌✨')
        if msg_item.date:
            hours_counter[msg_item.date.hour] += 1

    # Ambil top data
    top_posters = users_counter.most_common(5)
    top_words = words_counter.most_common(5)
    top_emojis = emoji_counter.most_common(5)
    busiest_hour = hours_counter.most_common(1)[0][0] if hours_counter else None

    # Ambil nama/top poster
    top_posters_str = ""
    for i, (user_id, count) in enumerate(top_posters):
        try:
            user = await client.get_entity(user_id)
            name = f"@{user.username}" if user.username else user.first_name
        except:
            name = f"User {user_id}"
        top_posters_str += f"{i+1}. {name} - {count} pesan\n"

    # Format hasil
    formatted = f"""
📊 *Statistik Grup*
- Total anggota: {total_members}
- Admin: {admins}
- Bots: {bots}

🏆 *Top Poster*
{top_posters_str}

📝 *Kata Populer*
{', '.join([f'{w} ({c})' for w,c in top_words])}

😀 *Emoji Populer*
{', '.join([f'{e} ({c})' for e,c in top_emojis])}

⏰ *Jam paling aktif:* {busiest_hour}:00
"""

    await msg.edit(formatted)

import os, json
from telethon import TelegramClient, events

BLACKLIST_FILE = "blacklist.json"

# --- Load/Save blacklist ---
def load_blacklist():
    if os.path.exists(BLACKLIST_FILE):
        try:
            with open(BLACKLIST_FILE, "r") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_blacklist():
    with open(BLACKLIST_FILE, "w") as f:
        json.dump(list(blacklisted_chats), f)

blacklisted_chats = load_blacklist()

# ========== GLOBAL FILTER ==========
@client.on(events.NewMessage)
async def global_blacklist_filter(event):
    chat_id = event.chat_id
    if chat_id in blacklisted_chats:
        cmd = event.raw_text.strip().lower()
        # only allow .unaddbl and .listbl when blacklisted
        if cmd not in [".unaddbl", ".listbl"]:
            raise events.StopPropagation

# ========== .addbl ==========
@client.on(events.NewMessage(pattern=r"^\.addbl$"))
async def addbl_handler(event):
    if event.sender_id != OWNER_ID:
        return
    chat_id = event.chat_id
    blacklisted_chats.add(chat_id)
    save_blacklist()
    await event.reply("✨ ᴄʜᴀᴛ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ\n ɪ ᴡɪʟʟ ʀᴇᴍᴀɪɴ sɪʟᴇɴᴛ ʜᴇʀᴇ.")

# ========== .unaddbl ==========
@client.on(events.NewMessage(pattern=r"^\.unaddbl$"))
async def unaddbl_handler(event):
    if event.sender_id != OWNER_ID:
        return
    chat_id = event.chat_id
    if chat_id in blacklisted_chats:
        blacklisted_chats.remove(chat_id)
        save_blacklist()
        await event.reply("💫 ʙʟᴀᴄᴋʟɪsᴛ ʀᴇᴍᴏᴠᴇᴅ\n ɪ ᴀᴍ ᴀᴄᴛɪᴠᴇ ᴀɢᴀɪɴ.")
    else:
        await event.reply("⚪ ɴᴏᴛ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ\n ᴛʜɪs ᴄʜᴀᴛ ɪsɴ’ᴛ ᴏɴ ᴛʜᴇ ʟɪsᴛ.")

# ========== .listbl ==========
@client.on(events.NewMessage(pattern=r"^\.listbl$"))
async def listbl_handler(event):
    if event.sender_id != OWNER_ID:
        return
    if not blacklisted_chats:
        await event.reply("⚪ ɴᴏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛs\n> ᴇᴠᴇʀʏᴛʜɪɴɢ ɪs ᴄʟᴇᴀʀ.")
        return

    text = "🕶 ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛs\n"
    for cid in blacklisted_chats:
        text += f"> • {cid}\n"
    await event.reply(text)

import asyncio
import random


# Kata-kata hacker / menyeramkan
SCARY_WORDS = [
    "Accessing mainframe", "Decrypting password", "Bypassing firewall",
    "Injecting virus", "Stealing data", "Uploading malware", "Tracing IP",
    "Erasing logs", "Compiling secrets", "Corrupting system", "Hacking network"
]

# Flag untuk stop hack
hack_running = False

# Function buat progress bar (bar lebih pendek)
def fake_progress(percent):
    total = 15  # <-- dipendekkan supaya muat satu bar
    filled = int(total * percent // 100)
    empty = total - filled
    bar = "█" * filled + "░" * empty
    return f"[{bar}] {percent}%"

# Function buat password palsu
def fake_password():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    return "".join(random.choices(chars, k=random.randint(8,12)))

@client.on(events.NewMessage(pattern=r"\.hack"))
async def hack(event):
    global hack_running
    if event.sender_id != OWNER_ID:
        return

    if not event.is_reply:
        return await event.reply("⚠ Balas ke pesan target untuk hack!")

    target_msg = await event.get_reply_message()
    target_username = target_msg.sender.username or target_msg.sender.first_name or "TargetUser"

    hack_running = True
    sent_msg = await event.reply("Initializing hack... 💻")

    percent = 0
    while percent < 100 and hack_running:
        scary_text = random.choice(SCARY_WORDS)
        progress_bar = fake_progress(percent)
        await sent_msg.edit(f"{scary_text}\n{progress_bar}")

        # Tambah persen random tiap loop, kadang cepat kadang lambat
        percent += random.randint(1,10)
        if percent > 100:
            percent = 100

        # Delay acak untuk realism (0.3s - 1.8s)
        await asyncio.sleep(random.uniform(0.3, 1.8))

    if hack_running:
        fake_pass = fake_password()
        await sent_msg.edit(f"✅ Hack selesai!\nUsername: {target_username}\nPassword: {fake_pass} 🔥💻 akun ada akan dinonaktifkan sebentar lagi.")

@client.on(events.NewMessage(pattern=r"\.stophack"))
async def stop_hack(event):
    global hack_running
    if event.sender_id != OWNER_ID:
        return await event.reply("❌ Kamu tidak bisa pakai command ini!")

    if hack_running:
        hack_running = False
        await event.reply("✅ hack dihentikan!")
    else:
        await event.reply("⚠ Tidak ada hack yang berjalan.")

# Telethon: .deak single-message edited animation (Bahasa Indonesia, small-caps)
import asyncio
from telethon import events

# small-caps mapping (glyphs)
_SMALL_CAPS = {
    'a':'ᴀ','b':'ʙ','c':'ᴄ','d':'ᴅ','e':'ᴇ','f':'ꜰ','g':'ɢ','h':'ʜ','i':'ɪ',
    'j':'ᴊ','k':'ᴋ','l':'ʟ','m':'ᴍ','n':'ɴ','o':'ᴏ','p':'ᴘ','q':'ǫ','r':'ʀ',
    's':'ꜱ','t':'ᴛ','u':'ᴜ','v':'ᴠ','w':'ᴡ','x':'x','y':'ʏ','z':'ᴢ',
    'A':'ᴀ','B':'ʙ','C':'ᴄ','D':'ᴅ','E':'ᴇ','F':'ꜰ','G':'ɢ','H':'ʜ','I':'ɪ',
    'J':'ᴊ','K':'ᴋ','L':'ʟ','M':'ᴍ','N':'ɴ','O':'ᴏ','P':'ᴘ','Q':'ǫ','R':'ʀ',
    'S':'ꜱ','T':'ᴛ','U':'ᴜ','V':'ᴠ','W':'ᴡ','X':'x','Y':'ʏ','Z':'ᴢ',
    '0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8','9':'9',
    '.':'.',',':',','!':'!','?':'?',' ':' '
}

def to_small_caps(text: str) -> str:
    return ''.join(_SMALL_CAPS.get(ch, ch) for ch in text)

@client.on(events.NewMessage(pattern=r"\.deak"))
async def deak(event):
    try:
        # kirim satu pesan dan edit terus (no spam)
        m = await event.reply(to_small_caps("memulai..."))

        # animasi titik mewah (1-4), loop 5 kali, cepat
        for _ in range(5):
            for dots in [".", "..", "...", "...."]:
                await m.edit(to_small_caps(f"menonaktifkan{dots}"))
                await asyncio.sleep(0.12)

        # urutan teks utama (terlihat realistik)
        seq = [
            "menghubungkan ke server telegram...",
            "memverifikasi sesi...",
            "menghapus perangkat terkait...",
            "menghapus data cloud...",
            "menghapus riwayat pesan...",
            "menyelesaikan proses...",
            "akun dihapus.",
            "pengguna ini tidak lagi tersedia di telegram."  # baris reveal tunggal
        ]

        for item in seq:
            await m.edit(to_small_caps(item))
            await asyncio.sleep(0.7)

    except Exception as e:
        # opsional: edit pesan kalau error
        try:
            await m.edit(to_small_caps("terjadi kesalahan."))
        except:
            pass
        raise

import asyncio
from datetime import datetime
from telethon import events

@client.on(events.NewMessage(pattern=r"\.ping$"))
async def ping(event):
    if event.sender_id != OWNER_ID:
        return
    start = datetime.now()
    msg = await event.reply("📡 ᴘɪɴɢ")

    # fast smooth animation: 5 loops, 1–4 dots
    for _ in range(5):
        for i in range(1, 5):
            dots = "·" * i
            await msg.edit(f"📡 ᴘɪɴɢ{dots}")
            await asyncio.sleep(0.08)  # shorter delay for faster animation

    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await msg.edit(luxury_ping_text(ms))

@client.on(events.NewMessage(pattern=r"^\.spam (\d+) (.+)$"))
async def spam(event):
    if event.sender_id != OWNER_ID:
        return

    jumlah, teks = event.pattern_match.group(1), event.pattern_match.group(2)
    jumlah = int(jumlah)
    
    for _ in range(jumlah):
        await event.reply(teks)
        await asyncio.sleep(0.5)  

# Variabel global
afk_status = False
afk_reason = ""
afk_mentions = {}  # {user_id: nama}

# Command .afk
@client.on(events.NewMessage(pattern=r"^\.afk(?:\s+(.+))?$"))
async def afk(event):
    if event.sender_id != OWNER_ID:
        return  # hanya OWNER_ID yang bisa pakai
    global afk_status, afk_reason, afk_mentions
    afk_status = True
    afk_reason = event.pattern_match.group(1) or "Sedang AFK"
    afk_mentions = {}
    await event.reply(f"💤 Kamu sekarang AFK!\nAlasan: {afk_reason}")

# Command .unafk
@client.on(events.NewMessage(pattern=r"^\.unafk$"))
async def unafk(event):
    if event.sender_id != OWNER_ID:
        return  # hanya OWNER_ID yang bisa pakai
    global afk_status, afk_reason, afk_mentions
    if afk_status:
        count = len(afk_mentions)
        names = ", ".join(afk_mentions.values()) if count > 0 else "Tidak ada"
        afk_status = False
        afk_reason = ""
        afk_mentions = {}
        await event.reply(f"✅ Kamu keluar dari AFK.\n💬 Jumlah orang yang nge-mention: {count}\n📝 Nama: {names}")
    else:
        await event.reply("⚠ Kamu tidak sedang AFK.")

# Auto-reply saat AFK (untuk orang lain)
@client.on(events.NewMessage(incoming=True))
async def afk_reply(event):
    global afk_status, afk_reason, afk_mentions
    if afk_status:
        sender = event.sender_id
        sender_name = event.sender.first_name or "User"
        if sender == OWNER_ID:
            return  # jangan balas diri sendiri
        # Balas jika di-reply atau mention
        if ((event.is_reply and (await event.get_reply_message()).sender_id == sender)
            or (event.message.message.find(f"@{event.sender.username}") != -1 if event.sender.username else False)):
            afk_mentions[sender] = sender_name
            await event.reply(f"💤 Saya sedang AFK!\nAlasan: {afk_reason}")


# Emoji yang dipakai
EMOJIS = ["😂","🤣","🔥","💀","✨","💖","😎","🤪","😜","🥵","💫","💥","🥳","💦","💢","👀","🙌","🥶","💣"]

# Flag untuk stop loop
_running = False

# Function untuk buat teks panjang ala 
def _text_long():
    base_words = [
        "hallo", "kamu", "lagi", "ngapain", "gila", "wkwk", "asik", "mantap", "ciee", "baper", 
        "parah", "kocak", "ngakak", "sipp", "hebat", "woy", "yoi", "gokil", "hadehh", "mantul"
    ]
    result = ""
    for _ in range(80):  # bikin panjang
        word = random.choice(base_words)
        # ubah huruf jadi besar/kecil acak + tambah emoji acak
        word_ = "".join([c.upper() if random.choice([True, False]) else c.lower() for c in word])
        emojis = "".join(random.choices(EMOJIS, k=random.randint(1,3)))
        result += word_ + emojis + " "
    return result

@client.on(events.NewMessage(pattern=r"\.alay"))
async def _loop(event):
    global _running
    if event.sender_id != OWNER_ID:
        return

    _running = True
    sent_msg = await event.reply(_text_long())

    i = 0
    while _running:
        new_text = _text_long()
        # tambah emoji 🔥 semakin loop
        new_text += " " + "🔥" * (i % 50 + 10)
        await sent_msg.edit(new_text)
        i += 1
        await asyncio.sleep(1)  # interval 1 detik

import random
import asyncio
from telethon import events

# --- TEKS ROMANTIS LEMBUT (GANTI2 SETIAP LOOP) ---
ROMANTIC_TEXTS = [
    "Every heartbeat whispers your name softly.",
    "Your soul feels like my home.",
    "You are the calm after every storm.",
    "Even silence feels warm when it's with you.",
    "You’re my favorite kind of peace.",
    "My heart smiles every time it thinks of you.",
    "You glow softer than the moonlight itself.",
    "Your love feels like poetry in motion.",
    "I find serenity in your eyes.",
    "You are love in its purest form.",
    "With every breath, I think of you.",
    "Your presence turns ordinary moments magical.",
    "You’re the gentle rhythm my heart beats to.",
    "In your arms, I find forever.",
    "Every second with you feels divine."
]

# --- FLAG LOOP ---
iloveyou_running = False

# --- TEKS UTAMA (TETAP) ---
MAIN_LOVE = "💞 𝓛𝓸𝓿𝓮 𝓯𝓸𝓻 𝔂𝓸𝓾 💞"

# --- GENERATOR TEKS (SATU LINE DALAM CODE BLOCK) ---
def romantic_line(target_name):
    bucin = random.choice(ROMANTIC_TEXTS)
    return f"{MAIN_LOVE} {target_name} — {bucin}"

# --- COMMAND .iloveyou ---
@client.on(events.NewMessage(pattern=r"\.iloveyou"))
async def iloveyou_loop(event):
    global iloveyou_running
    if event.sender_id != OWNER_ID:
        return

    if not event.is_reply:
        return await event.reply("💌 Balas ke pesan target!")

    target_msg = await event.get_reply_message()
    target_name = target_msg.sender.first_name or target_msg.sender.username or "Someone Special"

    iloveyou_running = True
    sent_msg = await event.respond(romantic_line(target_name), reply_to=target_msg.id, parse_mode="markdown")

    while iloveyou_running:
        new_text = romantic_line(target_name)
        await sent_msg.edit(new_text, parse_mode="markdown")
        await asyncio.sleep(random.uniform(2.8, 4.5))  # jeda romantis

# --- COMMAND .stopiloveyou ---
@client.on(events.NewMessage(pattern=r"\.stopiloveyou"))
async def stop_iloveyou(event):
    global iloveyou_running
    if event.sender_id != OWNER_ID:
        return

    if iloveyou_running:
        iloveyou_running = False
        await event.reply("💫 Love stopped gracefully 💫")
    else:
        await event.reply("⚠ Tidak ada .iloveyou yang sedang berjalan.")
        
        from telethon import events


from telethon import events
import asyncio
import random

@client.on(events.NewMessage(pattern=r"\.sinyal$", outgoing=True))
async def sinyal(event):
    if event.sender_id != OWNER_ID:
        return
    bar_symbols = ["·", "▂", "▃", "▅", "▆", "█"]
    
    status_texts = [
        "sɪɢɴᴀʟ sᴛᴀʙʟᴇ ✅",
        "ɴᴇᴛᴡᴏʀᴋ ᴏᴘᴛɪᴍɪᴢᴇᴅ",
        "ᴍᴀxɪᴍᴜᴍ ʙᴀɴᴅᴡɪᴅᴛʜ",
        "ᴜʟᴛʀᴀ ᴄᴏɴɴᴇᴄᴛɪᴏɴ",
        "ᴄᴏɴɴᴇᴄᴛɪᴏɴ sᴇᴄᴜʀᴇᴅ",
        "sᴄᴀɴɴɪɴɢ ɴᴇᴛᴡᴏʀᴋs...",
        "ᴛᴏᴡᴇʀ sᴛᴀʙɪʟɪᴢɪɴɢ",
        "ᴍᴏᴅᴜʟᴇs ᴀʟɪɢɴɪɴɢ",
        "ᴜᴘᴅᴀᴛɪɴɢ ᴄᴏɴɴᴇᴄᴛɪᴏɴ"
    ]

    sound_sim = ["BEEP", "BEEP..", "BEEP...", "PING", "PING..", "PING..."]

    intro_texts = [
        "🔍 sᴇᴀʀᴄʜɪɴɢ ғᴏʀ sɪɴʏᴀʟ...",
        "📡 aᴅᴊᴜsᴛɪɴɢ ɴᴇᴛᴡᴏʀᴋ...",
    ]
    for txt in intro_texts:
        await event.edit(txt)
        await asyncio.sleep(1.5)

    # 2️⃣ Ultra cinematic scanning
    for i in range(80):  # lebih banyak frame untuk cinematic effect
        # Signal bar naik turun acak
        bars = "".join(random.choices(bar_symbols, k=5))
        ping = random.choice(sound_sim)
        status = random.choice(status_texts)
        
        # Reveal typing effect kecil
        reveal_len = min(i % (len(status)+1), len(status))
        display_text = f"sɪɴʏᴀʟ: {bars} — {ping}\n{status[:reveal_len]}"
        await event.edit(display_text)
        await asyncio.sleep(0.066)  # ~15fps

    # 3️⃣ Ending cinematic blink + pulse
    final_status = random.choice(status_texts)
    for _ in range(10):
        bars_full = "".join(random.choices(bar_symbols[-2:], k=5))  # bar hampir penuh
        ping = random.choice(sound_sim)
        await event.edit(f"sɪɴʏᴀʟ: {bars_full} — {ping}\n{final_status} ▂▃▅▆█")
        await asyncio.sleep(0.066)
        await event.edit(f"sɪɴʏᴀʟ: {bars_full} — {ping}\n{final_status}")
        await asyncio.sleep(0.066)

import asyncio
import random
from telethon import events

# Simpan status bom di memori
bomb_data = {}

@client.on(events.NewMessage(pattern=r"^\.bom$", outgoing=True))
async def start_bomb(event):
    colors = ["Merah", "Biru", "Kuning", "Hijau"]
    correct_color = random.choice(colors)
    
    # Simpan jawaban benar berdasarkan ID pesan
    bomb_data[event.chat_id] = correct_color
    
    await event.edit(
        "💣 **BOM DIPASANG!**\n\n"
        "Seseorang harus menjinakkan bom ini dalam 30 detik!\n"
        "Balas (`reply`) pesan ini dengan warna kabel:\n"
        "🔴 Merah | 🔵 Biru | 🟡 Kuning | 🟢 `Hijau`"
    )
    
    # Tunggu 30 detik
    await asyncio.sleep(30)
    
    if event.chat_id in bomb_data:
        await event.edit(f"💥 BOOM!! Bom meledak! Kabel yang benar adalah {correct_color}. Kalian semua payah!")
        del bomb_data[event.chat_id]

@client.on(events.NewMessage)
async def defuse_bomb(event):
    # Cek jika ada bom aktif dan pesan adalah reply ke bom
    if event.chat_id in bomb_data and event.is_reply:
        reply = await event.get_reply_message()
        if "BOM DIPASANG!" in reply.text:
            input_color = event.text.capitalize()
            correct_color = bomb_data[event.chat_id]
            
            if input_color == correct_color:
                await event.respond(f"✅ **BOM DIJINAKKAN!**\nSelamat [{event.sender.first_name}](tg://user?id={event.sender_id}), kamu adalah pahlawan!")
                # Hapus status bom agar tidak meledak di loop awal
                del bomb_data[event.chat_id]
            elif input_color in ["Merah", "Biru", "Kuning", "Hijau"]:
                await event.respond(f"❌ SALAH KABEL! [{event.sender.first_name}](tg://user?id={event.sender_id}) memicu ledakan!")
                # Biarkan loop utama menangani ledakan

import asyncio
from telethon import events, errors
from telethon.tl.types import User

@client.on(events.NewMessage(outgoing=True, pattern=r'^\.ucast(?:\s+(.+))?$'))
async def ucast_handler(event):
    if event.sender_id != OWNER_ID:
        return
    # Ambil teks dari argumen atau reply
    text = event.pattern_match.group(1)
    if not text and event.is_reply:
        reply = await event.get_reply_message()
        if reply and reply.message:
            text = reply.message

    if not text:
        await event.edit("ᴜsᴀɢᴇ: .ucast <pesan> ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴍᴇssᴀɢᴇ")
        await asyncio.sleep(3)
        await event.delete()
        return

    await event.edit("ᴍᴇɴʏɪᴀᴘᴋᴀɴ ᴘᴇʀsᴏɴᴀʟ ᴄʜᴀᴛ...")

    me = await client.get_me()
    dialogs = []
    async for dialog in client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, User) and not entity.bot and entity.id != me.id:
            dialogs.append(entity)

    total = len(dialogs)
    if total == 0:
        await event.edit("ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴘᴇʀsᴏɴᴀʟ ᴄʜᴀᴛ ᴜɴᴛᴜᴋ ᴅɪᴋɪʀɪᴍ.")
        await asyncio.sleep(3)
        await event.delete()
        return

    await event.edit(f"ᴍᴇɴᴇᴍᴜᴋᴀɴ {total} ᴄʜᴀᴛ. ᴍᴇᴍᴜʟᴀɪ ʙʀᴏᴀᴅᴄᴀsᴛ...")

    success = 0
    failed = 0
    delay = 1  # delay antar kiriman

    for idx, user in enumerate(dialogs, start=1):
        try:
            await client.send_message(user, text)
            success += 1
        except errors.FloodWaitError as e:
            await asyncio.sleep(e.seconds + 1)
            try:
                await client.send_message(user, text)
                success += 1
            except:
                failed += 1
        except:
            failed += 1

        # Update progress langsung
        await event.edit(f"ᴜᴄᴀsᴛ ᴘʀᴏɢʀᴇss: {idx}/{total} | sᴜᴋsᴇs: {success} | ɢᴀɢᴀʟ: {failed}")

        await asyncio.sleep(delay)

    # Output akhir dengan emoji ✨
    await event.edit(f"ᴜᴄᴀsᴛ sᴇʟᴇsᴀɪ! ᴛᴏᴛᴀʟ: {total} | sᴜᴋsᴇs: {success} | ɢᴀɢᴀʟ: {failed} ✨")

    await asyncio.sleep(5)
    try:
        await event.delete()
    except:
        pass

from telethon import events
import asyncio
import random

import asyncio
import random
from telethon import events

@client.on(events.NewMessage(pattern=r"\.dino$", outgoing=True))
async def dino_revamp(event):
    # Frame animasi yang lebih "hidup"
    # Menggunakan kombinasi emoji untuk environment
    frames = [
        "🌳          🦖🏃",
        "🌳        🦖🏃  ",
        "🌳      🦖🏃    ",
        "🌳    🦖🏃      ",
        "🌳  🦖🏃        ",
        "🌵🦖🏃          ",
        "🌵  🦖🏃        ",
        "🌵    🦖🏃      ",
        "🌵      🦖🏃    ",
        "🌵        🦖🏃  ",
    ]
    
    # Dialog bergantian agar tidak membosankan
    action_text = [
        "GAWAT! DIA MAU MAKAN AKU! 😱",
        "LARI WOIIII! 🏃💨",
        "JANGAN SAMPAI KETANGKAP! ⚡",
        "KAKIKU SUDAH LEMAS... 😰"
    ]

    await event.edit("`[!] Memulai simulasi purbakala...`")
    await asyncio.sleep(1)

    # 1. Action Sequence (Lari bolak-balik)
    for cycle in range(2):
        for frame in frames:
            text = random.choice(action_text)
            # Gabungan frame environment + karakter + dialog
            await event.edit(f"**DINOSAUR CHASE**\n\n{frame}\n\n`{text}`")
            await asyncio.sleep(0.5) # Kecepatan aman agar tidak limit

    # 2. Plot Twist (Dino-nya capek)
    await event.edit("**DINOSAUR CHASE**\n\n💨       🦖... 🏃💨\n\n`Dino-nya mulai bengek...`")
    await asyncio.sleep(1.2)
    
    await event.edit("**DINOSAUR CHASE**\n\n💨       😫🦖  🙏🏃\n\n`Bentar... istirahat dulu bro.`")
    await asyncio.sleep(1.5)

    # 3. Ending Scene (No Blockquote)
    # Teks bersih dengan simbol estetik
    ending = (
        "🦖 🤝 🏃\n\n"
        "**Info:** Dino cuma mau minta ttd.\n\n"
    )
    
    await event.edit(ending)
   
    from telethon import events
import random

TEBAK_ANSWERS = [
    "☑ YA lah tolol",
    "❌ NGGAK la gblk",
    "🤡 MUNGKIN sih, dasar bego",
    "✅ 100% iya cuy",
    "❌ mana ada, halu lu",
    "🤔 mungkin... tapi kayaknya enggak sih",
    "☠ nggak bakal terjadi bambank",
    "🔥 jelas iya dong bebbb",
    "💩 salah pertanyaan jing",
    "💀 iya... di mimpi lu"
]

@client.on(events.NewMessage(pattern=r"\.iyakah"))
async def tebak(event):
    if event.sender_id != OWNER_ID:
        return await event.reply("❌ Kamu tidak bisa pakai command ini!")

    jawab = random.choice(TEBAK_ANSWERS)
    await event.reply(jawab)

    from telethon import events

jadian_running = False

# kata kata jadian  + emoji, wajib ada {name} untuk target
JADIAN_TEXTS = [
    "💖 SaYa SaYaNg KaMuUuU {name} bEbZz 💖",
    "🌹 {name} tUh CeRiAhIn HaRi² aKuU 🌹",
    "💞 JaNgAn TiNgGaLiN aKuU yAa {name} AyAnKk 💞",
    "💘 KiTa TaK jUdOh Di DuNiA, TaPi AkUu MaU jAdiIn {name} dI HaTi 💘",
    "💕 MaCaM mAnA AkUu tAk Cinta {name}, KaMuUu DuNia aKuU 💕",
    "💓 {name} kAyAk OxYgEn, aKuU sEsAk TaNpA KaMuUu 💓",
    "💝 AkUu BeRbOhOnG kAlAu BilAnG aKuUu TaK rInDu {name} 💝",
    "💌 JaNgAn KaMuU tInGgAlIn AkUu, {name} GaK bIsa HiDp TaNpA KaMuUu 💌"
]

def jadian_text(target_name):
    return random.choice(JADIAN_TEXTS).format(name=target_name)

@client.on(events.NewMessage(pattern=r"\.jadian"))
async def jadian_loop(event):
    global jadian_running
    if event.sender_id != OWNER_ID:
        return await event.reply("❌ Kamu tidak bisa pakai command ini!")

    if not event.is_reply:
        return await event.reply("⚠ Balas ke pesan target untuk jadian!")

    target_msg = await event.get_reply_message()
    target_name = target_msg.sender.first_name or target_msg.sender.username or "Ayank"

    jadian_running = True
    sent_msg = await event.reply(jadian_text(target_name))

    while jadian_running:
        await asyncio.sleep(2)
        await sent_msg.edit(jadian_text(target_name))

@client.on(events.NewMessage(pattern=r"\.stopjadian"))
async def stop_jadian(event):
    global jadian_running
    if event.sender_id != OWNER_ID:
        return await event.reply("❌ Kamu tidak bisa pakai command ini!")

    if jadian_running:
        jadian_running = False
        await event.reply("✅ Loop jadian dihentikan!")
    else:
        await event.reply("⚠ Tidak ada loop jadian yang berjalan.")

LONTE_ANSWERS = [
    "✅ YA lah dasar lonte",
    "❌ BUKAN la goblok",
    "💀 jelas iya, lonte premium",
    "🤡 ngakak, nggak lah tolol",
    "🔥 iya betul betul betul",
    "☠ bukan woy, halu lu",
]

@client.on(events.NewMessage(pattern=r"\.inilonte"))
async def inilonte(event):
    if event.sender_id != OWNER_ID:
        return

    if not event.is_reply:
        return await event.reply("⚠ Harus reply ke orang buat cek lonte!")

    target = await event.get_reply_message()
    target_name = target.sender.first_name or target.sender.username or "Orang"

    jawab = random.choice(LONTE_ANSWERS)
    await event.reply(f"{target_name} : {jawab}")

import os
import yt_dlp
import asyncio
from telethon import events, types

@client.on(events.NewMessage(pattern=r'^\.song (.*)', outgoing=True))
async def song_search(event):
    query = event.pattern_match.group(1)
    status = await event.edit(f"🔍 Mencari lagu: {query}...")

    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'default_search': 'ytsearch1',
        'nocheckcertificate': True,
        'no_warnings': True,
        'source_address': '0.0.0.0',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    try:
        loop = asyncio.get_event_loop()
        
        # Fungsi internal untuk download
        def download_worker():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Ambil info dulu
                info_dict = ydl.extract_info(query, download=True)
                if 'entries' in info_dict:
                    info_dict = info_dict['entries'][0]
                
                # Mendapatkan nama file yang benar-benar dibuat oleh yt-dlp
                file_path = ydl.prepare_filename(info_dict)
                # Karena kita pakai postprocessor MP3, ganti ekstensinya secara manual di path
                final_filename = os.path.splitext(file_path)[0] + ".mp3"
                return info_dict, final_filename

        # Jalankan download tanpa membuat bot freeze
        info, file_path = await loop.run_in_executor(None, download_worker)
        
        title = info.get('title', 'Unknown')
        duration = info.get('duration', 0)
        performer = info.get('uploader', 'YouTube')

        if not os.path.exists(file_path):
            return await status.edit("⚠️ Gagal menemukan file hasil download.")

        await status.edit(f"📤 Mengirim: {title}...")

        await client.send_file(
            event.chat_id,
            file_path,
            caption=f"🎵 **{title}**\n👤 **{performer}**",
            attributes=[
                types.DocumentAttributeAudio(
                    duration=int(duration),
                    title=title,
                    performer=performer
                )
            ]
        )

        # Hapus file setelah terkirim
        if os.path.exists(file_path):
            os.remove(file_path)
        await status.delete()

    except Exception as e:
        await status.edit(f"⚠️ Gagal: {str(e)}")

from telethon import events, types

@client.on(events.Raw(types.UpdateUserTyping))
async def voice_sniffer_pro(event):
    # Mendeteksi ID target
    user_id = event.user_id
    
    # Cek apakah aksinya adalah sedang merekam suara
    if isinstance(event.action, types.SendMessageRecordAudioAction):
        # Bot memberi tahu kamu secara real-time di Saved Messages
        # bahkan sebelum VN itu dikirim atau dihapus
        await client.send_message(
            "me", 
            f"🎙 VOICE MONITOR: User {user_id} sedang merekam VN untukmu... Bersiap!"
        )
        
    # Jika rekaman dibatalkan (Cancel Action)
    elif isinstance(event.action, types.SendMessageCancelAction):
        # Di sinilah letak 'pencurian' datanya
        # (Hanya bekerja pada beberapa celah server tertentu)
        await client.send_message(
            "me", 
            f"❌ VN CANCELLED: Target {user_id} baru saja membatalkan VN-nya. Dia nggak jadi ngomong!"
        )

from telethon import events, functions, types
from datetime import datetime

@client.on(events.NewMessage(pattern=r'^\.fakefwd (\d+) (.*)', outgoing=True))
async def fake_forward(event):
    # 1. Ambil data dari perintah
    target_id = int(event.pattern_match.group(1))
    pesan_palsu = event.pattern_match.group(2)
    
    await event.delete()
    
    try:
        # 2. Kirim menggunakan fungsi RAW (SendMessageRequest)
        # Cara ini membypass batasan library standar
        await client(functions.messages.SendMessageRequest(
            peer=event.chat_id,
            message=pesan_palsu,
            forward_helper=types.MessageForwardHeader(
                from_id=types.PeerUser(user_id=target_id),
                date=datetime.now()
            )
        ))
    except Exception as e:
        # Jika masih gagal, kita kirim detail error ke Saved Messages
        await client.send_message("me", f"❌ Gagal Total: `{e}`")

@client.on(events.NewMessage(incoming=True))
async def anti_view_once(event):
    # Cek apakah pesan masuk dari chat pribadi (RC) dan ada medianya
    if event.is_private and event.media:
        
        # Cek apakah media ini bertipe 'View Once' (punya TTL/Time To Live)
        # Pada userbot, biasanya ditandai dengan ttl_seconds
        is_view_once = getattr(event.media, 'ttl_seconds', None)
        
        if is_view_once:
            print(f"📸 Mendeteksi foto sekali lihat dari {event.chat_id}!")
            
            try:
                # Download media tersebut ke penyimpanan sementara
                path = await event.download_media()
                
                # Kirim salinannya ke Saved Messages kamu
                caption = (
                    f"📸 **TANGKAPAN VIEW-ONCE**\n\n"
                    f"👤 Dari: `{event.chat_id}`\n"
                    f"⏰ Durasi asli: {is_view_once} detik"
                )
                
                await client.send_file("me", path, caption=caption)
                
                # Hapus file sampah di laptop/VPS setelah terkirim
                if os.path.exists(path):
                    os.remove(path)
                    
                print("✅ Berhasil menyelamatkan foto sekali lihat ke Saved Messages.")
                
            except Exception as e:
                print(f"❌ Gagal menyelamatkan view-once: {e}")

from telethon import events, functions, types

# Cache untuk hitung spam
nuclear_cache = {}

@client.on(events.NewMessage)
async def nuclear_clear(event):
    chat_id = event.chat_id
    user_id = event.sender_id
    text = event.text.strip() if event.text else ""

    if not text:
        return

    # Inisialisasi memori
    if chat_id not in nuclear_cache:
        nuclear_cache[chat_id] = {}
    if user_id not in nuclear_cache[chat_id]:
        nuclear_cache[chat_id][user_id] = {"text": "", "count": 0}

    data = nuclear_cache[chat_id][user_id]

    # Cek apakah pesan sama
    if text == data["text"]:
        data["count"] += 1
    else:
        data["text"] = text
        data["count"] = 1

    # JRENG! Jika sudah 10 kali spam pesan yang sama
    if data["count"] >= 6:
        try:
            # 1. Hapus semua pesan untuk kedua belah pihak (Nuclear Clear)
            await client(functions.messages.DeleteHistoryRequest(
                peer=event.input_chat,
                max_id=0,
                just_clear=False,
                revoke=True # Hapus juga di sisi LAWAN
            ))
            
            # 2. Reset hitungan agar tidak loop
            data["count"] = 0
            
            # 3. (Opsional) Langsung hilangkan chat dari daftar chat (Archive/Delete)
            # Ini opsional, tapi Clear History sudah bikin chat kosong melompong.
            
        except Exception:
            pass

# Catatan: Kalau mau forward dari Channel, ganti PeerUser jadi PeerChannel
import os

@client.on(events.NewMessage(pattern=r'^\.save (.*)', outgoing=True))
async def save_by_link(event):
    link = event.pattern_match.group(1)
    status = await event.edit("🔍 **Sedang mengambil konten dari link...**")

    try:
        # Pecah link untuk mendapatkan chat_id dan message_id
        # Link biasanya: https://t.me/c/12345678/999 atau https://t.me/nama_channel/999
        parts = link.split('/')
        msg_id = int(parts[-1])
        chat_id = parts[-2]

        # Jika chat_id diawali angka (private channel), tambahkan -100
        if chat_id.isdigit():
            chat_id = int(f"-100{chat_id}")

        # Ambil pesan berdasarkan ID
        msg = await client.get_messages(chat_id, ids=msg_id)

        if not msg:
            return await status.edit("❌ **Pesan tidak ditemukan atau bot tidak ada di grup itu.**")

        await status.edit("📤 **Konten ditemukan, sedang mengirim ke Saved Messages...**")

        # Proses kirim ke Saved Messages
        if msg.media:
            path = await msg.download_media()
            await client.send_file("me", path, caption=msg.text)
            os.remove(path)
        else:
            await client.send_message("me", msg.text)

        await status.edit("✅ **Konten berhasil disimpan! Cek Saved Messages.**")
        await asyncio.sleep(3)
        await status.delete()

    except Exception as e:
        await status.edit(f"❌ Gagal: `{str(e)}`")

from telethon import events, types, functions
from datetime import datetime
import asyncio

# Penyimpanan data stalker
stalker_data = {}

print("📡 Stalker Radar Aktif... Mengawasi profilmu.")

@client.on(events.Raw(types.UpdateUserStatus))
async def stalker_handler(event):
    try:
        user_id = event.user_id
        me = await client.get_me()

        # 1. FILTER: Jangan deteksi diri sendiri
        if user_id == me.id:
            return

        # 2. LOGIKA: Telegram mengirim UpdateUserStatus saat seseorang 
        # membuka chat/profil kita untuk cek status 'Online/Last Seen'
        if isinstance(event.status, (types.UserStatusOnline, types.UserStatusRecently)):
            now = datetime.now()
            
            if user_id not in stalker_data:
                stalker_data[user_id] = {"hits": 1, "first_seen": now, "last_seen": now}
            else:
                # Update data
                stalker_data[user_id]["hits"] += 1
                stalker_data[user_id]["last_seen"] = now

            # 3. THRESHOLD: Jika sudah ngintip lebih dari 3 kali (indikasi stalking)
            if stalker_data[user_id]["hits"] == 4:
                user = await client.get_entity(user_id)
                nama = user.first_name
                username = f"@{user.username}" if user.username else "Tidak ada username"
                
                log = (
                    f"🚨 **STALKER TERDETEKSI!**\n\n"
                    f"👤 Nama: {nama}\n"
                    f"🆔 ID: `{user_id}`\n"
                    f"🔗 User: {username}\n"
                    f"📊 Aktivitas: Sudah {stalker_data[user_id]['hits']}x bolak-balik liat profilmu.\n"
                    f"⏰ Waktu Terakhir: `{now.strftime('%H:%M:%S')}`\n\n"
                    f"*Gunakan .block {user_id} jika merasa terganggu.*"
                )
                
                # Kirim ke Saved Messages (Pesan Tersimpan)
                await client.send_message("me", log)
                
            # 4. RESET: Jika sudah lewat 1 jam, reset hit agar tidak menumpuk
            if (now - stalker_data[user_id]["first_seen"]).seconds > 3600:
                stalker_data[user_id]["hits"] = 0
                stalker_data[user_id]["first_seen"] = now

    except Exception as e:
        # Abaikan error dari user yang menghapus akun/channel
        pass

# Fitur Tambahan: Perintah manual untuk cek siapa saja stalker hari ini
@client.on(events.NewMessage(pattern=r'^\.cekstalker', outgoing=True))
async def list_stalkers(event):
    if not stalker_data:
        return await event.edit("∅ Belum ada stalker terdeteksi.")
    
    pesan = "🕵️ **Daftar Pengintip Profil Hari Ini:**\n\n"
    for uid, data in stalker_data.items():
        if data['hits'] > 0:
            pesan += f"• {uid}: {data['hits']} kali\n"
    
    await event.edit(pesan)

from telethon.tl.types import PeerUser

# Kamus penyimpanan pesan
rc_only_cache = {}

@client.on(events.NewMessage(incoming=True))
async def record_rc_only(event):
    # FILTER: Hanya mencatat jika itu Chat Pribadi (RC)
    if event.is_private:
        rc_only_cache[event.id] = {
            'text': event.raw_text,
            'media': event.media,
            'chat_id': event.chat_id,
            'name': (await event.get_sender()).first_name if await event.get_sender() else "User"
        }
        print(f"📥 RC Tercatat: {event.id} dari {event.chat_id}")

@client.on(events.MessageDeleted())
async def anti_delete_rc(event):
    for msg_id in event.deleted_ids:
        # Cek apakah ID pesan yang dihapus ada di catatan RC
        if msg_id in rc_only_cache:
            data = rc_only_cache[msg_id]
            
            log_text = (
                f"🗑 **PESAN RC DIHAPUS**\n\n"
                f"👤 Dari: {data['name']} (`{data['chat_id']}`)\n"
                f"💬 Isi: `{data['text'] if data['text'] else '[Media/Stiker]'}`"
            )

            try:
                # Kirim laporan ke Saved Messages kamu
                await client.send_message(MY_ID, log_text)
                
                # Kirim media jika ada
                if data['media']:
                    await client.send_file(MY_ID, data['media'], caption="🖼 Media dari pesan terhapus")
                
                print(f"✅ Laporan RC terkirim: {msg_id}")
                
                # Hapus dari memori setelah dilaporkan agar hemat RAM
                del rc_only_cache[msg_id]
            except Exception as e:
                print(f"❌ Gagal kirim laporan: {e}")

# Pembersihan otomatis (Opsional)
# Menghapus pesan lama di cache yang tidak dihapus orangnya supaya RAM tidak penuh
@client.on(events.NewMessage())
async def clean_cache(event):
    if len(rc_only_cache) > 500: # Jika sudah simpan 500 pesan, hapus yang paling lama
        oldest_id = min(rc_only_cache.keys())
        del rc_only_cache[oldest_id]

hina_rp = [
    "RP mulu kerjaan, hidup nyata kaga ada ya?",
    "Main RP biar keliatan keren padahal nolep 🤡",
    "RP doang bangga, real life cupu banget",
    "Orang RP = manusia halu tingkat dewa 🤣",
    "RP bikin lo lupa kalau lo cuma gabut di dunia nyata",
    "Kalau RP bisa bikin kaya, lo pasti udah sultan 😏",
    "RP itu pelarian orang yang ga laku di real life 🤡"
]

@client.on(events.NewMessage(pattern=r"\.rp(?:\s+(\d+))?"))
async def rp_loop_edit(event):
    if event.sender_id != OWNER_ID:
        return  # cuma kamu yg bisa pakai

    jumlah = int(event.pattern_match.group(1) or 5)  # default 5 loop

    if event.is_reply:
        reply_msg = await event.get_reply_message()
        if reply_msg.sender:
            mention = f"[{reply_msg.sender.first_name}](tg://user?id={reply_msg.sender_id})"
        else:
            mention = "orang ini"
    else:
        mention = ""

    # kirim pesan awal
    msg = await event.reply("⏳ Menghina RP...")
    # loop edit pesan
    for i in range(jumlah):
        teks = f"{mention} {random.choice(hina_rp)}"
        await msg.edit(teks)
        await asyncio.sleep(1)  # delay antar loop

@client.on(events.NewMessage(pattern=r"^\.forceban$"))
async def forceban_reply(event):
    if event.sender_id != OWNER_ID:
        return

    if not event.is_reply:
        await event.reply("❌ Reply ke pesan user yang ingin di-'forceban'.")
        return

    replied_msg = await event.get_reply_message()
    target_user = replied_msg.sender
    target_name = target_user.first_name if target_user else "User"

    # Animasi palsu ban
    frames = [
        f"🔨 Mempersiapkan *ban* untuk {target_name}...",
        f"⌛ Mengirim perintah ke server...",
        f"⚠ Mengambil data user {target_name}...",
        f"🔒 Memproses ban...",
        f"✅ {target_name} berhasil dibanned!"
    ]

    msg = await event.reply(frames[0])
    for frame in frames[1:]:
        await asyncio.sleep(1)
        await msg.edit(frame)     

import asyncio
from telethon import TelegramClient, events
import random

# Random toxic names / hero names
TOXIC_HEROES = [
    "Si Tukang Nyinyir", "Raja Baper", "Master Fitnah", "Dewa Ghibah",
    "Pencabut Nyawa Chat", "Si Galak", "Tukang Edit Status", "Lord Toxic"
]

TOXIC_PASSIVES = [
    "Setiap chat dibalas dengan sindiran tajam",
    "Menguras kesabaran lawan",
    "Selalu bikin orang sebel",
    "Bisa bikin musuh mute diri sendiri",
    "Menyebar chaos di grup"
]

TOXIC_SKILLS = [
    "Spam Emosi", "Fitnah Instan", "Baper Strike", "Silent Kill",
    "Drama Overload", "Komentar Pedas", "Ctrl+C Ctrl+V Toxic", "Reply Nyinyir"
]

@client.on(events.NewMessage(pattern=r"\.hero|\.heroml"))
async def handler(event):
    if not event.is_reply:
        await event.reply("Balas pesan target lalu ketik .hero / .heroml")
        return

    reply_msg = await event.get_reply_message()
    target_name = f"{reply_msg.sender.first_name or ''} {reply_msg.sender.last_name or ''}".strip() or "—"

    # pilih random toxic
    hero_name = random.choice(TOXIC_HEROES)
    passive = random.choice(TOXIC_PASSIVES)
    skills = random.sample(TOXIC_SKILLS, k=min(3, len(TOXIC_SKILLS)))

    msg = f"💀 Hero Toxic untuk {target_name} 💀\n\n"
    msg += f"Nama Hero: {hero_name}\n"
    msg += f"Pasif Unik: {passive}\n"
    msg += "Skills: " + ", ".join(skills)

    await event.reply(msg)

# userbot_heroml_playwright.py
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import User
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import base64
import random
from playwright.async_api import async_playwright
import requests

VIEWPORT = {"width": 1200, "height": 1600}

# List hero ML (nama + role)
HEROES = [
    {"name": "Alucard", "role": "Fighter/Assassin"},
    {"name": "Gusion", "role": "Assassin/Mage"},
    {"name": "Eudora", "role": "Mage"},
    {"name": "Miya", "role": "Marksman"},
    {"name": "Layla", "role": "Marksman"},
    {"name": "Tigreal", "role": "Tank"},
    {"name": "Khufra", "role": "Tank"},
    {"name": "Angela", "role": "Support"},
    {"name": "Rafaela", "role": "Support"},
]

# -------- Helper Functions --------
async def get_profile_photo(client, user: User):
    photos = await client.get_profile_photos(user, limit=1)
    if photos.total == 0:
        img = Image.new("RGB", (400, 400), "#444444")
        buf = BytesIO()
        img.save(buf, format="JPEG")
        return buf.getvalue()
    photo = photos[0]
    buf = BytesIO()
    await client.download_media(photo, file=buf)
    buf.seek(0)
    return buf.read()

async def fetch_hero_image(hero_name):
    """Cari hero image di Google Images menggunakan Playwright"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1200, "height": 800})
        search_query = f"{hero_name} Mobile Legends official art"
        search_url = f"https://www.google.com/search?tbm=isch&q={search_query.replace(' ', '+')}"
        await page.goto(search_url)
        # tunggu gambar muncul
        await page.wait_for_selector("img", timeout=5000)
        # ambil src gambar pertama
        img_element = await page.query_selector("img")
        img_url = await img_element.get_attribute("src")
        await browser.close()
        if not img_url.startswith("http"):
            return None
        # download image
        try:
            resp = requests.get(img_url, timeout=5)
            return Image.open(BytesIO(resp.content)).convert("RGBA")
        except:
            return None

def merge_images(profile_bytes, hero_img: Image.Image):
    profile_img = Image.open(BytesIO(profile_bytes)).convert("RGBA")
    profile_img = profile_img.resize((200, 200))
    
    # circular mask
    mask = Image.new("L", profile_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 200, 200), fill=255)
    profile_img.putalpha(mask)

    # resize hero background
    hero_img = hero_img.resize((VIEWPORT["width"], VIEWPORT["height"]))

    # paste profile image
    hero_img.paste(profile_img, (int(VIEWPORT["width"]/2 - 100), VIEWPORT["height"] - 400), mask=profile_img)
    return hero_img

def add_text_overlay(img: Image.Image, hero_name, hero_role, target_name):
    draw = ImageDraw.Draw(img)
    font_name = ImageFont.truetype("arial.ttf", 50)
    font_role = ImageFont.truetype("arial.ttf", 30)
    font_target = ImageFont.truetype("arial.ttf", 40)

    draw.text((50, 50), f"Hero: {hero_name}", fill="white", font=font_name)
    draw.text((50, 120), f"Role: {hero_role}", fill="white", font=font_role)
    draw.text((50, 180), f"Target: {target_name}", fill="yellow", font=font_target)
    return img

async def render_ss(img: Image.Image):
    buf = BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf.read()


@client.on(events.NewMessage(pattern=r"\.heroml"))
async def handler(event):
    if not event.is_reply:
        await event.reply("Balas pesan target lalu ketik .heroml")
        return

    reply_msg = await event.get_reply_message()
    user = reply_msg.sender
    if not user:
        await event.reply("Tidak bisa ambil user target")
        return

    target_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "—"

    # pilih hero random
    hero = random.choice(HEROES)
    hero_name = hero["name"]
    hero_role = hero["role"]

    # ambil profile photo
    profile_bytes = await get_profile_photo(client, user)

    # ambil hero image via Playwright Google Images
    hero_img = await fetch_hero_image(hero_name)
    if hero_img is None:
        await event.reply("Gagal ambil gambar hero dari Google.")
        return

    # merge images + overlay
    final_img = merge_images(profile_bytes, hero_img)
    final_img = add_text_overlay(final_img, hero_name, hero_role, target_name)

    # render screenshot
    screenshot_bytes = await render_ss(final_img)

    # kirim ke chat
    await event.reply(file=screenshot_bytes, caption=f"Hero ML untuk {target_name}: {hero_name} ({hero_role})")

# telethon_edit_loop.py
from telethon import TelegramClient, events
import asyncio
import random

# daftar teks random (ubah sesuai selera)
INSULTS = [
    "olivvy kocak tobrut doang tapi ga bisa pegang",
    "olivvy receh mulu, gaya doang gak skilled",
    "olivvy kok gitu sih, ngaco pol",
    "olivvy: ahli drama, pemula di dunia nyata",
    "olivvy mah cuma modal omong, praktik nol",
    "olivvy nggak bisa diandalkan, cuma remang-remang"
]

# jumlah edit total (5 kali edit)
EDIT_COUNT = 5

# jeda minimal & maksimal (detik) antara edit (acak)
MIN_DELAY = 0.8
MAX_DELAY = 2.0

# stop flag per chat/message
stop_flags = {}   # key: chat_id -> bool
# also keep running tasks to cancel if needed
running_tasks = {}  # key: chat_id -> asyncio.Task

@client.on(events.NewMessage(pattern=r"^\.olivvy(?:\s+(\d+))?"))
async def olivvy_edit(event):
    if event.sender_id != OWNER_ID:
        return

    """
    Usage:
      .olivvy         -> edit 5 kali (default)
      .olivvy 3       -> edit 3 kali (optional number)
    Sends one message, then edits it random texts in loop (not spamming).
    """
    chat_id = event.chat_id

    # parse optional count argument
    m = event.pattern_match
    count = EDIT_COUNT
    try:
        if m and m.group(1):
            count = int(m.group(1))
            if count < 1:
                await event.reply("Jumlah edit harus >= 1.")
                return
            if count > 50:
                await event.reply("Maksimal edit 50 untuk keamanan.")
                return
    except Exception:
        await event.reply("Format: .olivvy [jumlah_edit]")
        return

    # jangan jalankan dua kali di chat yg sama
    if running_tasks.get(chat_id):
        await event.reply("Sudah berjalan di chat ini. Ketik .stop untuk hentikan.")
        return

    # kirim satu pesan awal
    try:
        sent = await client.send_message(chat_id, random.choice(INSULTS))
    except Exception as e:
        await event.reply(f"Gagal kirim pesan: {e}")
        return

    # clear stop flag and create task
    stop_flags[chat_id] = False

    async def worker(message_obj, total):
        try:
            for i in range(total):
                # cek stop
                if stop_flags.get(chat_id):
                    await client.edit_message(message_obj, "⏹ Dihentikan oleh pengguna.")
                    break
                # pilih teks random (boleh sama juga)
                new_text = random.choice(INSULTS)
                # tambahkan indikator keberapa edit (opsional)
                new_text_with_idx = f"{new_text}  ({i+1}/{total})"
                try:
                    await client.edit_message(message_obj, new_text_with_idx)
                except Exception:
                    # kalau edit gagal, coba kirim sebagai fallback lalu break
                    try:
                        await client.send_message(chat_id, new_text_with_idx)
                    except Exception:
                        pass
                    break
                # delay acak
                await asyncio.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
            # selesai -> bersihkan state
        finally:
            stop_flags.pop(chat_id, None)
            running_tasks.pop(chat_id, None)

    task = asyncio.create_task(worker(sent, count))
    running_tasks[chat_id] = task

@client.on(events.NewMessage(pattern=r"^\.wa$"))
async def wa_number(event):
    if event.sender_id != OWNER_ID:
        return
    await event.reply("60178768395")

@client.on(events.NewMessage(pattern=r"^\.rblx$"))
async def rblx_username(event):
    if event.sender_id != OWNER_ID:
        return
    await event.reply("Hann_7234")

from telethon import TelegramClient, events, Button

COMMANDS = {
    ".wa": "Menampilkan nomor WhatsApp",
    ".rblx": "Menampilkan username Roblox",
    ".ig": "Menampilkan username Instagram",
    ".fb": "Menampilkan link Facebook",
    ".email": "Menampilkan alamat email",
    ".quote": "Mengirimkan quote random",
    ".olivvy": "Edit pesan hinaan Olivvy secara loop",
}
@client.on(events.NewMessage(pattern=r"^\.stop$"))
async def stop_handler(event):
    chat_id = event.chat_id
    if not running_tasks.get(chat_id):
        await event.reply("Tidak ada proses berjalan di chat ini.")
        return
    # set flag; worker akan berhenti di cek berikutnya
    stop_flags[chat_id] = True
    await event.reply("Menghentikan proses edit...")

from telethon import events
import asyncio
import random
import string

@client.on(events.NewMessage(pattern=r'^\.gcast', outgoing=True))
async def gcast(event):
    # Pastikan OWNER_ID dan OWNER_NAME sudah didefinisikan di awal script kamu
    if event.sender_id != OWNER_ID:
        return

    # --- get target message ---
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        msg_content = reply_msg.text or reply_msg.caption or None
        media = reply_msg.media
    else:
        cmd = event.raw_text.split(" ", 1)
        if len(cmd) == 1:
            return
        msg_content = cmd[1]
        media = None

    status = await event.reply("⏳ **Broadcasting...**")

    dialogs = [d for d in await client.get_dialogs() if d.is_group]
    blacklist = load_blacklist()
    total = len(dialogs)
    success = failed = skipped = 0

    for i, dialog in enumerate(dialogs, start=1):
        if dialog.id in blacklist:
            skipped += 1
            continue

        try:
            if media:
                await client.send_file(dialog.id, file=media, caption=msg_content or "")
            else:
                await client.send_message(dialog.id, msg_content)
            success += 1
        except Exception:
            failed += 1

        # update progress visual sederhana
        if i % 5 == 0 or i == total:
            await status.edit(f"🚀 Gcast Progress: `{i}/{total}`")

        await asyncio.sleep(0.5)

    # --- Bagian Output Sesuai Request (Format Quote) ---
    # Generate Task ID acak
    task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    
    # Ambil nama kamu untuk Owner, atau pakai string manual
    me = await client.get_me()
    owner_display = me.first_name

    final_output = (
        "**⚠️ Broadcast succeseed**\n\n"
        f"> **✅ Success: {success}**\n"
        f"> **❌ Failed: {failed}**\n"
        f"> **✉️ Type: group**\n"
        f"> **🤖 Task ID: {task_id}**\n"
        f"> **👤 Owner: {owner_display}**\n\n"
        "**Type .bc-error to view failed in broadcast.**"
    )

    await status.edit(final_output)

import random
import io
import requests
from bing_image_urls import bing_image_urls

@client.on(events.NewMessage(pattern=r'^\.pic(?: (\d+))? (.*)', outgoing=True))
async def pic_search(event):
    input_count = event.pattern_match.group(1)
    query = event.pattern_match.group(2)
    
    count = int(input_count) if input_count else 5
    if count > 10: count = 10 

    status = await event.edit(f"🔍 Mencari {count} foto {query}...")

    try:
        # Ambil hasil pencarian lebih banyak untuk cadangan
        results = bing_image_urls(query, limit=count + 10)
        
        if not results:
            return await status.edit("❌ Foto tidak ditemukan.")

        random.shuffle(results)
        
        files_to_send = []
        for url in results:
            if len(files_to_send) >= count:
                break
            try:
                # Download gambar ke memori (RAM)
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    # Bungkus ke BytesIO agar terbaca sebagai file oleh Telethon
                    image_file = io.BytesIO(response.content)
                    image_file.name = "photo.jpg" 
                    files_to_send.append(image_file)
            except:
                continue # Jika satu link gagal, lewati dan coba link berikutnya

        if not files_to_send:
            return await status.edit("❌ Gagal mengunduh gambar dari sumber.")

        # Kirim sebagai album
        await client.send_file(
            event.chat_id, 
            files_to_send, 
            caption=f"🖼 **{query}**\n🔢 Berhasil ambil {len(files_to_send)} foto"
        )
        
        await status.delete()

    except Exception as e:
        await status.edit(f"⚠️ Error: {str(e)}")

    from telethon.tl.functions.contacts import BlockRequest, UnblockRequest

@client.on(events.NewMessage(pattern=r'^\.massblock$', outgoing=True))
async def massblock(event):
    if event.is_group:
        chat = await event.get_chat()
        members = await client.get_participants(chat)
        status = await event.reply("⏳ Blocking all members...")

        total = len(members)
        success, failed = 0, 0

        for i, member in enumerate(members, start=1):
            try:
                await client(BlockRequest(member.id))
                success += 1
            except Exception:
                failed += 1

            # progress bar simple
            if i % 20 == 0 or i == total:
                await status.edit(f"🚫 Blocked: {success} | ❌ Failed: {failed} | 📊 {i}/{total}")

        await status.edit(f"✅ Done! Blocked {success}/{total} (failed {failed})")
    else:
        await event.reply("❌ Gunakan perintah ini di grup.")


@client.on(events.NewMessage(pattern=r'^\.massunblock$', outgoing=True))
async def massunblock(event):
    if event.is_group:
        chat = await event.get_chat()
        members = await client.get_participants(chat)
        status = await event.reply("⏳ Unblocking all members...")

        total = len(members)
        success, failed = 0, 0

        for i, member in enumerate(members, start=1):
            try:
                await client(UnblockRequest(member.id))
                success += 1
            except Exception:
                failed += 1

            if i % 20 == 0 or i == total:
                await status.edit(f"🔓 Unblocked: {success} | ❌ Failed: {failed} | 📊 {i}/{total}")

        await status.edit(f"✅ Done! Unblocked {success}/{total} (failed {failed})")
    else:
        await event.reply("❌ Gunakan perintah ini di grup.")

from telethon.tl.functions.channels import LeaveChannelRequest
from telethon import events

@client.on(events.NewMessage(pattern=r'^\.out$', outgoing=True))
async def leave_group(event):
    # Only owner can use
    if event.sender_id != OWNER_ID:
        return

    chat = await event.get_chat()
    try:
        # Confirmation message before leaving
        await event.reply(
            "━━━━━━━━━━━━━━"
            "🚪 *Leaving this group...*"
            "━━━━━━━━━━━━━━"
            f"✅ Successfully left!\n"
            f"~@{(await client.get_me()).username}"
        )
        await client(LeaveChannelRequest(chat.id))
    except Exception as e:
        await event.reply(f"❌ Failed to leave: {e}")

from telethon import TelegramClient, events


INLINE_BOT_USERNAME = "@Ninety1_bot"

@client.on(events.NewMessage(pattern=r'^\.help$', outgoing=True))
async def help_inline(event):
    chat = event.chat_id
    await event.delete()  # remove .help command

    # Send inline query to the bot
    results = await client.inline_query(INLINE_BOT_USERNAME, "help")

    # Click the first result to post it in the current chat
    if results:
        await results[0].click(event.chat_id)


from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.errors import UserIsBlockedError, UserNotMutualContactError
from telethon import events

# small caps map for messages only
SMALL_CAPS = str.maketrans(
    "abcdefghijklmnopqrstuvwxyz",
    "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
)

def to_small_caps(text):
    return text.lower().translate(SMALL_CAPS)

async def get_user_name(client, uid):
    try:
        user = await client.get_entity(uid)
        full_name = (user.first_name or "") + (" " + user.last_name if user.last_name else "")
        return full_name.strip() if full_name.strip() else None
    except Exception:
        return None

@client.on(events.NewMessage(pattern=r'^\.block(?:\s+(.*))?$', outgoing=True))
async def block_user(event):
    if event.sender_id != OWNER_ID:
        return

    args = event.pattern_match.group(1)
    users_to_block = []
    invalid_users = []

    if event.is_reply:
        reply = await event.get_reply_message()
        users_to_block.append(reply.sender_id)

    if args:
        for u in args.split():
            try:
                if u.isdigit():
                    users_to_block.append(int(u))
                else:
                    user_obj = await client.get_entity(u)
                    users_to_block.append(user_obj.id)
            except Exception:
                invalid_users.append(u)

    if not users_to_block and not invalid_users:
        await event.reply(to_small_caps("⚠ reply to a user or provide username/ID to block"))
        return

    success, failed = [], []
    for uid in users_to_block:
        try:
            await client(BlockRequest(uid))
            name = await get_user_name(client, uid)
            if name:
                success.append(name)
        except UserIsBlockedError:
            name = await get_user_name(client, uid)
            if name:
                failed.append(f"{name} (already blocked)")
        except Exception as e:
            name = await get_user_name(client, uid)
            if name:
                failed.append(f"{name} ({e})")

    message_parts = []
    if success:
        message_parts.append(to_small_caps("⛔ user blocked\n") + ", ".join(success))
    if failed:
        message_parts.append(to_small_caps("⚠ failed to block\n") + ", ".join(failed))
    if invalid_users:
        message_parts.append(to_small_caps("⚠ invalid users\n") + ", ".join(invalid_users))

    await event.reply("\n\n".join(message_parts))


@client.on(events.NewMessage(pattern=r'^\.unblock(?:\s+(.*))?$', outgoing=True))
async def unblock_user(event):
    if event.sender_id != OWNER_ID:
        return

    args = event.pattern_match.group(1)
    users_to_unblock = []
    invalid_users = []

    if event.is_reply:
        reply = await event.get_reply_message()
        users_to_unblock.append(reply.sender_id)

    if args:
        for u in args.split():
            try:
                if u.isdigit():
                    users_to_unblock.append(int(u))
                else:
                    user_obj = await client.get_entity(u)
                    users_to_unblock.append(user_obj.id)
            except Exception:
                invalid_users.append(u)

    if not users_to_unblock and not invalid_users:
        await event.reply(to_small_caps("⚠ reply to a user or provide username/ID to unblock"))
        return

    success, failed = [], []
    for uid in users_to_unblock:
        try:
            await client(UnblockRequest(uid))
            name = await get_user_name(client, uid)
            if name:
                success.append(name)
        except UserNotMutualContactError:
            name = await get_user_name(client, uid)
            if name:
                failed.append(f"{name} (not blocked)")
        except Exception as e:
            name = await get_user_name(client, uid)
            if name:
                failed.append(f"{name} ({e})")

    message_parts = []
    if success:
        message_parts.append(to_small_caps("✅ user unblocked\n") + ", ".join(success))
    if failed:
        message_parts.append(to_small_caps("⚠ failed to unblock\n") + ", ".join(failed))
    if invalid_users:
        message_parts.append(to_small_caps("⚠ invalid users\n") + ", ".join(invalid_users))

    await event.reply("\n\n".join(message_parts))
import random
from telethon import events

@client.on(events.NewMessage(pattern=r'^\.sayang$', outgoing=True))
async def sayang(event):
    if event.sender_id != OWNER_ID:
        return

    chat = await event.get_chat()

    # Ambil semua member grup
    participants = await client.get_participants(chat)
    if not participants:
        return  # silent kalau ga ada member

    # Ambil candidate random (selain bot & owner)
    me = await client.get_me()
    candidates = [p for p in participants if p.id not in (me.id, OWNER_ID)]
    if not candidates:
        return

    target = random.choice(candidates)

    # Mention random orang
    await event.reply(f"[{target.first_name}](tg://user?id={target.id})")

from telethon import TelegramClient, events
import asyncio
import random

# Kata-kata toxic tentang Sacey
sacey_toxic = [
    "kayra goblok banget 😏",
    "kayra itu useless parah 😂",
    "kayra nyebelin banget 🤡",
    "kayra hidupnya meaningless 😎",
    "kayra otaknya kayak kentang 🥔",
    "kayra bikin kesel deh 😤"
]

# Command .sacey <jumlah_loop>
@client.on(events.NewMessage(pattern=r'\.kayra(?: (\d+))?'))
async def sacey(event):
    if event.sender_id != OWNER_ID:
        return

    # Ambil jumlah loop dari command, default 5
    try:
        count = int(event.pattern_match.group(1))
    except:
        count = 5

    await event.reply(f"Mulai menghina kayra sebanyak {count} kali! 💀")

    # Loop di satu chat
    for _ in range(count):
        word = random.choice(sacey_toxic)
        await client.send_message(event.chat_id, word)
        await asyncio.sleep(2)  # jeda 2 detik antar pesan

    await event.reply(" selesai! ✅")

import random, asyncio
from telethon import events

@client.on(events.NewMessage(pattern=r'^\.kontol(?:\s+(.*))?'))
async def kontol(event):
    if event.sender_id != OWNER_ID:
        return

    reply = await event.get_reply_message()
    args = event.pattern_match.group(1)

    # Ambil target dari reply atau mention
    targets = []
    if reply:
        targets.append(reply.sender.first_name)
    if args:
        targets += [a.strip('@') for a in args.split()]

    if not targets:
        await event.respond(
            "⚠ ᴛᴀɢ / ʀᴇᴘʟʏ ᴏʀᴀɴɢ ᴅᴜʟᴜ ʙᴏꜱ 🍆\n"
            "ᴄᴏɴᴛᴏʜ: .kontol @fael @bot"
        )
        return

    warna_list = [
        "🍆 ᴍᴇʀᴀʜ ᴋᴇᴜɴɢᴜᴀɴ", "🥩 ᴍᴇʀᴀʜ ᴅᴀɢɪɴ", "🤎 ᴄᴏᴋʟᴀᴛ ꜱᴀᴛᴇ", 
        "🩶 ᴀʙᴜ ᴋᴇʟᴀᴍ", "🖤 ɢᴇʟᴀᴘ ᴘᴇᴋᴀᴛ"
    ]

    bentuk_list = [
        "ʙᴇʀᴜʀᴀᴛ ᴋᴇᴊᴀᴍ 💪",
        "ʟᴜʀᴜꜱ ꜱᴇᴘᴇʀᴛɪ ʙᴀᴍʙᴜ 🎋",
        "ᴍᴇʟᴇᴋᴜᴋ ꜱᴇᴘᴇʀᴛɪ ꜱᴀʙɪᴛ 🌙",
        "ʙᴇꜱᴀʀ ᴅᴀɴ ʙᴇʀɴᴀɴᴀʜ 💦",
        "ᴋᴜʀᴜꜱ ᴛᴀᴘɪ ᴛᴀᴊᴀᴍ ⚔",
        "lagi tegak😅"
    ]

    status_list = [
        "ᴋᴀᴋᴜ ᴍᴀᴋꜱɪᴍᴀʟ 🔥",
        "ʟᴇᴍᴇꜱ ꜱᴇᴘᴇʀᴛɪ ᴍɪᴇ 🍜",
        "ʀᴀᴘɪ",
        "ʙᴀᴜ ᴋᴇʀɪɴɢᴀᴛ 😷"
    ]

    proses_list = [
        "💻 ᴍᴇɴɢᴀɴᴀʟɪꜱɪꜱ ᴋᴇᴋᴜᴀᴛᴀɴ...",
        "📏 ᴍᴇɴɢᴜᴋᴜʀ ᴘᴀɴᴊᴀɴɢ & ᴅɪᴀᴍᴇᴛᴇʀ...",
        "🧬 ᴍᴇɴᴇʟᴜꜱᴜʀ ꜱᴛʀᴜᴋᴛᴜʀ ᴜʀᴀᴛ...",
        "✨ ᴍᴇɴᴄᴏᴄᴏᴋᴀɴ ᴅᴀᴛᴀ ᴋᴀᴋᴜ ᴅᴀɴ ʟᴇᴍᴇꜱ..."
    ]

    # Show initial proses message
    proses_msg = await event.respond(proses_list[0])
    await asyncio.sleep(0.5)
    for teks in proses_list[1:]:
        try:
            await proses_msg.edit(teks)
        except Exception:
            pass
        await asyncio.sleep(0.5)

    # Build final message
    hasil_list = []
    for target in targets:
        warna = random.choice(warna_list)
        panjang = random.randint(3, 30)
        bentuk = random.choice(bentuk_list)
        status = random.choice(status_list)

        hasil = (
            f"🍆 ᴋᴏɴᴛᴏʟ ᴀɴᴀʟʏᴢᴇ 🍆\n"
            f"👤 {target}\n"
            f"📏 ᴘᴀɴᴊᴀɴɢ : {panjang} ᴄᴍ\n"
            f"🎨 ᴡᴀʀɴᴀ : {warna}\n"
            f"🔮 ʙᴇɴᴛᴜᴋ : {bentuk}\n"
            f"🔥 ꜱᴛᴀᴛᴜꜱ : {status}"
        )
        hasil_list.append(hasil)

    teks_final = "\n\n".join(hasil_list)

    # Wrap in triple backticks for gray code block
    teks_final = f"```\n{teks_final}\n```"

    # Send as normal message (not reply)
    await event.respond(teks_final, parse_mode="markdown")


from telethon import events
import asyncio
import random

# Daftar kata kata  pakai nama Diva
_WORDS = [
    "celia itu cantik banget 😘✨",
    "celia jangan lupa makan ya 💕",
    "celia itu gemay banget 🥺👉👈",
    "celia sayang aku ya 😍",
    "celia itu queen di hati aku 👑💖",
    "sehari tanpa celia itu kyk 24 jam 😭",
]

# Biar bisa stop loop
loop_running = {}

@client.on(events.NewMessage(pattern=r"\.celia", outgoing=True))
async def diva_(event):
    chat_id = event.chat_id
    
    if chat_id in loop_running and loop_running[chat_id]:
        await event.edit("⚠lagi jalan di sini!")
        return

    loop_running[chat_id] = True
    await event.edit("🔮 celia...")

    try:
        while loop_running[chat_id]:
            msg = random.choice(_WORDS)
            await event.respond(msg)
            await asyncio.sleep(2)  # delay antar pesan biar ga langsung banjir
    except Exception as e:
        await event.respond(f"❌ Error: {str(e)}")
        loop_running[chat_id] = False


# Command buat stop loop
@client.on(events.NewMessage(pattern=r"\.stopcelia", outgoing=True))
async def stop_diva(event):
    chat_id = event.chat_id
    if chat_id in loop_running and loop_running[chat_id]:
        loop_running[chat_id] = False
        await event.edit("🛑dihentikan!")
    else:
        await event.edit("⚠ Gak ada yang jalan di sini.")


async def main():
    print("Bot running...")
    await client.start()
    try:
        await client.run_until_disconnected()
    except KeyboardInterrupt:
        print("\nCtrl+C pressed. Stopping bot...")
        await client.disconnect()
        print("Bot stopped.")
        return

asyncio.run(main())
