import telebot
import requests
import os


bot = telebot.TeleBot('8116297576:AAFWNwx7DyKt0dCfrYDMeGwa3xUi7zTpejY')
API = '13cf65db59720302d6d3986dbb79c057'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привіт! Напиши назву міста або села, щоб дізнатися погоду.')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    try:

        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
        res.raise_for_status()
        data = res.json()


        temp = data["main"]["temp"]
        bot.reply_to(message, f'Зараз температура в {city.capitalize()}: {temp}°C')


        image = 'sonychna.jpg' if temp > 5.0 else 'pasmurna.jpg'
        image_path = os.path.join('../../Desktop/', image)

        if os.path.exists(image_path):
            with open(image_path, 'rb') as file:
                bot.send_photo(message.chat.id, file)
        else:
            bot.reply_to(message, 'Вибач, зображення не знайдено!')

    except requests.exceptions.RequestException as e:
        bot.reply_to(message, 'Такого міста чи села не існує! Спробуй ще раз')
    except KeyError:
        bot.reply_to(message, 'Не вдалося знайти дані про погоду для цього міста.')
    except Exception as e:
        bot.reply_to(message, 'Виникла помилка. Будь ласка, спробуй пізніше.')

bot.polling(none_stop=True)
