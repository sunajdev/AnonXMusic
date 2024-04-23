from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.utils.database import set_cmode
from AnonXMusic.utils.decorators.admins import AdminActual
from AnonXMusic.plugins.tools.reload import delete_message
from config import BANNED_USERS


@app.on_message(filters.command(["channelplay"]) & filters.group & ~BANNED_USERS)
@AdminActual
async def playmode_(client, message: Message, _):
    if len(message.command) < 2:
        mystic = await message.reply_text(_["cplay_1"].format(message.chat.title))
        await delete_message(message.chat.id, mystic.id)
        return
    query = message.text.split(None, 2)[1].lower().strip()
    if (str(query)).lower() == "disable":
        await set_cmode(message.chat.id, None)
        mystic = await message.reply_text(_["cplay_7"])
        await delete_message(message.chat.id, mystic.id)
        return
    elif str(query) == "linked":
        chat = await app.get_chat(message.chat.id)
        if chat.linked_chat:
            chat_id = chat.linked_chat.id
            await set_cmode(message.chat.id, chat_id)
            mystic = await message.reply_text(
                _["cplay_3"].format(chat.linked_chat.title, chat.linked_chat.id)
            )
            await delete_message(message.chat.id, mystic.id)
            return
        else:
            mystic = await message.reply_text(_["cplay_2"])
            await delete_message(message.chat.id, mystic.id)
            return
    else:
        try:
            chat = await app.get_chat(query)
        except:
            mystic = await message.reply_text(_["cplay_4"])
            await delete_message(message.chat.id, mystic.id)
            return 
        if chat.type != ChatType.CHANNEL:
            mystic = await message.reply_text(_["cplay_5"])
            await delete_message(message.chat.id, mystic.id)
            return
        try:
            async for user in app.get_chat_members(
                chat.id, filter=ChatMembersFilter.ADMINISTRATORS
            ):
                if user.status == ChatMemberStatus.OWNER:
                    cusn = user.user.username
                    crid = user.user.id
        except:
            mystic = await message.reply_text(_["cplay_4"])
            await delete_message(message.chat.id, mystic.id)
            return
        if crid != message.from_user.id:
            mystic = await message.reply_text(_["cplay_6"].format(chat.title, cusn))
            await delete_message(message.chat.id, mystic.id)
            return
        await set_cmode(message.chat.id, chat.id)
        mystic = await message.reply_text(_["cplay_3"].format(chat.title, chat.id))
        await delete_message(message.chat.id, mystic.id)
        return