import telebot
from tmdbv3api import TMDb
from tmdbv3api import Movie
from tmdbv3api import  TV
from emoji import emojize
import rawgpy
import re

rawg = rawgpy.RAWG('TelegramBot')
f = False
t = False
g = False
tmdb = TMDb()
tmdb.api_key = '21d048a03d422d6993fd4e168b353f2b'
movie = Movie()
tv = TV()

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row(emojize(":tv:", use_aliases=True)+'TV', emojize(":clapper:", use_aliases=True)+'Film', emojize(":video_game:",use_aliases=True)+'Game')
bot=telebot.TeleBot('1073454302:AAFv-PeU0GtPoYqY4Ghh7vtbO1r5GquKZG8')
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start\nДля того, чтобы найти фильм, введи FILM и название фильма\nДля того, чтобы найти сериал, введи TV и название сериала')
@bot.message_handler()
def send_text(message):
    global t
    global f
    global g
    if message.text==emojize(":tv:", use_aliases=True)+'TV':
        t=True
        f=False
        g=False
    elif message.text==emojize(":clapper:", use_aliases=True)+'Film':
        t=False
        f=True
        g=False
    elif message.text==emojize(":video_game:",use_aliases=True)+'Game':
        g=True
        t=False
        f=False
    if f and message.text!=emojize(":clapper:", use_aliases=True)+'Film':
        search = movie.search(message.text)
        if search:
            bot.send_message(message.chat.id,emojize(":clapper:", use_aliases=True)+search[0].title)
            if search[0].poster_path: bot.send_photo(message.chat.id, 'http://image.tmdb.org/t/p/w185/'+search[0].poster_path)
            bot.send_message(message.chat.id, search[0].overview)
            bot.send_message(message.chat.id,search[0].vote_average)
        else:
            bot.send_message(message.chat.id,'Не найдено, проверьте правильность запроса')
    elif t and message.text!=emojize(":tv:", use_aliases=True)+'TV':
        search = tv.search(message.text)
        if search:
            bot.send_message(message.chat.id, emojize(":tv:", use_aliases=True)+search[0].name)
            if search[0].poster_path: bot.send_photo(message.chat.id, 'http://image.tmdb.org/t/p/w185/' + search[0].poster_path)
            bot.send_message(message.chat.id, search[0].overview)
            bot.send_message(message.chat.id, search[0].vote_average)
        else:
            bot.send_message(message.chat.id,'Не найдено, проверьте правильность запроса')
    elif g and message.text!=emojize(":video_game:",use_aliases=True)+'Game':
        results = rawg.search(message.text)  # defaults to returning the top 5 results
        if results:
           game = results[0]
           game.populate()  # get additional info for the game
           bot.send_message(message.chat.id,emojize(":video_game:",use_aliases=True)+game.name)
           bot.send_message(message.chat.id, game.developers)
           bot.send_message(message.chat.id, game.description)
        else:
           bot.send_message(message.chat.id,'Не найдено, проверьте правильность запроса')
    #else: bot.send_message(message.chat.id,'Для того, чтобы найти фильм, введи FILM и название фильма\nДля того, чтобы найти сериал, введи TV и название сериала')
bot.polling()