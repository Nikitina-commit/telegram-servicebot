# дата обращения, тип обращения при отправке сообщения в сервис

# import constants as Keys
import telebot, traceback, re
from telebot import types
from datetime import datetime
import json
import string, threading, sys, logging
#from telegram.ext import Updater
#from telegram import Update
#from aiogram import Bot, Dispatcher


credentials = json.load(open("service_telegram.json", "r")) #388367643
TO_CHAT_ID = int(credentials["id"])
TOKEN = credentials["token"]
bot = telebot.TeleBot(TOKEN, parse_mode= "html")
#dp = Dispatcher(bot, storage=storage)
global FROM_CHAT_ID
f = open('user_id.txt', 'a')
f.write( 'ID          Дата обращения        Дата запуска: ' + str(datetime.now()) +  "\n")
f.close()
fs = open('service_id.txt', 'a')
fs.write( 'ID             Оценка        ID_service          Дата ответа ' + "\n" )
fs.close()

def isID(stri):
 #   r = re.compile()
    if re.search(r'\d{9}', stri):
        return 1
    else:
        return 0

def isMashine(stri):
    #   r = re.compile()
    if (re.search(r'[1][0-9]\W[0-8][0-9]\W8[П,п]\b', stri) or re.search(r'[2][0-8]\W[0-8][0-9]\W8[П,п]\b', stri) or
            re.search(r'[1][0-9]\W[0-8][0-9]\W[4,8]\b', stri) or re.search(r'[2][0-8]\W[0-8][0-9]\W[4,8]\b', stri)):
        #re.search(r'\d{2}\W\d{2}\W[4,8]\b', stri)
        return 1
    else:
        return 0

def isFIO(stri):
 #   r = re.compile()
    if re.search(r'\w+\s\w+', stri):
        return 1
    else:
        return 0

@bot.message_handler(content_types=['text','document', 'photo', 'video', 'audio', 'media_group'])

def data(message):
    if message.text == "/start" :
        question = 'Чем могу помочь?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
        bot.register_next_step_handler(message, callback_worker)
        f = open('user_id.txt', 'a')
        f.write( str(message.from_user.id) +'   ' + str(datetime.now()) + "\n")
        f.close()
        #print(str(count) + ':' + str(message.from_user.id), end="\n")
    elif message.from_user.id == TO_CHAT_ID and message.text == "/service":
        bot.send_message(message.from_user.id, text='ID заявки: ')
        bot.register_next_step_handler(message, callback_worker)
    elif message.from_user.id == TO_CHAT_ID and message.text == "/logs":
        bot.send_media_group(message.from_user.id, [telebot.types.InputMediaDocument(open('service_id.txt', 'rb')),
                                               telebot.types.InputMediaDocument(open('user_id.txt', 'rb'))])
    else:
        question = 'Для начала работы напишите /start'
        bot.send_message(message.from_user.id, text=question)
        bot.register_next_step_handler(message, data)



def callback_worker(message):

    if message.text == "Продукция":
        question = 'Наша компания предлагает широкий спектр продукции. \nКакая именно Вас интересует?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboardProduct)
        bot.register_next_step_handler(message, callback_Product)

    elif message.text == "Сервисная служба":
        question = 'С чем связано обращение?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboardServ)
        bot.register_next_step_handler(message, callback_Serv)

    elif message.text == "Обучение инженеров":
        question = ('Мы проводим курс повышения квалификации по сервисному обслуживанию на нашем аппарате АРХП-"АМИКО", а именно: '
                    '\n1. Периодическое техническое обслуживание;'
                    '\n2. Внеплановое техническое обслуживание;'
                    '\n3. Техническое диагностирование;'
                    '\n4. Ремонт;'
                    '\n5. Контроль технического состояния;'
                    '\n6. Монтаж и наладка;'
                    '\nНа безвоздмездной основе с целью дальнейшего партнерского сотрудничества.'
                    '\nЕсли заинтересованы, то свяжитесь с нами:')
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboardBack)
        bot.register_next_step_handler(message, callback_Back, 0)

    elif message.from_user.id == TO_CHAT_ID:
        if message.text.isdigit() and isID(message.text)==1:
            FROM_CHAT_ID = message.text
            bot.send_message(TO_CHAT_ID, text='Введите ответ на обращение:')
            bot.send_message(FROM_CHAT_ID, text='Добрый день, вас приветствует сервисная служба \nООО "Рентген-Комплект", '
                                                'следующим сообщением в этом чате вы получите ответ наших инженеров по вашей заявке.')
            bot.register_next_step_handler(message, callback_answer, FROM_CHAT_ID)
        else:
            bot.send_message(TO_CHAT_ID, text='ID заявки:')
            bot.register_next_step_handler(message, callback_worker)

    else:
        question = 'Для начала работы напишите /start'
        bot.send_message(message.from_user.id, text=question)
        bot.register_next_step_handler(message, data)


