import telebot
from telebot import types
import openpyxl

bot = telebot.TeleBot('5323975739:AAGJjjbV3s_ZwWiOmvfqLGkkrwRhVMrzt68')

book = openpyxl.open('price.xlsx', read_only=True)
sheet = book.active

class User:
    def __init__(self, phone):
        self.phone = phone
        self.model = None
        self.problem = 5
        self.check = None
        self.money = 0

class Check:
    def __init__(self, chapter):
        self.chapter = False
        self.model = None
        self.order = None
        self.problem = None
        self.user = None
        self.chat = False

user_dict = {}
user_dict2 = {}

admin = 455284316
manager = 455284316
chat_group = -796330575




@bot.message_handler(commands=['chat'])
def chat(message):
    check = user_dict2[message.chat.id]  # открыл словарь проверки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)  # Создаем клавиатуру для отмены чата
    markup.add(types.KeyboardButton('Завершить чат'))
    if check.chat == True: # если уже активирован чат с менеджером
        bot.send_message(message.chat.id, 'У вас уже активен чат с менеджером, пожалуйста дождитесь ответа ⏳\n\n  Для того чтобы отменить запрос введите напишите "Завершить чат"')
    if check.chat == False: # если нет активных чатов
        bot.send_message(message.chat.id, "Здравствуйте! Вы начали чат с нашим менеджером.\n"
                                          "Введите ваш вопрос и ожидайте ответа.", reply_markup=markup)  # Отправляем сообщение пользователю с приветствием и инструкцией по использованию
        bot.send_message(chat_id=manager, text="Начат чат с пользователем {} (ID: {}).".format(message.chat.first_name, message.chat.id))  # Отправляем сообщение менеджеру о начале чата
    check.chat = True

@bot.message_handler(commands=['no_chat'])
def no_chat(message):
    check = user_dict2[message.chat.id]  # открыл словарь проверки
    if check.chat == False:
        bot.send_message(message.chat.id, 'На данный момент чат с менеджером закрыт, если вы хотетите проконсультироваться по поводу ремонта смартфона\
     воспользуйтесь командой /chat')
    elif check.chat == True:
        bot.send_message(message.chat.id, '    Чат  закрыт!✅ \n\n /start')
    check.chat = False

@bot.message_handler(commands=['start'])
def start(message):
    user_dict2[message.chat.id] = Check(message.text)  # создал словарь проверки
    check = user_dict2[message.chat.id]  # открыл словарь проверки
    check.chapter = None
    check.model = None

    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    sloman = types.KeyboardButton('У меня сломался телефон')
    status = types.KeyboardButton(text="Узнать статус заказа", request_contact=True)
    interes = types.KeyboardButton('Посмотреть/почитать что-нибудь интересненькое')
    murkup.add(sloman, status)
    privet = f'<b>Приветсвтую {message.from_user.first_name}</b>,\n Я бот сервисного центра по ремонту смартфонов в Одессе!\n\n<b>С моей помощью можно:</b>\n\n-Получить консультаци. и узнать стоимость ремонта устройства, оформить заявку на ремонт\n\n-Проверить статус заказа если уже оставили на ремонт устройство\n\n-Узнать много полезного\n\nДля консультации с менеджером введите команду /chat'
    bot.send_message(message.chat.id, privet, reply_markup=murkup, parse_mode='html')
    print(message.chat.id)

@bot.message_handler(content_types=['text'])
# def process_user_msg(message):
#     # Если пользователь нажимает кнопку "Завершить чат", завершаем обработку сообщений
#     if message.text == 'Завершить чат':
#         bot.send_message(chat_id=message.chat.id, text="Чат завершен. Спасибо, что обратились к нам!")
#         return
#
#     # Отправляем сообщение менеджеру
#     bot.send_message(chat_id=manager, text="Сообщение от пользователя {} (ID: {}):\n{}".format(message.chat.first_name, message.chat.id, message.text))
#
#     # Регистрируем следующий обработчик для получения ответа от менеджера
#     bot.send_message(chat_id=message.chat.id, text="Ожидайте ответа от менеджера...")
#     bot.register_next_step_handler_by_chat_id(chat_id=manager, message_cb=process_manager_msg, text=message.text)
#
# def process_manager_msg(message):
#     # Отправляем ответ пользователю
#     bot.send_message(chat_id=message.text.split('(ID: ')[1].split('):\n')[0], text="Ответ от менеджера:\n{}".format(message.text.split(':\n')[1]))
#
#     # Регистрируем следующий обработчик для получения следующего сообщения от пользователя
#     bot.register_next_step_handler(message.chat.id, callback=process_user_msg)

