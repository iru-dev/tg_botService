import datetime
import telebot;
import cv2;
import config
import telebot
from telebot import apihelper
from telebot import types
import datetime
import os
from PIL import Image, ImageGrab
import logging
from git import Repo


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)  # Outputs debug messages to console.



def autor(chatid):
    strid = str(chatid)
    for item in config.ADMINS:
        if item == strid:
            return True
    return False



bot = telebot.TeleBot(config.TG_TOKEN);





kb = types.InlineKeyboardMarkup()
bt1 = types.InlineKeyboardButton("Фото", callback_data='foto')
bt2 = types.InlineKeyboardButton("Видео", callback_data='video')
bt3 = types.InlineKeyboardButton("Рабочий стол", callback_data='desktop')
bt4 = types.InlineKeyboardButton("Звук", callback_data='sound')
bt5 = types.InlineKeyboardButton("restart bot", callback_data='restart_bot')
bt6 = types.InlineKeyboardButton("update bot", callback_data='update_bot')
bt7 = types.InlineKeyboardButton("Охрана", callback_data='toggle')
bt8 = types.InlineKeyboardButton("Мониторинг", callback_data='monitor')

kb.row(bt1,bt2,bt3)
#kb.row(bt4)
kb.row(bt7, bt6)
kb.row(bt5)

#kb.add(bt1,bt2,bt3,bt4)


    # bot.send_message(238538484, 'BOT START\nip: '+ pymyip.get_ip() + '\nCity:' + pymyip.get_city() + '\nCountry' + pymyip.get_country(), reply_markup=kb)
  

kb_video = types.InlineKeyboardMarkup(row_width=3)
btv1 = types.InlineKeyboardButton("10c", callback_data='10sv')
btv2 = types.InlineKeyboardButton("30c", callback_data='30sv')
btv3 = types.InlineKeyboardButton("60c", callback_data='60sv')
kb_video.add(btv1,btv2,btv3)

kb_sound = types.InlineKeyboardMarkup(row_width=3)
bts1 = types.InlineKeyboardButton("10c", callback_data='10ss')
bts2 = types.InlineKeyboardButton("30c", callback_data='30ss')
bts3 = types.InlineKeyboardButton("60c", callback_data='60ss')
kb_sound.add(btv1,btv2,btv3)

# @bot.message_handler(func=lambda m: True, content_types=['new_chat_participant'])
# def on_user_joins(message):
#     name = message.new_chat_participant.first_name
#     if hasattr(message.new_chat_participant, 'last_name') and message.new_chat_participant.last_name is not None:
#         name += u" {}".format(message.new_chat_participant.last_name)

#     if hasattr(message.new_chat_participant, 'username') and message.new_chat_participant.username is not None:
#         name += u" (@{})".format(message.new_chat_participant.username)

#     bot.reply_to(message, text_messages['welcome'].format(name=name))


def sound_r(s_time, chat_id):
    a = datetime.datetime.today().strftime("%Y%m%d%H%M%S%s")
    voiceFile = '/tmp/voice_' + a + '.ogg'
    bot.send_message(chat_id, "Пишем видео")
    voice = open(voiceFile, 'rb')
    bot.send_voice(chat_id, voice)

def video_r(s_time, chat_id):
    bot.send_message(chat_id, "Пишем видео")
    a = datetime.datetime.today().strftime("%Y%m%d%H%M%S%s")
    cap = cv2.VideoCapture(0)
#
#
#
    cap.set(cv2.CAP_PROP_FPS, 24) # Частота кадров
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # Ширина кадров в видеопотоке.
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) # Высота кадров в
    codec = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter('/tmp/cam_' + a + '.mp4', codec, 25.0, (1280, 720))
    start_time = datetime.datetime.now()
    while(cap.isOpened()):
        ret, frame = cap.read()
        time_delta = datetime.datetime.now() - start_time
        if time_delta.total_seconds() >= s_time:
            break
        #cv2.imshow('frame', frame)
        out.write(frame)
    out.release()
    cap.release()
    cv2.destroyAllWindows()
    video = open('/tmp/cam_' + a + '.mp4', 'rb')
    bot.send_video(chat_id, video, caption='Видео с камеры', reply_markup=kb)


