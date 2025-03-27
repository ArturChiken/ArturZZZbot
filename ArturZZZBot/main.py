import asyncio
import logging
import sys
import API
import requests
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

TOKEN = API.botAPI
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(f'Hello!')

@dp.message(Command('youtube')) #сделать запрос ссылки и переброс на след шаг, это фейк что нижу...
async def YT_start(message: Message) -> None:

    url = "https://youtube-media-downloader.p.rapidapi.com/v2/video/details"

    querystring = {"videoId":"G33j5Qi4rE8"}

    headers = {
        "x-rapidapi-key": "831b4d7540mshf9745ac3cc801bcp103320jsn5ee0da0ded29",
        "x-rapidapi-host": "youtube-media-downloader.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    video_url = data['videos']['items'][0]['url']

@dp.message()
async def echo_message(message: Message) -> None:
    await message.reply(f'Сорри не понял, еще раз')


async def main() -> None:
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())