def eho(message):
    try:
        print(message.text)
        user_dict[message.chat.id] = User(message.text)  # cоздание словарь
        check = user_dict2[message.chat.id]  # открыл словарь проверки
        if check.chat == True:
            if manager != message.chat.id:   #условия для пользователя с откртым чатом
                bot.send_message(manager, message.chat.id)
                bot.send_message(manager, f'{message.from_user.first_name}: {message.text}')
                if check.problem == None:
                    bot.send_message(message.chat.id, '    Менеджер получил ваше сообщение, пожалуйста ожидайте ответа.\n    График работы "Пн-Сб с10:00 до 18:00"\n\n\
                    Чтобы прекратить чат, введите команду /no_chat')
                    check.problem = message.text
            if manager == message.chat.id: #условия для менеджера с открытым чатом
                if message.text.lower() == 'закрыть':
                    check = user_dict2[check.user]
                    check.chat = False
                    bot.send_message(message.chat.id, f'Чат с {check.user} отключен')
                elif message.text.lower() == 'текущий чат':
                    bot.send_message(manager, f'Чат с {check.user}')
                else:
                    try:
                        bot.send_message(check.user, message.text)
                        bot.send_message(message.chat.id, f'Отправлено: {check.user}\n{message.text}')
                    except:
                        bot.send_message(message.chat.id, 'Некорректный id пользователя')

        elif message.chat.id == manager: #меню менеджера
            if message.text != None:
                 try:
                    if int(message.text) < int('1000000'):
                        bot.send_message(message.chat.id, 'Слишком короткий id')
                    elif int(message.text) > int('10000000000'):
                        bot.send_message(message.chat.id, 'Слишком длинный id')
                    else:
                        int(message.text)
                        check.user = message.text
                        check.chat = True
                        bot.send_message(message.chat.id, f'Чат с {check.user} открыт')
                 except:
                    bot.send_message(message.chat.id, '     Введите id пользователя')
            elif message.text.lower() == 'текущий чат':
                bot.send_message(manager, f'Чат с {check.user}')
            elif message.text.lower() == 'Закрыть чат':
                bot.send_message(manager, 'Чат с пользователем закрыт')
                bot.send_message(check.user, 'Чат закрыт')
                check.chat = False
            elif message.text == type(int):
                try:
                    check.user = int(message.text)
                    bot.send_message(manager, f'Чат с {check.user} открыт')
                except:
                    bot.send_message(manager, 'Что-то не так')








        elif message.text.lower() == 'ремонт':
            check.model = None
            check.problem = None
            check.chapter = 'castom'

            user = user_dict[message.chat.id]
            user.model = None

            photo = open('cartinios/repair.jpg', 'rb')
            markup = types.InlineKeyboardMarkup(row_width=1)
            samsung = types.InlineKeyboardButton(text='Samsung', callback_data='Устройство Samsung')
            apple = types.InlineKeyboardButton(text='Apple', callback_data='Устройство Apple')
            huawei = types.InlineKeyboardButton(text='Huawei', callback_data='Устройство Huawei')
            xiaomi_redmi = types.InlineKeyboardButton(text='Xiaomi Redmi', callback_data='Устройство Xiaomi')
            oppo_realme = types.InlineKeyboardButton(text='Oppo Realme', callback_data='Устройство Oppo')
            markup.add(samsung, huawei, xiaomi_redmi, oppo_realme, apple)
            bot.send_photo(message.chat.id, photo, reply_markup=markup)
        elif message.text.lower() == 'у меня сломался телефон':
            check.model = None
            check.chapter = None

            murkup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            cons = types.KeyboardButton('Получить консультацию')
            remont = types.KeyboardButton('Ремонт')
            murkup.add(cons, remont)
            bot.send_message(message.chat.id,
                             'Напишите "Ремонт" если хотите оставить заявку на ремонт смартфона. \nИли выберите "Получить консультацию" (рекомендуется)',
                             reply_markup=murkup, parse_mode='html')
        elif message.text.lower() == 'получить консультацию':
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            connector = types.InlineKeyboardButton('Не заряжается')
            voda = types.InlineKeyboardButton('Упал в воду')
            gluk = types.KeyboardButton('Глючит, зависает')
            razbit = types.KeyboardButton('Разбит дисплей, трещины')
            zvyk = types.KeyboardButton('Проблемы со звуком')
            razryazh = types.KeyboardButton('Быстро разряжается')
            drugoe = types.KeyboardButton('Другое')
            markup.add(connector, voda, gluk, razbit, zvyk, razryazh, drugoe)
            problem = f'Проблема которую вы наблюдаете?'

            bot.send_message(message.chat.id, problem, reply_markup=markup)
        elif message.text.lower() == 'не заряжается':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item_next = types.InlineKeyboardButton(text='Дальше', callback_data='consultation_connector')
            markup.add(item_next)
            bot.send_message(message.chat.id,
                             '*Проблемы с зарядкой могут быть сязаны с:*\n*а:* Неисправен кабель \n*б:* Неисправен блочёк\n*в: *Забился, загрязнился разъем в телефоне\n*г: *Cломался / расшатался разъем',
                             parse_mode='markdown', reply_markup=markup)
        elif message.text.lower() == 'упал в воду':
            markup = types.InlineKeyboardMarkup()
            item_next = types.InlineKeyboardButton(text='Дальше', callback_data='consultation_voter')
            markup.add(item_next)
            bot.send_message(message.chat.id,
                             'Если в ваш телефон попала влага, нужно его  немедленно разобрать и промыть плату специальной жидкостью не оставляющей никаких остатков. При этом не повредить подсветку дисплея, микрофоны и камеры. Вообщем чистку могут выполнить только в сервисном центре.',
                             reply_markup=markup)
        elif message.text.lower() == 'глючит, зависает':
            markup = types.InlineKeyboardMarkup()
            item_next = types.InlineKeyboardButton(text='Дальше', callback_data='consultation_buggy')
            markup.add(item_next)

            bot.send_message(message.chat.id,
                             'Что делать, если телефон зависает?\n[ПРИЧИНЫ ЗАВИСАНИЯ ТЕХНИКИ](https://teletype.in/@andrei_iph/P_-KoDBU2Sr)',
                             parse_mode='markdown', reply_markup=markup)
        elif message.text.lower() == 'разбит дисплей, трещины':
            markup = types.InlineKeyboardMarkup(row_width=1)
            option1 = types.InlineKeyboardButton(text='Есть трещины но пользоваться можно',
                                                 callback_data='consultation_broken_option1')
            option2 = types.InlineKeyboardButton(text='Нет трещин но черный экран',
                                                 callback_data='consultation_broken_option2')
            option3 = types.InlineKeyboardButton(text='Разбит полность пользоваться невозможно',
                                                 callback_data='consultation_broken_option3')
            markup.add(option1, option2, option3)

            bot.send_message(message.chat.id,
                             'Если так случилось что экран вашего смрфона пострадал - не унывайте, мы поможем вам это исправить в кратчайшие сроки но для начала нужно понимать насколько сильный ущерб принял на себя гаджет',
                             reply_markup=markup)
        elif message.text.lower() == 'проблемы со звуком':
            markup = types.InlineKeyboardMarkup(row_width=1)
            item_next = types.InlineKeyboardButton(text='Дальше', callback_data='consultation_sound')
            markup.add(item_next)

            bot.send_message(message.chat.id, 'Прохо слышите собеседника?\nИли вас не слишит собеседник?\n   Важно правильно ответить на этот вопрос так как в первом случае неисправен спикер(разговорный динамик) во втором микрофон.\n\
                В современном смарфоне встроено порядка 3-4х микрофонов и несколько динамиков как правило один снизу и один  возможно двухконтурный сверху если у вас стерео звук на телефоне.\n\
                Сам динамик очень редко выходит из строя, физически навредить ему можно либо проткнув мембрану иголкой либо мелкая металическая стружка. В противном случае достаточно правильно прочистить защитную решетку.',
                             reply_markup=markup)
        elif message.text.lower() == 'другое':
            bot.send_message(message.chat.id, 'Дя того чтобы начать чат с менеджером введите команду /chat')
        elif check.model != None:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            back = types.KeyboardButton('Ремонт')
            contact = types.KeyboardButton('🖊️Подтвердить заказ', request_contact=True)
            markup.add(back, contact)

            check.problem = message.text #записали проблему
            check.order = True

            bot.send_message(message.chat.id, f'Устройство: {check.model} 📱 \n\n🛠 {check.problem}\n\n   Пришлите сообщение еще раз если хотите изменить описание проблемы\n    Для того чтобы отправить запрос менеджеру, поделитесь номером телефона нажав кнопкку "Подтвердить". Или отправте контакт', reply_markup=markup)
        elif check.chapter == True:
            bot.send_message(manager, message.chat.id)
            bot.send_message(manager, message.text)
            bot.send_message(message.chat.id, 'Ожидайте ответа менеджера в ближайшее время \n\nКоманда /start')
        elif check.chapter == None:
            photo = open('cartinios/keyboard.jpg', 'rb')
            bot.send_photo(message.chat.id, photo, 'Пожалуйста воспользуйтесь встроенной клаиватурой \n\nКоманда /start')
        elif check.chapter == 'castom':  #если человек вводит модель вручную в разделе "Ремонт"
            check.model = message.text #записал модель

            markup = types.InlineKeyboardMarkup()  # клавиатура да нет
            yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
            no = types.InlineKeyboardButton(text='Нет', callback_data='no')
            markup.add(yes, no)

            bot.send_message(message.chat.id, f'Ваш телефон "{check.model}"?', reply_markup=markup)
    except:
        bot.send_message(message.chat.id, 'Воспользуйтесь меню /start')



@bot.callback_query_handler(func=lambda call: call.data.startswith('repair'))
def repair_call(call):
    check = user_dict2[call.message.chat.id]  # открыл словарь проверки
    check.chapter = 'castom'
    photo = open('cartinios/repair.jpg', 'rb')
    markup = types.InlineKeyboardMarkup(row_width=1)
    samsung = types.InlineKeyboardButton(text='Samsung', callback_data='Устройство Samsung')
    apple = types.InlineKeyboardButton(text='Apple', callback_data='Устройство Apple')
    huawei = types.InlineKeyboardButton(text='Huawei', callback_data='Устройство Huawei')
    xiaomi_redmi = types.InlineKeyboardButton(text='Xiaomi Redmi', callback_data='Устройство Xiaomi')
    oppo_realme = types.InlineKeyboardButton(text='Oppo Realme', callback_data='Устройство Oppo')
    markup.add(samsung, huawei, xiaomi_redmi, oppo_realme, apple)
    bot.edit_message_media(media=types.InputMedia(type='photo', media=photo), chat_id=call.message.chat.id,
                                 message_id=call.message.message_id, reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data.startswith('Устройство'))
