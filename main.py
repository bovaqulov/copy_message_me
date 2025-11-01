# forward_to_saved.py
# Talab: Python 3.10+, telethon
# O'rnatish: pip install telethon

import logging
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
import asyncio
import os
API_ID = 23938357
CHAT_ID = -1005049479645
API_HASH = "b18904e991d8585610fa9eeabc86b337"
SESSION_NAME = "session"



# Log sozlamalari
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(incoming=True))
async def forward_to_saved(event: events.NewMessage.Event):
    try:
        # Faqat individual (private) chatlardan kelgan xabarlarni qabul qilamiz
        if not event.is_private:
            return

        sender = await event.get_sender()
        if not sender:
            return

        # Agar sender bot bo'lsa yoki ID ignore ro'yxatda bo'lsa - o'tkazib yubor
        if sender.bot:
            return

        # Agar o'zingizdan kelgan xabar bo'lsa - o'tkazib yubor
        if sender.is_self:
            return

        # Forward qilamiz (asl xabar va media bilan)
        await client.forward_messages('me', event.message)
        logger.info(f"Forward qildim: from @{getattr(sender, 'username', None) or sender.id}")

    except FloodWaitError as e:
        # Agar Telegram flood kutishni buyursa, kutamiz
        logger.warning(f"FloodWait: kutilyapti {e.seconds} soniya")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        logger.exception("Xatolik yuz berdi:")

async def main():
    await client.start()
    me = await client.get_me()
    logger.info(f"Userbot ishga tushdi: {me.first_name} ({me.id})")
    # Botni doimiy ishlashi uchun idle holatiga o'tkazish
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("To'xtatildi.")
