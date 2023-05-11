# from telegram import Bot, Update, ReplyKeyboardMarkup, KeyboardButton
# from telegram.ext import CommandHandler, Updater, MessageHandler
import telebot
import requests
import dotenv
import os

dotenv.load_dotenv()
foursquare_api_key = os.environ['FOURSQUARE_API_KEY']
bot = telebot.TeleBot(os.environ['BOT_API_KEY'])

def start(update):
    bot.send_message(update.message.chat_id, "Welcome to the MakanBot! I can help you find nearby restaurants around you.")

    bot.send_message(
        update.message.chat_id,
        "Send me your location so i can find nearby restaurants around you.",
        reply_markup=telebot.types.ReplyKeyboardMarkup([
            telebot.types.KeyboardButton("Send Location", request_location=True)
        ]),
    )

def get_nearby_restaurants(latitude, longitude, radius):
    URL = "https://api.foursquare.com/v2/venues/explore?client_id={}&client_secret={}&ll={},{}&radius={}&v=20230510".format(
        foursquare_api_key, foursquare_api_key, latitude, longitude, radius
    )

    response = requests.get(URL)

    data = response.json()

    restaurants = data["response"]["groups"][0]["items"]

    return restaurants


def nearby(update):
    location = update.message.location

    restaurants = get_nearby_restaurants(location.latitude, location.longitude, 2000)

    bot.send_message(update.message.chat_id, "Here are the nearest restaurants to you:")
    for restaurant in restaurants:
        bot.send_message(update.message.chat_id, restaurant["name"])




def main():
    bot.poll_handler(telebot.types.BotCommand("start", start))
    bot.poll_handler(telebot.types.BotCommand("nearby", nearby))
    bot.polling()

if __name__ == '__main__':
    main()