def func_phone(call):
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton(text='⬅️Назад', callback_data='repair')
    photo = open(f'cartinios/{call.data}.jpg', 'rb')
    if call.data == 'Устройство Samsung':
        markup = types.InlineKeyboardMarkup(row_width=1)
        a = types.InlineKeyboardButton(text='Galaxy A', callback_data='galaxy a')
        s = types.InlineKeyboardButton(text='Galaxy S', callback_data='galaxy s')
        note = types.InlineKeyboardButton(text='Galaxy Note', callback_data='galaxy note')
        j = types.InlineKeyboardButton(text='Galaxy J', callback_data='galaxy j')
        m = types.InlineKeyboardButton(text='Galaxy M', callback_data='galaxy m')
        markup.add(a, s, note, j, m, back)
    elif call.data == 'Устройство Huawei':
        nova = types.InlineKeyboardButton(text='Nova', callback_data='huawei nova')
        hy = types.InlineKeyboardButton(text='Y', callback_data='huawei y')
        honor = types.InlineKeyboardButton(text='Honor', callback_data='huawei honor')
        hp = types.InlineKeyboardButton(text='P', callback_data='huawei hp')
        mate = types.InlineKeyboardButton(text='Mate', callback_data='huawei mate')
        other = types.InlineKeyboardButton(text='Enjoy', callback_data='huawei enjoy')
        markup.add(nova, hy, honor, hp, other, back)
    elif call.data == 'Устройство Xiaomi':
        mi = types.InlineKeyboardButton(text='MI', callback_data='xiaomi mi')
        redmi = types.InlineKeyboardButton(text='Redmi', callback_data='xiaomi redmi')
        poco = types.InlineKeyboardButton(text='Poco', callback_data='xiaomi poco')
        markup.add(mi, redmi, back)
    elif call.data == 'Устройство Apple':
        iph_6s = types.InlineKeyboardButton(text='6s', callback_data='2')
        iph_6s_plus = types.InlineKeyboardButton(text='6s Plus', callback_data='3')
        iph_7 = types.InlineKeyboardButton(text='7', callback_data='4')
        iph_7_Plus = types.InlineKeyboardButton(text='7 Plus', callback_data='5')
        iph_8 = types.InlineKeyboardButton(text='8', callback_data='6')
        iph_8_plus = types.InlineKeyboardButton(text='8 Plus', callback_data='7')
        iph_x = types.InlineKeyboardButton(text='X', callback_data='8')
        iph_xs = types.InlineKeyboardButton(text='Xs', callback_data='9')
        iph_xs_max = types.InlineKeyboardButton(text='Xs Max', callback_data='10')
        iph_xr = types.InlineKeyboardButton(text='Xr', callback_data='11')
        iph_11 = types.InlineKeyboardButton(text='11', callback_data='12')
        iph_11_pro = types.InlineKeyboardButton(text='11 Pro', callback_data='13')
        iph_11_pro_max = types.InlineKeyboardButton(text='11 Pro Max', callback_data='14')
        iph_12_mini = types.InlineKeyboardButton(text='12 mini', callback_data='15')
        iph_12 = types.InlineKeyboardButton(text='12', callback_data='16')
        iph_12_pro = types.InlineKeyboardButton(text='12 Pro', callback_data='17')
        iph_12_pro_max = types.InlineKeyboardButton(text='12 Pro Max', callback_data='18')
        iph_13_mini = types.InlineKeyboardButton(text='13 mini', callback_data='19')
        iph_13 = types.InlineKeyboardButton(text='13', callback_data='20')
        iph_13_pro = types.InlineKeyboardButton(text='13 Pro', callback_data='21')
        iph_13_pro_max = types.InlineKeyboardButton(text='13 Pro Max', callback_data='22')
        markup.add(iph_6s, iph_6s_plus, iph_7, iph_7_Plus, iph_8, iph_8_plus, iph_x, iph_xs, iph_xs_max, iph_xr, iph_11,
                   iph_11_pro, iph_11_pro_max, iph_12_mini, iph_12, iph_12_pro, iph_12_pro_max, iph_13_mini, iph_13,
                   iph_13_pro, iph_13_pro_max, back)
    elif call.data == 'Устройство Oppo':

        bot.register_next_step_handler(xiaomi)
    bot.edit_message_media(media=types.InputMedia(type='photo', media=photo), chat_id=call.message.chat.id,
                           message_id=call.message.message_id, reply_markup=markup)  # отправил фото с клавиатурой
