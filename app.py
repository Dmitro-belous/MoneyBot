import telebot
from config import TOKEN, exchanges
from extensions import APIException, MoneyConverter
import traceback

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты>" \
           "<в какую валюту перевести>" \
           "<количество переводимой валюты>\nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in exchanges.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Некорректное количество параметров')

        base, sym, amount = values
        answer = MoneyConverter.get_price(base, sym, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()
