import requests
import telebot
import API
import os

bot = telebot.TeleBot(API.botAPI)


def download_video(video_url, file_name):
    try:
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size= 1024 * 1024):
                if chunk:
                    file.write(chunk)
        return file_name
    except Exception as e:
        print(f'Ошибка загрусзки видео: {e}')
        return 0

@bot.message_handler(content_types=['text'])
def main(message):
    try:
        video_id = message.text
        bot.reply_to(message, f'Ищу видео...')

        #video info:
        url = "https://youtube-media-downloader.p.rapidapi.com/v2/video/details"
        querystring = {"videoId":video_id}

        headers = {
            "x-rapidapi-key": "831b4d7540mshf9745ac3cc801bcp103320jsn5ee0da0ded29",
            "x-rapidapi-host": "youtube-media-downloader.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        #video url
        video_url = data['videos']['items'][3]['url']
        video_name = "video.mp4"

        #downloading video
        bot.send_message(message.chat.id, f'Скачиваю видео...')
        video_path = download_video(video_url, video_name)

        if video_path:
            with open(video_path, 'rb') as video_file:
                bot.send_video(message.chat.id, video_file)
                os.remove(video_path)
        else:
            bot.send_message(message.chat.id, f'Не удалось скачать видео')


    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {str(e)}')



bot.infinity_polling()