def callback_YN(message):
    if message.text == "Да":
        question = ('Заявка принята, мы свяжемся с вами в ближайшее время')
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboardAnother )
        bot.register_next_step_handler(message, callback_Serv)
        txt = ('Обращение от: ' + str(personal) + '\nНаселенный пункт: ' + str(city) +'\nНомер телефона: ' + str(phone_number) + '\nНомер аппарата: ' + str(machine_number) +
               '\nВопрос: ' + str(text_question) + '\nДата обращения: ' + str(datetime.now().date()) + '\n\nID: ' + str(message.from_user.id))
        bot.send_message(TO_CHAT_ID, text=txt )

    elif message.text == "Нет":
        question = 'Заполните заявку снова'
        bot.send_message(message.from_user.id, text=question)
        question = 'Укажите Ваше Ф.И.О. и должность:'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboardBack)
        bot.register_next_step_handler(message, data_ID)
    elif message.text == "Отправить файл":
        question = 'Отправьте файл:'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboardBack)
        bot.register_next_step_handler(message, callback_file)
    elif message.text == 'Выход в меню':
        callback_Back(message, 0)
    else:
        question = 'Для отправки файла нажмите кнопку "Отправить файл"'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboardYN)
        bot.register_next_step_handler(message, callback_YN)


def callback_Product(message):
    if message.text == 'С-Дуга':
        question = ('Аппарат рентгенохирургический передвижной АРХП-АМИКО.\n'
                    'Детально ознакомиться с характеристиками и комплектациями '
                    'можете на нашем сайте:\nhttps://r-k.ru/production/'
                    '\nЛибо по телефону:\n')
        bot.send_photo(message.from_user.id, open('C-duga.jpg', 'rb'))
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboardBack)
        bot.register_next_step_handler(message, callback_Back, 1)

    elif message.text == "Рентген. защита":
        question = ('Мы можем предложить:\n'
                    '1. Рентгенозащитную одежду;\n'
                    '2. Рентгенозащитные ширмы;\n'
                    '3. Рентгенозащитные ставни, окна и двери;\n'
                    'Во вложении каталог нашей продукции, прайс и номенклатура '
                    'обязательной защиты в зависимости от задач. \n'
                    'Заказать можно на нашем сайте:\n'
                    'https://r-k.ru/shop/\n'
                    'Либо по телефону:\n')
        bot.send_media_group(message.from_user.id, [telebot.types.InputMediaPhoto(open('1.jpg','rb')), telebot.types.InputMediaPhoto(open('2.jpg', 'rb'))])
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboardBack)
        bot.send_media_group(message.from_user.id, [telebot.types.InputMediaDocument(open('f_nom.jpg', 'rb')),
                                               telebot.types.InputMediaDocument(open('f_price.pdf', 'rb')),
                                               telebot.types.InputMediaDocument(open('f_sredstva.pdf', 'rb'))])
        bot.register_next_step_handler(message, callback_Back, 1)
    elif message.text == 'Негатоскоп':
        question = ('Детально ознакомиться с характеристиками и комплектациями и '
                    'сделать заказ можете на нашем сайте:\n'
                    'https://r-k.ru/shop/negatoskopy/\n'
                    'Либо по телефону:\n')
        bot.send_photo(message.from_user.id, open('3.jpg', 'rb'))
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboardBack)
        bot.register_next_step_handler(message, callback_Back, 1)
    elif message.text == 'Назад':
        callback_Back(message,0)
    elif message.text == 'Выход в меню' or message.text == '/start':
        callback_Back(message,0)
    else:
        question = 'Для начала работы напишите /start'
        bot.send_message(message.from_user.id, text=question)
        bot.register_next_step_handler(message, data)


