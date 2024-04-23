from pyrogram import filters

from AnonXMusic import app
from AnonXMusic.misc import SUDOERS
from AnonXMusic.utils.database import add_off, add_on
from AnonXMusic.utils.decorators.language import language
from AnonXMusic.plugins.tools.reload import delete_message


@app.on_message(filters.command(["logger"]) & SUDOERS)
@language
async def logger(client, message, _):
    usage = _["log_1"]
    if len(message.command) != 2:
        mystic = await message.reply_text(usage)
        await delete_message(message.chat.id, mystic.id)
        return 
    state = message.text.split(None, 1)[1].strip().lower()
    if state == "enable":
        await add_on(2)
        mystic = await message.reply_text(_["log_2"])
    elif state == "disable":
        await add_off(2)
        mystic = await message.reply_text(_["log_3"])
    else:
        mystic = await message.reply_text(usage)

    await delete_message(message.chat.id, mystic.id)