@bot.callback_query_handler(func=lambda call: call.data.startswith('xiaomi'))
def phone_xiaomi(call):
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton(text='⬅️Назад', callback_data='Устройство: Xiaomi')
    if call.data == 'xiaomi mi':
        _8 = types.InlineKeyboardButton(text='8', callback_data='146')
        _8se = types.InlineKeyboardButton(text='8SE', callback_data='148')
        _8_lite = types.InlineKeyboardButton(text='8 lite', callback_data='147')
        _9 = types.InlineKeyboardButton(text='9', callback_data='155')
        _9se = types.InlineKeyboardButton(text='9SE', callback_data='157')
        _9_lite = types.InlineKeyboardButton(text='9 lite', callback_data='156')
        _9_pro = types.InlineKeyboardButton(text='9 pro', callback_data='2')
        _10 = types.InlineKeyboardButton(text='10', callback_data='2')
        note_10 = types.InlineKeyboardButton(text='Note 10', callback_data='2')
        note_10_pro = types.InlineKeyboardButton(text='Note 10 pro', callback_data='2')
        note_10_lite = types.InlineKeyboardButton(text='Note 10 lite', callback_data='2')
        _10_pro = types.InlineKeyboardButton(text='10 pro', callback_data='2')
        _10_ultra = types.InlineKeyboardButton(text='10 Ultra', callback_data='2')
        _10i = types.InlineKeyboardButton(text='10i', callback_data='2')
        _10_lite = types.InlineKeyboardButton(text='10 lite', callback_data='2')
        _11 = types.InlineKeyboardButton(text='11', callback_data='2')
        _11_pro = types.InlineKeyboardButton(text='11 pro', callback_data='2')
        _11_ultra = types.InlineKeyboardButton(text='11 Ultra', callback_data='2')
        _11i = types.InlineKeyboardButton(text='11i', callback_data='2')
        _11_lite = types.InlineKeyboardButton(text='11 lite', callback_data='2')
        max_2 = types.InlineKeyboardButton(text='MAX 2', callback_data='2')
        max_3 = types.InlineKeyboardButton(text='MAX 3', callback_data='2')
        mix = types.InlineKeyboardButton(text='MIX', callback_data='2')
        mix_2 = types.InlineKeyboardButton(text='MIX 2', callback_data='2')
        mix_2s = types.InlineKeyboardButton(text='MIX 2s', callback_data='2')
        mix_3 = types.InlineKeyboardButton(text='MIX 3', callback_data='2')
        a1 = types.InlineKeyboardButton(text='A1', callback_data='2')
        a2 = types.InlineKeyboardButton(text='A2', callback_data='2')
        a2_lite = types.InlineKeyboardButton(text='A2 lite', callback_data='2')
        a3 = types.InlineKeyboardButton(text='A3', callback_data='2')
        _9t = types.InlineKeyboardButton(text='(9T', callback_data='2')
        _10t = types.InlineKeyboardButton(text='10T', callback_data='2')
        markup.add(_8, _8se, _8ee, _8_lite, _9, _9se, _9_lite, _9_pro, _10, note_10, note_10_pro, note_10_lite, _10_pro,
                   _10_ultra, _10i, _10_lite, _11, _11_pro, _11_ultra, _11i, _11_lite, max_2, max_3, mix, mix_2, mix_2s,
                   mix_3, a1, a2, a2_lite, a3, _9t, _10t, back)
    elif call.data == 'xiaomi redmi':
        _4 = types.InlineKeyboardButton(text='4x', callback_data='110')
        _4x = types.InlineKeyboardButton(text='4x', callback_data='111')
        _note_4 = types.InlineKeyboardButton(text='Note 4', callback_data='112')
        _note_4x = types.InlineKeyboardButton(text='Note 4x', callback_data='113')
        _5 = types.InlineKeyboardButton(text='5', callback_data='114')
        _5a = types.InlineKeyboardButton(text='5A', callback_data='116')
        _5_plus = types.InlineKeyboardButton(text='5 Plus', callback_data='115')
        _note_5 = types.InlineKeyboardButton(text='Note 5', callback_data='117')
        _s2 = types.InlineKeyboardButton(text='S2', callback_data='118')
        _6 = types.InlineKeyboardButton(text='6', callback_data='119')
        _6a = types.InlineKeyboardButton(text='6A', callback_data='120')
        _note_6 = types.InlineKeyboardButton(text='Note 6', callback_data='121')
        _6pro = types.InlineKeyboardButton(text='6 pro', callback_data='122')
        _7 = types.InlineKeyboardButton(text='7', callback_data='123')
        _go = types.InlineKeyboardButton(text='GO', callback_data='124')
        _7a = types.InlineKeyboardButton(text='7A', callback_data='125')
        _note_7 = types.InlineKeyboardButton(text='Note 7', callback_data='126')
        _8 = types.InlineKeyboardButton(text='8', callback_data='127')
        _8a = types.InlineKeyboardButton(text='8A', callback_data='128')
        _note_8 = types.InlineKeyboardButton(text='Note 8', callback_data='129')
        _note_8t = types.InlineKeyboardButton(text='Note 8T', callback_data='130')
        _note_8pro = types.InlineKeyboardButton(text='Note 8pro', callback_data='131')
        _9 = types.InlineKeyboardButton(text='9', callback_data='132')
        _9a = types.InlineKeyboardButton(text='9A', callback_data='133')
        _9c = types.InlineKeyboardButton(text='9C', callback_data='134')
        _9t = types.InlineKeyboardButton(text='9T', callback_data='135')
        _note_9 = types.InlineKeyboardButton(text='Note 9', callback_data='136')
        _note_9s = types.InlineKeyboardButton(text='Note 9s', callback_data='137')
        _note_9pro = types.InlineKeyboardButton(text='Note 9 pro', callback_data='132')
        _10 = types.InlineKeyboardButton(text='10', callback_data='139')
        _note_10 = types.InlineKeyboardButton(text='Note 10', callback_data='140')
        _note_10x = types.InlineKeyboardButton(text='10x', callback_data='141')
        _note_10t_5g = types.InlineKeyboardButton(text='Note 10t 5g', callback_data='142')
        k40 = types.InlineKeyboardButton(text='K40', callback_data='143')
        markup.add(_4, _4x, _note_4, _note_4x, _5, _5a, _5_plus, _note_5, _s2, _6, _6a, _note_6, _6pro, _7, _7a,
                   _note_7, _8, _8a, _note_8, _note_8t, _note_8pro, _9, _9a, _9c, _9t, _note_9, _note_9pro, _note_9s,
                   _10, _note_10, _note_10x, _note_10t_5g, k40, back)
    elif call.data == 'xiaomi poco':
        f1 = types.InlineKeyboardButton(text='F1', callback_data='166')
        c3 = types.InlineKeyboardButton(text='C3', callback_data='167')
        f2pro = types.InlineKeyboardButton(text='F2 pro', callback_data='168')
        m2 = types.InlineKeyboardButton(text='M2', callback_data='169')
        m2pro = types.InlineKeyboardButton(text='M2 pro', callback_data='170')
        m3 = types.InlineKeyboardButton(text='M3', callback_data='172')
        m3pro = types.InlineKeyboardButton(text='M3 pro', callback_data='171')
        x2 = types.InlineKeyboardButton(text='Note 10', callback_data='173')
        x3 = types.InlineKeyboardButton(text='Note 10', callback_data='174')
        x3pro = types.InlineKeyboardButton(text='Note 10', callback_data='175')
        m4 = types.InlineKeyboardButton(text='Note 10', callback_data='M4 pro')
        markup.add(f1, c3, f2pro, m2, m2pro, m3, m3pro, x2, x3, x3pro, m4)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Выберте модель', reply_markup=markup)
    # msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
    #                       text='Укажите модель')
    # bot.register_next_step_handler(msg, xiaomi)
    # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Ваша модель, {user.model}?')

    if call.data == 'Устройство: Oppo Realme':
        markup = types.InlineKeyboardMarkup()
        iph_6s = types.InlineKeyboardButton(text='6s', callback_data='2')
        back = types.InlineKeyboardButton(text='Назад', switch_inline_query=call.message.text)
        markup.add(a, s, note, j, m, back)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберите серию',
                              reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data.startswith('galaxy'))