def desktop_message(message):
    a = datetime.datetime.today().strftime("%Y%m%d%H%M%S%s")
    imageFile = '/tmp/des_' + a + '.jpg'
    img = ImageGrab.grab()
    img.save(imageFile, "jpg")
    img2 = open(imageFile, 'rb')
    bot.send_photo(message.chat.id, img2, caption='Рабочий стол', reply_markup=kb)

def update_bot():
    print('git')
    g = git.cmd.Git(os.path.abspath(__file__))
    g.pull() 
    origin.pull()


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if autor(call.message.chat.id):
                if call.data == "monitor":
                    monitoring(call.message)
                if call.data == "update_bot":
                    update_bot(call.message)
                if call.data == "foto":
                    sendfoto_message(call.message)
                if call.data == "video":
                    bot.send_message(call.message.chat.id, 'Записать видео', reply_markup=kb_video)
                if call.data == "sound":
                    bot.send_message(call.message.chat.id, 'Записать звук', reply_markup=kb_sound)
                if call.data == 'desktop':
                    desktop_message(call.message)
                if call.data == '10sv':
                    video_r(10, call.message.chat.id)
                if call.data == '30sv':
                    video_r(30, call.message.chat.id)
                if call.data == '60sv':
                    video_r(60, call.message.chat.id)
                if call.data == '10ss':
                    sound_r(10, call.message.chat.id)
                if call.data == '30ss':
                    sound_r(15600, call.message.chat.id)
                if call.data == '60ss':
                    sound_r(60, call.message.chat.id)
                if call.data == 'ecure_on':
                    secure_fun(1)
                if call.data == 'ecure_off':
                    secure_fun(0)
                if call.data == 'restart_bot':
                    os.system("systemctl restart tgbot.service")
            else:
                bot.send_message(call.message.chat.id, 'Тебе сюда нельзя. Твой ID: ' + str(call.message.chat.id))
                bot.send_sticker(call.message.chat.id, 'CAADAgADcQMAAkmH9Av0tmQ7QhjxLRYE')

    except Exception as e:
        print(repr(e))

@bot.callback_query_handler(func=lambda call: True)
def test_callback(call): # <- passes a CallbackQuery type object to your function
    logger.info(call)

@bot.message_handler(commands=['start'])
def start_message(message):
    if autor(message.chat.id):
        cid = message.chat.id
        message_text = message.text
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        bot.send_sticker(message.chat.id, 'CAADAgAD6CQAAp7OCwABx40TskPHi3MWBA')
        bot.send_message(message.chat.id, 'Привет, ' + user_name + ' Что ты хочешь от меня, собака сутулая?', reply_markup=kb)
    else:
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Я не сутулая собака, я коженный мешок", request_contact=True)
        keyboard.add(button_phone)

        bot.send_message(message.chat.id, 'Тебе сюда нельзя, Сутулая собака. Твой ID: ' + str(message.chat.id), reply_markup=keyboard)

def sendfoto_message(message):
    a = datetime.datetime.today().strftime("%Y%m%d%H%M%S%s")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    ret, frame = cap.read()
    imageFile = '/tmp/cam_' + a + '.jpg'
    cv2.imwrite(imageFile, frame)
    img = open(imageFile, 'rb')
    bot.send_photo(message.chat.id, img, caption='Фото с камеры', reply_markup=kb)
    cap.release()

# @bot.message_handler(content_types=['contact'])
# def contact(message):
#     if message.contact is not None:
#         keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#         button_phone = types.KeyboardButton(text="Я даже знаю, где я", request_location = True)
#         keyboard.add(button_phone)

#         bot.send_message(238538484, message.contact)
#         bot.send_message(message.chat.id, "Здорово, а откуда ты?", reply_markup=keyboard)

def main():
    
   
    # bot.polling(none_stop=True)
    # bot.infinity_polling()
    bot.send_message(config.ADMINS[0], "START BOT /start")
    bot.polling(True)

if __name__ == '__main__':
    main()

