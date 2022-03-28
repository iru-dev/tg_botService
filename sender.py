import logging
import telebot
import config

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)  # Outputs debug messages to console.
bot = telebot.TeleBot(config.token, threaded=True)

import sys

video = open(sys.argv[1], 'rb')
bot.send_video(config.ADMIN[0], video, caption='Обнаружено движение')