def callback_Serv(message):
    if message.text == 'Консультация' or message.text == 'Другая неисправность' or message.text == 'Предложения':
        question = 'Для составления заявки напишите Ваше Ф.И.О. и должность:'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboardBack)
        bot.register_next_step_handler(message, data_ID)

    elif message.text == 'Неисправность':
        question = ('Перед тем как оставить заявку, убедитесь, что Вашей '
                    'неисправности нет в следующем списке частых проблем и их '
                    'решений:\n\n'
                    '<u>Проблема:</u> По нажатию на кнопку "Подъём каретки" или "Опускание каретки" ничего не происходит.\n'
                    '<i>Причина:</i> Нажата кнопка "Аварийный стоп".\n'
                    '<b>Решение</b> Поверните кнопку "Аварийный стоп" по направлению стрелок до возврата кнопки в отключённое положение.\n\n'
                    '<u>Проблема:</u> После нажатие на кнопку экспозиции излучение отсутствует. Так же отсутствуют показания дозиметра.\n'
                    '<i>Причина:</i> Сработало 10-ти минутное ограничение на подачу излучения.\n'
                    '<b>Решение:</b>  Для сброса нажмите на пульте управления кнопку "Рентгеноскопический таймер".\n\n'
                    '<u>Проблема:</u> Аппарат не включается.\n'
                    '<i>Причина:</i> Ключ находится в положении "Выкл".\n'
                    '<b>Решение:</b> Переведите ключ в положении "Вкл".\n')
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboardAnother)
        bot.register_next_step_handler(message, callback_Serv)
    elif message.text == 'Назад':
        callback_Back(message,0)
    elif message.text == 'Выход в меню' or message.text == '/start':
        callback_Back(message, 0)
    else:
        question = 'Для начала работы напишите /start'
        bot.send_message(message.from_user.id, text=question)
        bot.register_next_step_handler(message, data)


def data_ID(message):
    global personal
    if message.text == 'Назад':
        callback_Back(message,2)
    elif message.text == 'Выход в меню' or message.text == '/start':
        callback_Back(message,0)
    else:
        if message.content_type == 'text' and isFIO(message.text) == 1:
            personal = message.text
            bot.send_message(message.from_user.id, text="Укажите населенный пункт, в котором находится оборудование: ", reply_markup=keyboardBack)
            bot.register_next_step_handler(message, data_city)
        else:
            bot.send_message(message.from_user.id, text="Для составления заявки напишите Ваше Ф.И.О. и должность: ",
                             reply_markup=keyboardBack)
            bot.register_next_step_handler(message, data_ID)

def data_city(message):
    global city
    if message.text == 'Назад':
        callback_Back(message,3)
    elif message.text == 'Выход в меню' or message.text == '/start':
        callback_Back(message,0)
    else:
        if message.content_type == 'text':
            city = message.text
            bot.send_message(message.from_user.id, text="Укажите номер для связи: ", reply_markup=keyboardBack)
            bot.register_next_step_handler(message, data_contact)
        else:
            bot.send_message(message.from_user.id, text="Укажите населенный пункт, в котором находится оборудование: ", reply_markup=keyboardBack)
            bot.register_next_step_handler(message, data_city)

def data_contact(message):
    global phone_number
    if message.text == 'Назад':
        callback_Back(message,4)
    elif message.text == 'Выход в меню' or message.text == '/start':
        callback_Back(message,0)
    else:
        if message.text.isdigit():
            phone_number = message.text
            bot.send_message(message.from_user.id, text="Укажите номер аппарата: ", reply_markup=keyboardBack)
            bot.register_next_step_handler(message, data_machine)
        else:
            bot.send_message(message.from_user.id, text="Укажите номер для связи (только цифры): ", reply_markup=keyboardBack)
            bot.register_next_step_handler(message, data_contact)

def data_machine(message):
    global machine_number
    if message.text == 'Назад':
        callback_Back(message,5)
    elif message.text == 'Выход в меню' or message.text == '/start':
        callback_Back(message,0)
    else:
        if isMashine(message.text) == 1:
            machine_number = message.text
            bot.send_message(message.from_user.id, text="Опишите Ваш запрос. Чем подробнее, тем лучше. "
                                                   '\nЧтобы прислать фото/видео отправьте текст обращения, а после нажмите кнопку "Отправить файл" : ', reply_markup=keyboardBack)
            bot.register_next_step_handler(message, data_question)
        else:
            bot.send_message(message.from_user.id, text="Укажите номер аппарата по форме XX-XX-X / XX-XX-XП: ", reply_markup=keyboardBack)
            bot.register_next_step_handler(message, data_machine)