def phone_samsung_galaxy(call):
    photo = open(f'cartinios/{call.data}.jpg', 'rb')
    back = types.InlineKeyboardButton(text='⬅️Назад', callback_data='Устройство Samsung')
    markup = types.InlineKeyboardMarkup()
    if call.data == 'galaxy a':
        a6 = types.InlineKeyboardButton(text='A6', callback_data='33')
        a6_plus = types.InlineKeyboardButton(text='A6+', callback_data='34')
        a7 = types.InlineKeyboardButton(text='A7 (2018)', callback_data='32')
        a8 = types.InlineKeyboardButton(text='A8', callback_data='35')
        a8_plus = types.InlineKeyboardButton(text='A8+', callback_data='36')
        a3 = types.InlineKeyboardButton(text='A3 (2017)', callback_data='40')
        a5 = types.InlineKeyboardButton(text='A5 (2017)', callback_data='39')
        a72017 = types.InlineKeyboardButton(text='A7 (2017)', callback_data='38')
        a30s = types.InlineKeyboardButton(text='A30s', callback_data='24')
        a31 = types.InlineKeyboardButton(text='A31', callback_data='25')
        a32 = types.InlineKeyboardButton(text='A32', callback_data='49')
        a10 = types.InlineKeyboardButton(text='A10', callback_data='26')
        a20 = types.InlineKeyboardButton(text='A20', callback_data='27')
        a30 = types.InlineKeyboardButton(text='A30', callback_data='28')
        a40 = types.InlineKeyboardButton(text='A40', callback_data='29')
        a50 = types.InlineKeyboardButton(text='A50', callback_data='30')
        a51 = types.InlineKeyboardButton(text='A51', callback_data='41')
        a52 = types.InlineKeyboardButton(text='A52', callback_data='50')
        a71 = types.InlineKeyboardButton(text='A71', callback_data='42')
        a72 = types.InlineKeyboardButton(text='A72', callback_data='51')
        a01 = types.InlineKeyboardButton(text='A01', callback_data='43')
        a02 = types.InlineKeyboardButton(text='A02', callback_data='52')
        a02s = types.InlineKeyboardButton(text='A02s', callback_data='47')
        a11 = types.InlineKeyboardButton(text='A11', callback_data='45')
        a12 = types.InlineKeyboardButton(text='A12', callback_data='46')
        a21s = types.InlineKeyboardButton(text='A21s', callback_data='47')
        a10s = types.InlineKeyboardButton(text='A10s', callback_data='53')
        a41 = types.InlineKeyboardButton(text='A41', callback_data='54')
        markup.add(a6, a6_plus, a7, a8, a8_plus, a3, a5, a72017, a30s, a31, a10, a10s, a20, a30, a32, a40, a41, a50,
                   a51, a52, a71, a72, a01, a02, a02s, a11, a12, a21s, back)
    if call.data == 'galaxy s':
        s9 = types.InlineKeyboardButton(text='S9', callback_data='72')
        s9_plus = types.InlineKeyboardButton(text='S9 Plus', callback_data='73')
        s8_plus = types.InlineKeyboardButton(text='S8 Plus', callback_data='74')
        s8 = types.InlineKeyboardButton(text='S8', callback_data='75')
        s10 = types.InlineKeyboardButton(text='S10', callback_data='69')
        s10e = types.InlineKeyboardButton(text='S10e', callback_data='70')
        s10_plus = types.InlineKeyboardButton(text='S10 Plus', callback_data='71')
        s10_lite = types.InlineKeyboardButton(text='S10 Lite', callback_data='76')
        s20 = types.InlineKeyboardButton(text='S20', callback_data='77')
        s20_plus = types.InlineKeyboardButton(text='S20 Plus', callback_data='78')
        s20_ultra_5g = types.InlineKeyboardButton(text='s20 Ultra 5g', callback_data='79')
        s21 = types.InlineKeyboardButton(text='S21', callback_data='80')
        s21_ultra = types.InlineKeyboardButton(text='S21 Ultra', callback_data='81')
        s21_plus = types.InlineKeyboardButton(text='S21 Plus', callback_data='82')
        markup.add(s8, s8_plus, s9, s9_plus, s10, s10e, s10_plus, s10_plus, s10_lite, s20, s20_plus, s20_ultra_5g, s21,
                   s21_ultra, s21_plus, back)
    if call.data == 'galaxy note':
        markup = types.InlineKeyboardMarkup(row_width=2)
        note_8 = types.InlineKeyboardButton(text='Note 8', callback_data='83')
        note_9 = types.InlineKeyboardButton(text='Note 9', callback_data='83')
        note_10 = types.InlineKeyboardButton(text='Note 10', callback_data='84')
        note_10_plus = types.InlineKeyboardButton(text='Note 10 Plus', callback_data='85')
        note_20_ultra = types.InlineKeyboardButton(text='Note 20 Ultra', callback_data='86')
        note_20 = types.InlineKeyboardButton(text='Note 20', callback_data='87')
        markup.add(note_8, note_9, note_10, note_10_plus, note_20_ultra, note_20, back)
    if call.data == 'galaxy j':
        j4_2018 = types.InlineKeyboardButton(text='J4', callback_data='91')
        j4_plus_2018 = types.InlineKeyboardButton(text='J4 Plus', callback_data='92')
        j6_2018 = types.InlineKeyboardButton(text='J6', callback_data='93')
        j6_plus_2018 = types.InlineKeyboardButton(text='J6 Plus', callback_data='94')
        j8_2018 = types.InlineKeyboardButton(text='J8 (2018)', callback_data='95')
        j7_2017 = types.InlineKeyboardButton(text='J7 (2017)', callback_data='96')
        j5_2017 = types.InlineKeyboardButton(text='J5 (2017)', callback_data='97')
        j3_2017 = types.InlineKeyboardButton(text='J3 (2017)', callback_data='98')
        j7_2016 = types.InlineKeyboardButton(text='J7 (2016)', callback_data='99')
        j5_2016 = types.InlineKeyboardButton(text='J5 (2016)', callback_data='100')
        markup.add(j4_2018, j4_plus_2018, j6_2018, j6_plus_2018, j8_2018, j7_2017, j5_2017, j3_2017, j8_2018, j7_2016,
                   j5_2016, back)
    if call.data == 'galaxy m':
        m01 = types.InlineKeyboardButton(text='M01', callback_data='56')
        m01_core = types.InlineKeyboardButton(text='M01 core', callback_data='65')
        m10 = types.InlineKeyboardButton(text='M10', callback_data='57')
        m11 = types.InlineKeyboardButton(text='M11', callback_data='58')
        m20 = types.InlineKeyboardButton(text='M20', callback_data='59')
        m21 = types.InlineKeyboardButton(text='M21', callback_data='60')
        m30s = types.InlineKeyboardButton(text='M30s', callback_data='61')
        m31 = types.InlineKeyboardButton(text='M31', callback_data='62')
        m31s = types.InlineKeyboardButton(text='M31s', callback_data='63')
        m51 = types.InlineKeyboardButton(text='M51', callback_data='64')
        markup.add(m01, m01_core, m10, m11, m20, m21, m30s, m31, m31s, m51, back)
    bot.edit_message_media(media=types.InputMedia(type='photo', media=photo), chat_id=call.message.chat.id,
                           message_id=call.message.message_id, reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data.startswith('huawei '))
