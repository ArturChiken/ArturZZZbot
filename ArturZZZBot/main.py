from API import *

bot = Bot(token=botAPI)
dp = Dispatcher()

class Form(StatesGroup):
    waiting_for_text = State()


@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await message.answer(f'Привет, {message.from_user.first_name}, отправь мне ссылку на видео с ютуба и я скачаю и отправлю его для тебя в формате аудио!')
    await state.set_state(Form.waiting_for_text)

@dp.message(StateFilter(Form.waiting_for_text))
async def your_handler(message: types.Message, state: FSMContext):
    url = message.text
    audio_path = await download_video(url)

    if audio_path:
        try:
            audio_file = FSInputFile(audio_path)
            await message.reply_audio(audio_file, caption="Ваше аудио ♪")
            os.remove(audio_path)
        except Exception as e:
            await message.reply("Ошибка отправки")
            print(f"Ошибка: {e}")
    else:
        await message.reply("Не удалось скачать аудио")

    await state.clear()
    await message.answer(f'Отправь еще ссылку, чтобы скачать еще видео')
    await state.set_state(Form.waiting_for_text)

def _sync_download(url):
    try:
        os.makedirs("downloads", exist_ok=True)
        ydl_opts = {
            "format": "bestaudio[ext=m4a]",
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "quiet": True,
            "restrictfilenames": True,
            "no_warnings": True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)

    except Exception as e:
        print(f"Ошибка: {e}")
        return None

async def download_video(url):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _sync_download, url)



if __name__ == '__main__':
    dp.run_polling(bot)