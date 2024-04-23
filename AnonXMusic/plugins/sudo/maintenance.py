from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.misc import SUDOERS
from AnonXMusic.utils.database import (
    get_lang,
    is_maintenance,
    maintenance_off,
    maintenance_on,
)
from AnonXMusic.plugins.tools.reload import delete_message
from strings import get_string


@app.on_message(filters.command(["maintenance"]) & SUDOERS)
async def maintenance(client, message: Message):
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except:
        _ = get_string("en")
    usage = _["maint_1"]
    if len(message.command) != 2:
        mystic = await message.reply_text(usage)
        await delete_message(message.chat.id, mystic.id)
        return
    state = message.text.split(None, 1)[1].strip().lower()
    if state == "enable":
        if await is_maintenance() is False:
            mystic = await message.reply_text(_["maint_4"])
        else:
            await maintenance_on()
            mystic = await message.reply_text(_["maint_2"].format(app.mention))
    elif state == "disable":
        if await is_maintenance() is False:
            await maintenance_off()
            mystic = await message.reply_text(_["maint_3"].format(app.mention))
        else:
            mystic = await message.reply_text(_["maint_5"])
    else:
        mystic = await message.reply_text(usage)

    await delete_message(message.chat.id, mystic.id)    