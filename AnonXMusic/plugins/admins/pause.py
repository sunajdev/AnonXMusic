from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.core.call import Anony
from AnonXMusic.utils.database import is_music_playing, music_off
from AnonXMusic.utils.decorators import AdminRightsCheck
from AnonXMusic.utils.inline import close_markup
from AnonXMusic.plugins.tools.reload import delete_message
from config import BANNED_USERS


@app.on_message(filters.command(["pause", "cpause"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def pause_admin(cli, message: Message, _, chat_id):
    if not await is_music_playing(chat_id):
        mystic = await message.reply_text(_["admin_1"])
        await delete_message(chat_id, mystic.id)
        return 
    await music_off(chat_id)
    await Anony.pause_stream(chat_id)
    mystic = await message.reply_text(
        _["admin_2"].format(message.from_user.mention), reply_markup=close_markup(_)
    )
    await delete_message(chat_id, mystic.id)
