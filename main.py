import time

import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.background import BackgroundScheduler
from telepot.loop import MessageLoop

from config import token, my_chat_id

bot = telepot.Bot(token)


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    username = msg["from"]["username"]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Pubblicato", callback_data='pubblicato' + str(chat_id))]])

    if content_type == "text":
        txt = msg['text']
        if txt == '/start':
            bot.sendMessage(chat_id, "Benvenuto " + username + "! Invia qui i tuoi meme!")
        elif txt == '/help':
            bot.sendMessage(chat_id,
                            "Manda l'immagine che vuoi pubblicare, se accettata riceverai una notifica quando verrà "
                            "pubblicata sul canale")
        else:
            bot.sendMessage(chat_id, "Al momento accetto solo immagini")

    elif content_type == 'photo':
        media_id = msg["photo"][0]["file_id"]
        bot.sendMessage(chat_id, "Grazie, il tuo meme è sotto esame...")

        bot.sendPhoto(my_chat_id, media_id)
        bot.sendMessage(my_chat_id, "Ciao Claudio, @" + username + " ha inviato questo", reply_markup=keyboard)

    else:
        bot.sendMessage(chat_id, "Al momento accetto solo immagini")


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    chat_id = int(query_data[10:])

    if query_data[:10] == 'pubblicato':
        bot.answerCallbackQuery(query_id, text='Ok')
        bot.sendMessage(chat_id, "Pubblicato!")

def main():
    
    bot.message_loop({'chat': on_chat_message,
                      'callback_query': on_callback_query})
    print("Listening...")

    while 1:
        time.sleep(10)
        

if __name__ == '__main__':
    main()

