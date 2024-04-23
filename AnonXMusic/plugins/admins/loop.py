from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.utils.database import get_loop, set_loop
from AnonXMusic.utils.decorators import AdminRightsCheck
from AnonXMusic.utils.inline import close_markup
from AnonXMusic.plugins.tools.reload import delete_message
from config import BANNED_USERS


@app.on_message(filters.command(["loop", "cloop"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def admins(cli, message: Message, _, chat_id):
    usage = _["admin_17"]
    if len(message.command) != 2:
        mystic = await message.reply_text(usage)
        await delete_message(chat_id, mystic.id)
        return
    state = message.text.split(None, 1)[1].strip()
    if state.isnumeric():
        state = int(state)
        if 1 <= state <= 10:
            got = await get_loop(chat_id)
            if got != 0:
                state = got + state
            if int(state) > 10:
                state = 10
            await set_loop(chat_id, state)
            mystic = await message.reply_text(
                text=_["admin_18"].format(state, message.from_user.mention),
                reply_markup=close_markup(_),
            )
            await delete_message(chat_id, mystic.id)
            return
        else:
            mystic = await message.reply_text(_["admin_17"])
            await delete_message(chat_id, mystic.id)
            return
    elif state.lower() == "enable":
        await set_loop(chat_id, 10)
        mystic = await message.reply_text(
            text=_["admin_18"].format(state, message.from_user.mention),
            reply_markup=close_markup(_),
        )
        await delete_message(chat_id, mystic.id)
        return
    elif state.lower() == "disable":
        await set_loop(chat_id, 0)
        mystic = await message.reply_text(
            _["admin_19"].format(message.from_user.mention),
            reply_markup=close_markup(_),
        )
        await delete_message(chat_id, mystic.id)
        return
    else:
        mystic = await message.reply_text(usage)
        await delete_message(chat_id, mystic.id)
        return