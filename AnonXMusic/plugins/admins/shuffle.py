import random

from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.misc import db
from AnonXMusic.utils.decorators import AdminRightsCheck
from AnonXMusic.utils.inline import close_markup
from AnonXMusic.plugins.tools.reload import delete_message
from config import BANNED_USERS


@app.on_message(
    filters.command(["shuffle", "cshuffle"]) & filters.group & ~BANNED_USERS
)
@AdminRightsCheck
async def admins(Client, message: Message, _, chat_id):
    check = db.get(chat_id)
    if not check:
        mystic = await message.reply_text(_["queue_2"])
        await delete_message(message.chat.id, mystic.id)
        return
    try:
        popped = check.pop(0)
    except:
        mystic = await message.reply_text(_["admin_15"], reply_markup=close_markup(_))
        await delete_message(message.chat.id, mystic.id)
        return
    check = db.get(chat_id)
    if not check:
        check.insert(0, popped)
        mystic = await message.reply_text(_["admin_15"], reply_markup=close_markup(_))
        await delete_message(message.chat.id, mystic.id)
        return
    random.shuffle(check)
    check.insert(0, popped)
    mystic = await message.reply_text(
        _["admin_16"].format(message.from_user.mention), reply_markup=close_markup(_)
    )
    await delete_message(message.chat.id, mystic.id)
