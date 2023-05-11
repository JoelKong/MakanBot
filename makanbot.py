from telegram import Bot, Update, ReplyKeyboardMarkup, KeyboardButton
import requests
import dotenv
import os

dotenv.load_dotenv()
foursquare_api_key = os.environ['FOURSQUARE_API_KEY']
bot = os.environ['BOT_API_KEY']

def start(update):
    bot.sendMessage(update.message.chat_id, "Welcome to the MakanBot! I can help you find nearby restaurants around you.")

    bot.sendMessage(
        update.message.chat_id,
        "Send me your location so i can find nearby restaurants around you.",
        reply_markup=ReplyKeyboardMarkup([
            KeyboardButton("Send Location", request_location=True)
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