from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.core.call import Anony
from AnonXMusic.misc import SUDOERS, db
from AnonXMusic.utils.decorators import AdminActual
from AnonXMusic.utils.database import is_nonadmin_chat, set_autodelete, get_autodelete
from AnonXMusic.utils.decorators.language import languageCB
from AnonXMusic.utils.inline import close_markup, autodelete_markup
from AnonXMusic.plugins.tools.reload import delete_message
from config import BANNED_USERS, adminlist


@app.on_message(
    filters.command(["autodelete"])
    & filters.group
    & ~BANNED_USERS
)
@AdminActual
async def autodelete(cli, message: Message, _):
    chat_id = message.chat.id
    upl = autodelete_markup(_, chat_id)
    current_delete_time = await get_autodelete(chat_id)
    mystic = await message.reply_text(
        text=_["admin_41"].format(app.mention, current_delete_time),
        reply_markup=upl,
    )
    # this will delete the message after 30 seconds if no action is taken
    await delete_message(chat_id, mystic.id, long_seconds=30)


@app.on_callback_query(filters.regex("AutoDelete") & ~BANNED_USERS)
@languageCB
async def autodelete_callback(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    chat, seconds = callback_request.split("|")
    chat_id = int(chat)

    is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
    if not is_non_admin:
        if CallbackQuery.from_user.id not in SUDOERS:
            admins = adminlist.get(CallbackQuery.message.chat.id)
            if not admins:
                return await CallbackQuery.answer(_["admin_13"], show_alert=True)
            else:
                if CallbackQuery.from_user.id not in admins:
                    return await CallbackQuery.answer(_["admin_14"], show_alert=True)
                
    await set_autodelete(chat_id, int(seconds))
    
    await CallbackQuery.message.edit_text(
        text=_["admin_42"].format(seconds, CallbackQuery.from_user.mention),
        reply_markup=close_markup(_),
    )
    
    await delete_message(chat_id, CallbackQuery.message.id)
