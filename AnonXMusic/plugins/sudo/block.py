from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.misc import SUDOERS
from AnonXMusic.utils.database import add_gban_user, remove_gban_user
from AnonXMusic.utils.decorators.language import language
from AnonXMusic.utils.extraction import extract_user
from AnonXMusic.plugins.tools.reload import delete_message
from config import BANNED_USERS


@app.on_message(filters.command(["block"]) & SUDOERS)
@language
async def useradd(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            mystic = await message.reply_text(_["general_1"])
            await delete_message(message.chat.id, mystic.id)
            return 
    user = await extract_user(message)
    if user.id in BANNED_USERS:
        mystic = await message.reply_text(_["block_1"].format(user.mention))
        await delete_message(message.chat.id, mystic.id)
        return 
    await add_gban_user(user.id)
    BANNED_USERS.add(user.id)
    mystic = await message.reply_text(_["block_2"].format(user.mention))
    await delete_message(message.chat.id, mystic.id)

@app.on_message(filters.command(["unblock"]) & SUDOERS)
@language
async def userdel(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            mystic = await message.reply_text(_["general_1"])
            await delete_message(message.chat.id, mystic.id)
            return 
    user = await extract_user(message)
    if user.id not in BANNED_USERS:
        mystic = await message.reply_text(_["block_3"].format(user.mention))
        await delete_message(message.chat.id, mystic.id)
        return 
    await remove_gban_user(user.id)
    BANNED_USERS.remove(user.id)
    mystic = await message.reply_text(_["block_4"].format(user.mention))
    await delete_message(message.chat.id, mystic.id)

@app.on_message(filters.command(["blocked", "blockedusers", "blusers"]) & SUDOERS)
@language
async def sudoers_list(client, message: Message, _):
    if not BANNED_USERS:
        mystic = await message.reply_text(_["block_5"])
        await delete_message(message.chat.id, mystic.id)
        return 
    mystic = await message.reply_text(_["block_6"])
    msg = _["block_7"]
    count = 0
    for users in BANNED_USERS:
        try:
            user = await app.get_users(users)
            user = user.first_name if not user.mention else user.mention
            count += 1
        except:
            continue
        msg += f"{count}➤ {user}\n"
    if count == 0:
        await mystic.edit_text(_["block_5"])
    else:
        await mystic.edit_text(msg)
        
    await delete_message(message.chat.id, mystic.id)