def data_question(message):
    global text_question
    if message.text == 'Назад':
        callback_Back(message,6)
    elif message.text == 'Выход в меню' or message.text == '/start':
        callback_Back(message,0)
    else:
        if message.content_type == 'text':
            text_question = message.text
            txt ='Проверьте данные заявки:\nОбращение от: ' + str(personal) + '\nНаселенный пункт: ' + str(city)  +'\nНомер телефона: ' + str(phone_number) + (''
                '\nНомер аппарата: ') + str(machine_number) + '\nВопрос: ' + str(text_question) + '\nДата обращения: ' + str(datetime.now().date())
            bot.send_message(message.from_user.id, text=txt)
            question = 'Заявка верна? Нажмите кнопку для отправки файла (при необходимости)'
            bot.send_message(message.from_user.id, text=question, reply_markup=keyboardYN)
            bot.register_next_step_handler(message, callback_YN)
        else:
            question = 'Опишите проблему, для отправки файла нажмите кнопку "Отправить файл"'
            bot.send_message(message.from_user.id, text=question, reply_markup=keyboardBack)
            bot.register_next_step_handler(message, data_question)


def callback_Back(message, button):
    if message.text == 'Назад' and button != 0:
        if button == 1:
            question = 'Наша компания предлагает широкий спектр продукции. \nКакая именно Вас интересует?'
            bot.send_message(message.from_user.id, text=question, reply_markup=keyboardProduct)
            bot.register_next_step_handler(message, callback_Product)
        elif button == 2:
            question = 'С чем связано обращение?'
            bot.send_message(message.from_user.id, text=question, reply_markup=keyboardServ)
            bot.register_next_step_handler(message, callback_Serv)
        elif button == 3:
            question = 'Укажите Ваше Ф.И.О. и должность:'
            bot.send_message(message.from_user.id, text=question)
            bot.register_next_step_handler(message, data_ID)
        elif button == 4:
            bot.send_message(message.from_user.id, text="Укажите населенный пункт, в котором находится оборудование: ", reply_markup=keyboardBack)
            bot.register_next_step_handler(message, data_city)
        elif button == 5:
            bot.send_message(message.from_user.id, text="Укажите номер для связи: ", reply_markup=keyboardBack)
            bot.register_next_step_handler(message, data_contact)
        elif button == 6:
            bot.send_message(message.from_user.id, text="Укажите номер аппарата: ", reply_markup=keyboardBack)
            bot.register_next_step_handler(message, data_machine)
        elif button == 7:
            txt = 'Проверьте данные заявки:\nОбращение от: ' + str(personal) + '\nНаселенный пункт: ' + str(
                city) + '\nНомер телефона: ' + str(phone_number) + (''
                                                                    '\nНомер аппарата: ') + str(
                machine_number) + '\nВопрос: ' + str(text_question) + '\nДата обращения: ' + str(datetime.now().date())
            bot.send_message(message.from_user.id, text=txt)
            question = 'Заявка верна? Нажмите кнопку для отправки файла (при необходимости)'
            bot.send_message(message.from_user.id, text=question, reply_markup=keyboardYN)
            bot.register_next_step_handler(message, callback_YN)
    elif message.text == 'Выход в меню' or button == 0:
        question = 'Чем могу помочь?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
        bot.register_next_step_handler(message, callback_worker)

def callback_file(message):
    if message.text == 'Назад':
        callback_Back(message,  7)
    elif message.text == 'Выход в меню' or message.text == '/start':
        callback_Back(message, 0)
    else:
        if message.content_type != 'text':
            bot.forward_message(TO_CHAT_ID, message.from_user.id, message.id)
            bot.send_message(TO_CHAT_ID, text='ID: ' + str(message.from_user.id) + '\nДата обращения: ' + str(datetime.now().date()))
            txt = ('Обращение от: ' + str(personal) + '\nНаселенный пункт: ' + str(city) + '\nНомер телефона: ' + str(phone_number) + '\nНомер аппарата: ' +
                   str(machine_number) + '\nВопрос: ' + str(text_question) + '\nДата обращения: ' + str(datetime.now().date()))
            bot.send_message(message.from_user.id, text=txt)
            question = 'Заявка верна? (файл принят)'
            bot.send_message(message.from_user.id, text=question, reply_markup=keyboardYN)
            bot.register_next_step_handler(message, callback_YN)
        else:
            bot.send_message(message.from_user.id, text= 'Пожалуйста, отправьте файл (фото, видео, аудио, документ)')
            bot.register_next_step_handler(message, callback_file)