def phone_huawei(call):
    # photo = open(f'cartinios\\{call.data}.jpg', 'rb')
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton(text='⬅️Назад', callback_data='Устройство Huawei')
    if call.data == 'huawei honor':
        _6a = types.InlineKeyboardButton(text='6A', callback_data='huawei')
        _6cpro = types.InlineKeyboardButton(text='6c pro', callback_data='huawei nova')
        _7x = types.InlineKeyboardButton(text='7X', callback_data='huawei')
        _8pro = types.InlineKeyboardButton(text='8 pro', callback_data='huawei')
        _9 = types.InlineKeyboardButton(text='9', callback_data='huawei')
        _9lite = types.InlineKeyboardButton(text='9 Lite', callback_data='huawei')
        v9 = types.InlineKeyboardButton(text='V9', callback_data='huawei')
        v9play = types.InlineKeyboardButton(text='V9 Play', callback_data='huawei')
        _10 = types.InlineKeyboardButton(text='10', callback_data='huawei')
        _10lite = types.InlineKeyboardButton(text='10 Lite', callback_data='huawei')
        _7a = types.InlineKeyboardButton(text='7A', callback_data='huawei')
        _7c = types.InlineKeyboardButton(text='7C', callback_data='huawei')
        _7s = types.InlineKeyboardButton(text='Nova', callback_data='huawei')
        _8c = types.InlineKeyboardButton(text='7S', callback_data='huawei')
        _8x = types.InlineKeyboardButton(text='8X', callback_data='huawei')
        _9i = types.InlineKeyboardButton(text='9i', callback_data='huawei')
        _9n = types.InlineKeyboardButton(text='9n', callback_data='huawei')
        play = types.InlineKeyboardButton(text='play', callback_data='huawei')
        view20 = types.InlineKeyboardButton(text='View 20', callback_data='huawei')
        _10i = types.InlineKeyboardButton(text='10i', callback_data='huawei')
        _20 = types.InlineKeyboardButton(text='20', callback_data='huawei')
        _20lite = types.InlineKeyboardButton(text='20 lite', callback_data='huawei')
        _20s = types.InlineKeyboardButton(text='10s', callback_data='huawei')
        _8pro = types.InlineKeyboardButton(text='8 pro', callback_data='huawei')
        _8s = types.InlineKeyboardButton(text='8s', callback_data='huawei')
        _9x = types.InlineKeyboardButton(text='9x', callback_data='huawei')
        _9xpro = types.InlineKeyboardButton(text='9x pro', callback_data='huawei')
        _30 = types.InlineKeyboardButton(text='30', callback_data='huawei')
        _10xlite = types.InlineKeyboardButton(text='10x lite', callback_data='huawei')
        markup.add(_6a, _6cpro, _7x, _8pro, _9, _9lite, v9, v9play, _10, _10lite, _7a, _7c, _7s, _8c, _8x, _9i, _9n,
                   play, view20, _10i, _20, _20lite, _20s, _8pro, _8s, _9x, _9xpro, _30, _10xlite, back)

    elif call.data == 'nova':
        _2 = types.InlineKeyboardButton(text='2', callback_data='huawei')
        _2plus = types.InlineKeyboardButton(text='2 Plus', callback_data='huawei')
        _2s = types.InlineKeyboardButton(text='2s', callback_data='huawei')
        _3 = types.InlineKeyboardButton(text='3', callback_data='huawei')
        _3i = types.InlineKeyboardButton(text='3i', callback_data='huawei')
        _4 = types.InlineKeyboardButton(text='4', callback_data='huawei')
        _4e = types.InlineKeyboardButton(text='4e', callback_data='huawei')
        _5 = types.InlineKeyboardButton(text='5', callback_data='huawei')
        _5pro = types.InlineKeyboardButton(text='5 pro', callback_data='huawei')
        _5i = types.InlineKeyboardButton(text='5i', callback_data='huawei')
        _5ipro = types.InlineKeyboardButton(text='5i pro', callback_data='huawei')
        _5t = types.InlineKeyboardButton(text='5t', callback_data='huawei')
        _6 = types.InlineKeyboardButton(text='6', callback_data='huawei')
        markup.add(_2, _2plus, _2s, _3, _3i, _4, _4e, _5, _5pro, _5i, _5ipro, _5t, _6, back)

    elif call.data == 'hp':
        smart = types.InlineKeyboardButton(text='Smart', callback_data='huawei')
        _10 = types.InlineKeyboardButton(text='10', callback_data='huawei')
        _10lite = types.InlineKeyboardButton(text='10 Lite', callback_data='huawei')
        _10plus = types.InlineKeyboardButton(text='10 Plus', callback_data='huawei')
        _8lite2017 = types.InlineKeyboardButton(text='8 lite (2017)', callback_data='huawei')
        smart2019 = types.InlineKeyboardButton(text='Smart 2019', callback_data='huawei')
        _20 = types.InlineKeyboardButton(text='20', callback_data='huawei')
        _20lite = types.InlineKeyboardButton(text='20 lite', callback_data='huawei')
        _20pro = types.InlineKeyboardButton(text='20 pro', callback_data='huawei')
        smart_pro1019 = types.InlineKeyboardButton(text='Smart pro 2019', callback_data='huawei')
        smart_z = types.InlineKeyboardButton(text='Smart Z', callback_data='huawei')
        _30 = types.InlineKeyboardButton(text='30', callback_data='huawei')
        _30lite = types.InlineKeyboardButton(text='30 lite', callback_data='huawei')
        _30pro = types.InlineKeyboardButton(text='30 pro', callback_data='huawei')
        markup.add(smart, _10, _10lite, _10plus, _8lite2017, smart2019, _20, _20lite, _20pro, smart_pro1019, smart_z,
                   _30, _30lite, _30pro, back)

    elif call.data == 'hy':
        _5_17 = types.InlineKeyboardButton(text='5 (1017)', callback_data='huawei')
        _6_17 = types.InlineKeyboardButton(text='6 (2017)', callback_data='huawei')
        _7 = types.InlineKeyboardButton(text='7', callback_data='huawei')
        _7prime = types.InlineKeyboardButton(text='7 Prime', callback_data='huawei')
        max = types.InlineKeyboardButton(text='Max', callback_data='huawei')
        _3_18 = types.InlineKeyboardButton(text='3 (2018)', callback_data='huawei')
        _5lite_18 = types.InlineKeyboardButton(text='5 Lite (2018)', callback_data='huawei')
        _5prime_18 = types.InlineKeyboardButton(text='5 Prime (2018)', callback_data='huawei')
        _6_18 = types.InlineKeyboardButton(text='6 (2018)', callback_data='huawei')
        _7prime_18 = types.InlineKeyboardButton(text='7 Prime', callback_data='huawei')
        _9_18 = types.InlineKeyboardButton(text='9 (2018)', callback_data='huawei')
        _5_19 = types.InlineKeyboardButton(text='5 (1019)', callback_data='huawei')
        _6_19 = types.InlineKeyboardButton(text='6 (2019)', callback_data='huawei')
        _6pro_19 = types.InlineKeyboardButton(text='6 pro (2019)', callback_data='huawei')
        _7_19 = types.InlineKeyboardButton(text='7 (2019)', callback_data='huawei')
        _7pro_19 = types.InlineKeyboardButton(text='7 pro (2019)', callback_data='huawei')
        _7prime_19 = types.InlineKeyboardButton(text='7 Prime (2019)', callback_data='huawei')
        _9prime_19 = types.InlineKeyboardButton(text='9 Prime (2019)', callback_data='huawei')
        _9s = types.InlineKeyboardButton(text='9S', callback_data='huawei')
        markup.add(_5_17, _6_17, _7, _7prime, max, _3_18, _5lite_18, _5prime_18, _6_18, _7prime_18, _9_18, _5_19, _6_19,
                   _6pro_19, _7_19, _7prime_19, _9prime_19, _9s, back)

    elif call.data == 'enjoy':
        _8 = types.InlineKeyboardButton(text='8', callback_data='huawei')
        _9 = types.InlineKeyboardButton(text='9', callback_data='huawei')
        _10 = types.InlineKeyboardButton(text='10', callback_data='huawei')
        _10plus = types.InlineKeyboardButton(text='10 Plus', callback_data='huawei')
        _10s = types.InlineKeyboardButton(text='10s', callback_data='huawei')
        _9e = types.InlineKeyboardButton(text='9e', callback_data='huawei')
        _9s = types.InlineKeyboardButton(text='9s', callback_data='huawei')
        _20_5g = types.InlineKeyboardButton(text='20 5G', callback_data='huawei')
        _20plus = types.InlineKeyboardButton(text='20 Plus', callback_data='huawei')
        _20pro = types.InlineKeyboardButton(text='20 pro', callback_data='huawei')
        _20se = types.InlineKeyboardButton(text='dddddddddd', callback_data='huawei')
        z_5g = types.InlineKeyboardButton(text='20 SE', callback_data='huawei')
        markup.add(_8, _9, _10, _10plus, _10s, _9e, _20_5g, _20plus, _20pro, _20se, z_5g, back)
    bot.send_message(call.message.chat.id, 'трenkqehuq wnqcwhcfhupcn upwchuucquicgu', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('consultation'))
