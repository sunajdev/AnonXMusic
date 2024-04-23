from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.misc import SUDOERS
from AnonXMusic.utils.database import blacklist_chat, blacklisted_chats, whitelist_chat
from AnonXMusic.utils.decorators.language import language
from AnonXMusic.plugins.tools.reload import delete_message
from config import BANNED_USERS


@app.on_message(filters.command(["blchat", "blacklistchat"]) & SUDOERS)
@language
async def blacklist_chat_func(client, message: Message, _):
    if len(message.command) != 2:
        mystic = await message.reply_text(_["black_1"])
        await delete_message(message.chat.id, mystic.id)
        return 
    chat_id = int(message.text.strip().split()[1])
    if chat_id in await blacklisted_chats():
        mystic = await message.reply_text(_["black_2"])
        await delete_message(message.chat.id, mystic.id)
        return 
    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        mystic = await message.reply_text(_["black_3"])
    else:
        mystic = await message.reply_text(_["black_9"])
    try:
        await app.leave_chat(chat_id)
    except:
        pass
    await delete_message(message.chat.id, mystic.id)

@app.on_message(
    filters.command(["whitelistchat", "unblacklistchat", "unblchat"]) & SUDOERS
)
@language
async def white_funciton(client, message: Message, _):
    if len(message.command) != 2:
        mystic = await message.reply_text(_["black_4"])
        await delete_message(message.chat.id, mystic.id)
        return 
    chat_id = int(message.text.strip().split()[1])
    if chat_id not in await blacklisted_chats():
        mystic = await message.reply_text(_["black_5"])
        await delete_message(message.chat.id, mystic.id)
        return 
    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        mystic = await message.reply_text(_["black_6"])
        await delete_message(message.chat.id, mystic.id)
        return 
    mystic = await message.reply_text(_["black_9"])
    await delete_message(message.chat.id, mystic.id)

@app.on_message(filters.command(["blchats", "blacklistedchats"]) & ~BANNED_USERS)
@language
async def all_chats(client, message: Message, _):
    text = _["black_7"]
    j = 0
    for count, chat_id in enumerate(await blacklisted_chats(), 1):
        try:
            title = (await app.get_chat(chat_id)).title
        except:
            title = "ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
        j = 1
        text += f"{count}. {title}[<code>{chat_id}</code>]\n"
    if j == 0:
        mystic = await message.reply_text(_["black_8"].format(app.mention))
    else:
        mystic = await message.reply_text(text)
    
    await delete_message(message.chat.id, mystic.id)