import telebot
from handlers.command_handlers import *
from handlers.callback_handlers import *
from handlers.message_handlers import *
from telebot import types
from dotenv import load_dotenv
import openpyxl
import os

book = openpyxl.open('price.xlsx', read_only=True)
sheet = book.active

load_dotenv('config.env.env')
api_token = os.getenv('API_TOKEN')
bot = telebot.TeleBot(api_token)

class User:
    def __init__(self, phone):
        self.phone = phone
        self.model = None
        self.problem = None
        self.check = False
        self.money = 0
        self.order =False
        self.castom = False
user_dict = {}

group = os.getenv('ID_CHANNEL')
manager = os.getenv('ID_CHANNEL') # os.getenv('MANGER')