def anwer(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    if call.data == 'consultation_connector':
        item_next = types.InlineKeyboardButton(text='Дальше', callback_data='consultation_connector_next1')
        markup.add(item_next)
        bot.send_message(call.from_user.id,
                         'Проверять кабель или блок на наличие внешних повреждений не имеет смысла так как он может выйти из строя будучи внешне в идеальном состоянии \
                         \nПопробуйте другой *заведомо исправный кабель* который заряжает другой телефон без проблем и перебоев',
                         parse_mode='markdown', reply_markup=markup)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='*Проблемы с зарядкой могут быть сязаны с:*\n*а:* Неисправен кабель \n*б:* Неисправен блочёк\n*в: *Забился, загрязнился разъем в телефоне\n*г: *Cломался / расшатался разъем',
                              parse_mode='markdown')
    elif call.data == 'consultation_connector_next1':
        photo = open('cartinios/cleaning.jpg', 'rb')
        item_next = types.InlineKeyboardButton(text='Дальше', callback_data='consultation_connector_next2')
        markup.add(item_next)

        bot.send_photo(call.from_user.id, photo,
                         'Если разъем засорился (это не всегда видно невооруженным глазом) не рекомендуется выполнять чистку *самостоятельно!*\
                          \nВнутри находятся тонкие контакты которые легко повредить.\nСтоимость внешней чистки разъема не учитывается при любом из видов ремонта. \
                          \nВ нашем сервисном центре данная процедура выполняется с использованием изопропилового спирта (не оставляющий остатков), пинцета, щетки и умеренного воздушного давления. \
                          \nПосле чистки разъем будет выглядить внутри как новый но даже это не обязывает его исправно работать, ведь если разрушена пайка со внутренней стороны, без замены не обойтись(',
                         parse_mode='markdown', reply_markup=markup)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Проверять кабель или блок на наличие внешних повреждений не имеет смысла так как он может выйти из строя будучи внешне в идеально состоянии \
                              \nПопробуйте другой <b><u>заведомо исправный кабель</u></b> который заряжает другой телефон без проблем и перебоев',
                              parse_mode='html')
    elif call.data == 'consultation_connector_next2':
        photo = open('cartinios/cleaning.jpg', 'rb')

        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_photo(call.from_user.id, photo,
                       'Если разъем засорился (это не всегда видно невооруженным глазом) не рекомендуется выполнять чистку *самостоятельно!*\
                        \nВнутри находятся тонкие контакты которые легко повредить.\nСтоимость внешней чистки разъема не учитывается при любом из видов ремонта. \
                        \nВ нашем сервисном центре данная процедура выполняется с использованием изопропилового спирта (не оставляющий остатков), пинцета, щетки и умеренного воздушного давления. \
                        \nПосле чистки разъем будет выглядить внутри как новый но даже это не обязывает его исправно работать, ведь если разрушена пайка со внутренней стороны, без замены не обойтись(',
                       parse_mode='markdown')
        bot.send_message(call.from_user.id,
                         'Если же чистка не помогла, нужно менять разъем. Для замены в нашем сц напишите боту «ремонт» и он предложить вам создать заявку на ремонт\n\n/start')

    elif call.data == 'consultation_voter':
        item_next = types.InlineKeyboardButton(text='Дальше', callback_data='consultation_voter_next1')
        markup.add(item_next)

        bot.send_message(call.from_user.id,'Постарайтесь выключить телефон, если не реагирует на касания можно попробовать это сделать принудительным зажатием комбинации клавиш. \nКак насильно выключить Android-смартфон с несъемным аккумулятором:\n 1. Зажмите кнопку питания и удерживайте до отключения аппарата\n 2. Зажмите кнопку питания и клавишу увеличения громкости до отключения\n 3. Зажмите кнопку питания и обе клавиши громкости (только для раздельных кнопок!), удерживая их 10 секунд до выключения или дольше', reply_markup=markup)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Если в ваш телефон попала влага, нужно его  немедленно разобрать и промыть плату специальной жидкостью не оставляющей никаких остатков. При этом не повредить подсветку дисплея, микрофоны и камеры. Вообщем чистку могут выполнить только в сервисном центре.')
    elif call.data == 'consultation_voter_next1':
        markup = types.InlineKeyboardMarkup()
        item_next = types.InlineKeyboardButton(text='Дальше', callback_data='consultation_voter_next2')
        markup.add(item_next)
        bot.send_message(call.from_user.id,
                         'Не фен, не батарея вам не поможет, максимум сухие салфетки или рис. Влагу нужно не просто убрать с устройства, а и очистить все высохшие остатки от нее так как они могут замыкать элементы и смартфон выйдет из строя спустя время',
                         reply_markup=markup)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Постарайтесь выключить телефон, если не реагирует на касания можно попробовать это сделать принудительным зажатием комбинации клавиш. \nКак насильно выключить Android-смартфон с несъемным аккумулятором:\n 1. Зажмите кнопку питания и удерживайте до отключения аппарата\n 2. Зажмите кнопку питания и клавишу увеличения громкости до отключения\n 3. Зажмите кнопку питания и обе клавиши громкости (только для раздельных кнопок!), удерживая их 10 секунд до выключения или дольше',
                              parse_mode='html')
    elif call.data == 'consultation_voter_next2':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        sloman = types.KeyboardButton('У меня сломался телефон')
        markup.add(sloman)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Не фен, не батарея вам не поможет, максимум сухие салфетки. Влагу нужно не просто убрать с устройства, а и очистить все высохшие остатки от нее так как они могут замыкать элементы и смартфон выйдет из строя спустя время')
        bot.send_message(call.from_user.id, 'Обратитесь в ближайший сервисный центр для выполнения чистки смартфона. Узнать где ближайший можно в справочнике 2Gis. К нам ехать займет время, а влагу нужно устранить максимально быстро\n\n/start')

    elif call.data == 'consultation_buggy':
        item_next = types.InlineKeyboardButton(text='Дальше', callback_data='consultation_buggy_next1')
        markup.add(item_next)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Что делать, если телефон зависает?\n[ПРИЧИНЫ ЗАВИСАНИЯ ТЕХНИКИ](https://teletype.in/@andrei_iph/P_-KoDBU2Sr)', parse_mode='markdown')
        bot.send_message(call.message.chat.id, 'Для того чтобы оставить заявку на замену програмного обеспечения вашего устройства, напишите боту "ремонт" и укажите модель вашего телефона\n\n/start')

    elif call.data == 'consultation_broken_option1':
        item_next = types.InlineKeyboardButton(text='Дальше', callback_data='consultation_buggy_next1')
        markup.add(item_next)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Если так случилось, что экран вашего смрфона пострадал - не унывайте, мы поможем вам это исправить в кратчайшие сроки')
        bot.send_message(call.message.chat.id, 'В случает когда телефон в трещинах а картинка осталась без деффектов - смартфон можно восстановить тем самым сэкономив больше половины средств потраченных на замену модуля.\
                                               Подробнее о сепарации модуля вы можете уточнить у менеджера')
    elif call.data == 'consultation_broken_option2':
        bot.send_message(call.message.chat.id, 'Когда после подения, даже небольшего, у вас полностью погас экран это значит либо отщелкнулся шлейф дисплея внутри от платы, либо микротрещина на самой матрице\
                                                дисплея.\nДеталнее информацию можно уточнить у нашего менеджера')

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Если так случилось что экран вашего смрфона пострадал - не унывайте, мы поможем вам это исправить в кратчайшие сроки')
    elif call.data == 'consultation_broken_option3':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Если так случилось что экран вашего смрфона пострадал - не унывайте, мы поможем вам это исправить в кратчайшие сроки')
        bot.send_message(call.message.chat.id, 'В таком случае вам следует оставить заявку на ремонт написав боту "ремонт"\n Но если вы не планируете чинить свое устройстсво, а вам нужна информация с него доступа к которой вы лишены\
                                               пишите нашему менеджеру, скорей всего мы сможем скачать с него всю вам необходимую информацю')

    elif call.data == 'consultation_sound':
        item_next = types.InlineKeyboardButton(text='Дальше', callback_data='consultation_sound_next1')
        markup.add(item_next)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='    Прохо слышите собеседника?\nИли вас не слышит собеседник?\n   Важно правильно ответить на этот вопрос так как в первом случае неисправен спикер(разговорный динамик) во втором микрофон.\n\
    В современном смарфоне встроено порядка 3-4х микрофонов и несколько динамиков как правило один снизу и один,  возможно двухконтурный, сверху если у вас стерео звук на телефоне.\n\
    Сам динамик очень редко выходит из строя, физически навредить ему можно либо проткнув мембрану иголкой либо мелкая металическая стружка. В противном случае достаточно правильно прочистить защитную решетку.')
        bot.send_message(call.message.chat.id, 'Чистка производиться щеткой нужной мягкости, изопропилового спирта (не оставлыет остатков) и сжатого воздуха.\n\
    При любом ремонте или установки защитного стекла мы выполняем такую чистку бонусом\n   Случаеться такое, что все таки присутствует неисправность и без разбора не обойтись(', reply_markup=markup)
    elif call.data == 'consultation_sound_next1':
        item_next = types.InlineKeyboardButton(text='Дальше', callback_data='consultation_sound_next1')
        markup.add(item_next)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='    Чистка производиться щеткой нужной мягкости, изопропилового спирта (не оставлыет остатков) и сжатого воздуха.\n\
    При любом ремонте или установки защитного стекла мы выполняем такую чистку бонусом\n   Случаеться такое, что все таки присутствует неисправность и без разбора не обойтись(')
        bot.send_message(call.message.chat.id, '    Технически проблема может быть в: \n-непосредственно динамике/микрофоне\n-системной плате\n-межплатном шлейфе\n-контроллере питания\n-ауидиокодэке\n\
    В зависимости от загрузки, инженер в течении дня, сможет понять в чем именно проблема и уточниить цену устранения дефекта.\n   В iphone 7/7plus часто сплывает проблема \
аудиокодэка (не работает громкая связь во время вызова, не записываються голосовые сообщения, не активен диктофон)\n   Для того чтобы выполнить ремонт в нашем сервисном центре напишите слово "ремонт" боту, \
затем напишите модель телефона и кратко опишите проблему')

    else:
        bot.send_message(call.from_user.id,
                         'Код else. Что-то не так')
