from API import *

bot = Bot(token=botAPI)
dp = Dispatcher()

class Form(StatesGroup):
    waiting_for_text = State()


@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await message.answer(f'Привет, {message.from_user.first_name}, отправь мне ссылку на видео с ютуба и я скачаю и отправлю его для тебя в формате аудио!')
    await state.set_state(Form.waiting_for_text)

@dp.inline_query()
async def handle_inline_query(inline_query: types.InlineQuery):
    query = inline_query.query.strip()
    results = []

    if not query:
        results.extend([
            types.InlineQueryResultArticle(
                id='NoURL',
                title='Insert here a video URL',
                input_message_content=types.InputTextMessageContent(
                    message_text=f'Insert here like @ArtursZZZBot <URL>',
                )
            )
        ])
    else:
        url = query.strip()
        results.append(
            types.InlineQueryResultArticle(
                id="YesURL",
                title=f"AAA",
                input_message_content=types.InputTextMessageContent(
                    message_text=f'AAA!'
                ),
            )
        )
        try:
            audio_path = await download_video(query)
            if not audio_path or not os.path.exists(audio_path):
                raise FileNotFoundError

            result = InlineQueryResultAudio(
                id="1",
                audio_url=url,
                title=os.path.basename(audio_path),
            )

            await inline_query.answer(results=[result], cache_time=0)

        except Exception as e:
            print(f"Ошибка: {e}")
            await inline_query.answer(
                results=[],
                switch_pm_text="Ошибка загрузки",
                switch_pm_parameter="error",
            )

        finally:
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)

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