def callback_answer(message, FROM_CHAT_ID):
    if message.content_type == 'text':
        txt = message.text
        bot.send_message(FROM_CHAT_ID, text=txt)
    elif message.content_type == 'photo':
        bot.send_photo(FROM_CHAT_ID, message.photo[-1].file_id)
    elif message.content_type == 'video':
        bot.send_video(FROM_CHAT_ID, message.video.file_id)
    elif message.content_type == 'document':
        bot.send_document(FROM_CHAT_ID, message.document.file_id)
    else:
        bot.send_message(TO_CHAT_ID, text='Формат неверен, отправьте текст, фото, видео или документ')
        bot.register_next_step_handler(message, callback_answer, FROM_CHAT_ID)
    question = 'Отправить еще файл по этой заявке?'
    bot.send_message(TO_CHAT_ID, text=question, reply_markup=keyboardOperator)
    bot.register_next_step_handler(message, callback_Operator, FROM_CHAT_ID)

def callback_Operator(message, FROM_CHAT_ID):
    if message.text == 'Отправить еще ответ':
        bot.send_message(TO_CHAT_ID, text='Отправьте текст, фото или документ по заявке ' + str(FROM_CHAT_ID))
        bot.register_next_step_handler(message, callback_answer, FROM_CHAT_ID)
    elif message.text == 'Следующая заявка':
        question = ('Пожалуйста, оцените сервис от 1 до 5')
        bot.send_message(FROM_CHAT_ID, text=question, reply_markup=keyboardValue)
        bot.send_message(message.from_user.id, text='Введите ID обращения: ')
        bot.register_next_step_handler(message, callback_worker)
    else:
        bot.send_message(TO_CHAT_ID, text='Чтоб ответить на заявку напишите /service', reply_markup=types.ReplyKeyboardRemove())
        question = ('Пожалуйста, оцените сервис от 1 до 5')
        bot.send_message(FROM_CHAT_ID, text=question, reply_markup=keyboardValue)
        bot.register_next_step_handler(message, data)



@bot.callback_query_handler(lambda call: True)
def callback_inline(call):

    fs = open('service_id.txt', 'a')
    if call.data == "1":
        fs.write(str(call.message.from_user.id) + '      1             ' + str(TO_CHAT_ID) + '           ' + str(datetime.now().date()) + "\n")
    elif call.data == "2":
        fs.write(str(call.message.from_user.id) + '      2             ' + str(TO_CHAT_ID) + '           ' + str(datetime.now().date()) + "\n")
    elif call.data == "3":
        fs.write(str(call.message.from_user.id) + '      3             ' + str(TO_CHAT_ID) + '           ' + str(datetime.now().date()) + "\n")
    elif call.data == "4":
        fs.write(str(call.message.from_user.id) + '      4             ' + str(TO_CHAT_ID) + '           ' + str(datetime.now().date()) + "\n")
    elif call.data == "5":
        fs.write(str(call.message.from_user.id) + '      5             ' + str(TO_CHAT_ID) + '           ' + str(datetime.now().date()) + "\n")
    fs.close()
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    question = ('Спасибо за обращение!')
    bot.send_message(call.message.chat.id, text=question)
 #   bot.register_next_step_handler(message, data)

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row('Продукция', 'Сервисная служба')
keyboard.row( 'Обучение инженеров')

keyboardYN = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboardYN.row('Да', 'Нет')
keyboardYN.row('Отправить файл', 'Выход в меню')

keyboardProduct = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboardProduct.row('С-Дуга', 'Рентген. защита')
keyboardProduct.row('Негатоскоп', 'Выход в меню')

keyboardServ = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboardServ.row('Консультация', 'Неисправность')
keyboardServ.row('Выход в меню', 'Предложения')

keyboardAnother = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboardAnother.row('Другая неисправность', 'Выход в меню')

keyboardBack= types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboardBack.row('Назад','Выход в меню')

keyboardEdit = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboardEdit.row('Личные данные', 'Номер телефона')
keyboardEdit.row('Номер аппарата', 'Текст вопроса')

keyboardOperator = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboardOperator.row('Отправить еще ответ','Следующая заявка')
keyboardOperator.row('Стоп')

keyboardValue = types.InlineKeyboardMarkup()
key_1 = types.InlineKeyboardButton(text='1', callback_data='1')
key_2 = types.InlineKeyboardButton(text='2', callback_data='2')
key_3 = types.InlineKeyboardButton(text='3', callback_data='3')
key_4 = types.InlineKeyboardButton(text='4', callback_data='4')
key_5 = types.InlineKeyboardButton(text='5', callback_data='5')
keyboardValue.add(key_1, key_2, key_3, key_4, key_5)

#if __name__ == 'main':
#    executor.start_polling(dp, skip_updates=True)

try:
    bot.polling(none_stop=True, interval=0)
except:
    pass