@bot.callback_query_handler(func=lambda call: True)
def func_order(call):
    check = user_dict2[call.message.chat.id]

    user = user_dict[call.message.chat.id]
    model_nubmer = [str(i) for i in range(sheet.max_row)]  # Проходим по максимальному количеству строк
    problem_letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']
    A = 'A'
    if call.data in model_nubmer:  # Прилетает номер модели
        photo = open(f'cartinios/{call.data}.jpg', 'rb')
        user.model = call.data
        user.money = 0  # обнуляем баланс
        model = sheet[A + user.model].value  # = Название модели телефона
        markup = types.InlineKeyboardMarkup(row_width=1)
        broken = types.InlineKeyboardButton(text=sheet['B1'].value + str(sheet['B' + user.model].value) + ' грн',
                                            callback_data='B')
        connector = types.InlineKeyboardButton(text=sheet['C1'].value + str(sheet['C' + user.model].value) + ' грн',
                                               callback_data='C')
        sound = types.InlineKeyboardButton(text=sheet['E1'].value + str(sheet['E' + user.model].value) + ' грн',
                                           callback_data='E')
        battery = types.InlineKeyboardButton(text=sheet['D1'].value + str(sheet['D' + user.model].value) + ' грн',
                                             callback_data='D')
        back = types.InlineKeyboardButton(text='⬅️Назад', callback_data=user.phone)
        other = types.InlineKeyboardButton(text='Другое \ Оставить на диагностику 🔍', callback_data='H')
        markup.add(broken, connector, sound, battery, other, back)
        bot.edit_message_media(media=types.InputMedia(type='photo', media=photo), chat_id=call.message.chat.id,
                               message_id=call.message.message_id, reply_markup=markup)

        # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id + 1, text=f'{user.phone} {model}')
    elif call.data in problem_letter:  # Прилетает буква проблемы
        photo = open(f'cartinios/{call.data}.jpg', 'rb')
        user.problem = call.data
        model = sheet[A + user.model].value  # = Название модели телефона
        price = sheet[user.problem + user.model].value
        user.money += price  # пополнение кошелька
        problem = sheet[user.problem + '1'].value  # = Название ремонта
        markup = types.InlineKeyboardMarkup(row_width=1)
        confirm = types.InlineKeyboardButton(text='Далее', callback_data='confirm')
        back = types.InlineKeyboardButton(text='⬅️Назад', callback_data=user.model)
        # if user.problem != 'D':  # отображаем дополнительную кнопку замена аккумулятора
        #     battery = types.InlineKeyboardButton(
        #         text=str(sheet['D1'].value) + str(sheet['D' + user.model].value) + ' грн',
        #         callback_data='confirm_battery')
        #    markup.add(battery)
        markup.add(confirm, back)
        bot.edit_message_media(media=types.InputMedia(type='photo', media=photo), chat_id=call.message.chat.id,
                               message_id=call.message.message_id, reply_markup=markup)
    elif call.data.startswith('confirm'):
        photo = open('cartinios/confirm.jpg', 'rb')
        battery = sheet['D1'].value
        problem = sheet[user.problem + '1'].value
        price = sheet[user.problem + user.model].value
        model = sheet[A + user.model].value
        price_battery = sheet['D' + user.model].value
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup = types.InlineKeyboardMarkup(row_width=1)
        back = types.InlineKeyboardButton(text='⬅️Назад', callback_data=user.model)
        contact = types.KeyboardButton('Отправить свой контакт / подтвердить заказ', request_contact=True)
        markup.add(back)
        markup1.add(contact)
        bot.edit_message_media(media=types.InputMedia(type='photo', media=photo), chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
        bot.send_message(call.message.chat.id,
                                   f'{user.phone} {model}\n{problem} {price} грн\n\nИтого: {user.money} грн\n\nДля подтверждения заявки, пожалуйста, поделитесь совим номером телефонас помощью кнопки отправки контакта',
                                   reply_markup=markup1)
        # msg = bot.send_message(call.message.chat.id, 'Для подтверждения заявки, пожалуйста, поделитесь совим номером телефона', reply_markup=markup1)
    elif call.data == 'write':
        bot.edit_message_text('Мы поличили ваш заказ❕\nМы вам напишем📝\n\n/start', chat_id=call.message.chat.id, message_id=call.message.id)
        bot.send_message(manager, 'Написать в телеграм')
        bot.send_message(manager, '-------------------------------------------------------------------')
    elif call.data == 'call':
        bot.edit_message_text('Мы поличили вашг заказ❕\nМы вам позвоним📞\n\n/start', chat_id=call.message.chat.id, message_id=call.message.id)
        bot.send_message(manager, 'Позвонить')
        bot.send_message(manager, '-------------------------------------------------------------------')
    elif call.data == 'no':
        check.model = None #стираем модель введеную пользователем
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, call.message.message_id-1)
    elif call.data == 'yes':
        bot.edit_message_text(f'Ваш телефон "{check.model}"?', chat_id=call.message.chat.id, message_id=call.message.id)
        bot.send_message(call.message.chat.id, f'Пожалуйста коротко опишите проблему с вашим устройством {check.model} одним сообщением')

@bot.message_handler(content_types=['contact'])
def order_conact(message):
    check = user_dict2[message.chat.id]  # открыл словарь проверки
    user = user_dict[message.chat.id]

    markup = types.InlineKeyboardMarkup(row_width=2)   #клавитаура с выбором удобной связи
    ccall = types.InlineKeyboardButton(text='Позвонить📞', callback_data='call')
    write = types.InlineKeyboardButton(text='Написать в telegram📝', callback_data='write')
    markup.add(ccall, write)

    name = message.from_user.first_name
    contact = message.contact.phone_number
    contact_name = message.contact.first_name
   # try:
    if check.order == True:  # Если человк вручную писал
       # bot.forward_message(to_chat_id, from_chat_id, message_id)
        bot.forward_message(manager, message.chat.id, message_id=message.id)
        bot.send_message(message.chat.id, 'Мы поличили ва заказ❕', reply_markup=markup)
        bot.send_message(manager, f' Новая заявка от {name}\n{contact_name}   {contact}  Устройство: {check.model} 📱 \n\n🛠 {check.problem}')


    elif user_dict[message.chat.id] != 'phone':
        problem = sheet[user.problem + '1'].value
        model = sheet['A' + user.model].value
        price = sheet[user.problem + user.model].value
        order = f'{user.phone} {model}:\n➕ {problem} {price} грн\n\nИтого: {user.money} грн'

        bot.edit_message_text(f'Устройство: {user.model} 📱 \n\n🛠 {user.problem}\nДля того чтобы отправить запрос менеджеру, поделитесь номером телефона нажав кнопкку "Подтвердить". Или отправте контакт',chat_id=message.chat.id,
                              message_id=message.id-1)
        bot.send_message(message.chat.id,   f'Ваш заказ сформирован. Мы свяжемся с вами в ближайшее время. Спасибо!\n\n{order}', reply_markup=markup)

        bot.send_message(manager, f'Новый заказ от {contact_name}\nНомер телефона: {contact}\n\n{order}')

bot.polling(none_stop=True)
