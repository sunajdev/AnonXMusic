from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def autodelete_markup(_, chat_id):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🕒 5s",
                    callback_data=f"AutoDelete {chat_id}|5",
                ),
                InlineKeyboardButton(
                    text="🕓 10s",
                    callback_data=f"AutoDelete {chat_id}|10",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["P_B_4"],
                    callback_data=f"AutoDelete {chat_id}|15",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🕤 30s",
                    callback_data=f"AutoDelete {chat_id}|30",
                ),
                InlineKeyboardButton(
                    text="🕛 60s",
                    callback_data=f"AutoDelete {chat_id}|60",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )
    return upl
