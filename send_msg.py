import asyncio
import os
from aiogram import types, Router
from aiogram.filters import Command

from commersant import commersant_news
from config import ID_CHANNEL
from gazeta import get_gazeta
from main import bot
from rbc_news import checking_updates_rbc
from rt import get_rt

router = Router()


# Команда запускает парсер
@router.message(Command("go"))
async def cmd_start(message: types.Message):
    while True:
        try:
            await message.answer(text='Работа пошла!')
            news_dict = checking_updates_rbc()
            news_dict.update(get_rt())
            news_dict.update(commersant_news())
            news_dict.update(get_gazeta())
            for article_id, v in sorted(news_dict.items()):
                news = (f"<b>{v['article_title']}.</b>\n\n"
                        f"{v['article_news']}\n\n"
                        f"<u>{v['source']}</u>\n")
                image_path = f"img_downloaded/{article_id}.png"
                if len(news) >= 1024:
                    await bot.send_message(chat_id=ID_CHANNEL, text=news, parse_mode="HTML")
                else:
                    if os.path.exists(image_path):
                        await bot.send_photo(chat_id=ID_CHANNEL, photo=types.FSInputFile(image_path),
                                             caption=news, parse_mode="HTML")
                        os.remove(f"img_downloaded/{article_id}.png")
                    else:
                        await bot.send_message(chat_id=ID_CHANNEL, text=news, parse_mode="HTML")
            await asyncio.sleep(180)
        except Exception as e:
            error_msg = f"Произошла ошибка {e}"
            print(f'{e}')
            await message.answer(text=error_msg)
            await asyncio.sleep(900)
            continue
