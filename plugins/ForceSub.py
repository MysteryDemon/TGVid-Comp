from pyrogram import Client, filters, enums 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from config import Config
from helper.database import db

async def not_subscribed(_, client, message):
    await db.add_user(client, message)
    if not Config.AUTH_CHANNEL:
        return False
    try:             
        user = await client.get_chat_member(Config.AUTH_CHANNEL, message.from_user.id) 
        if user.status == enums.ChatMemberStatus.BANNED:
            return True 
        else:
            return False                
    except UserNotParticipant:
        pass
    return True


@Client.on_message((filters.private | filters.group) & filters.create(not_subscribed))
async def forces_sub(client, message):
    invite_link = await client.create_chat_invite_link(int(Config.AUTH_CHANNEL))
    buttons = [[InlineKeyboardButton(text="📢 Join Update Channel 📢", url=invite_link.invite_link) ]]
    text = "**Sᴏʀʀy Yᴏᴜ'ʀᴇ Nᴏᴛ Jᴏɪɴᴇᴅ My Cʜᴀɴɴᴇʟ 😐. Sᴏ Pʟᴇᴀꜱᴇ Jᴏɪɴ Oᴜʀ Uᴩᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ Tᴏ Cᴄᴏɴᴛɪɴᴜᴇ**"

    return await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
          


