from telebot import types
from imports import *
def register_message_handlers(bot):
    @bot.message_handler(content_types=['text'])
    def text(message):
        try:
            check = user_dict[message.chat.id]
            if message.text.lower() == 'ремонт':
                user_dict[message.chat.id] = User(check)
                check.model = None
                check.problem = None
                check.castom = True

                photo = open('cartinios/repair.jpg', 'rb')
                markup = types.InlineKeyboardMarkup(row_width=1)
                samsung = types.InlineKeyboardButton(text='Samsung', callback_data='Пристрiй Samsung')
                apple = types.InlineKeyboardButton(text='Apple', callback_data='Пристрiй Apple')
                huawei = types.InlineKeyboardButton(text='Huawei', callback_data='Пристрiй Huawei')
                xiaomi_redmi = types.InlineKeyboardButton(text='Xiaomi Redmi', callback_data='Пристрiй Xiaomi')
                oppo_realme = types.InlineKeyboardButton(text='Oppo Realme', callback_data='Пристрiй Oppo')
                markup.add(samsung, huawei, xiaomi_redmi, oppo_realme, apple)
                bot.send_photo(message.chat.id, photo, reply_markup=markup)

            elif message.text.lower() == 'отримати консультацiю':
                markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                connector = types.InlineKeyboardButton('Не заряджається')
                voda = types.InlineKeyboardButton('Впав у воду')
                gluk = types.KeyboardButton('Глючить, зависає')
                razbit = types.KeyboardButton('Розбитий дисплей, тріщини')
                zvyk = types.KeyboardButton('Проблеми зі звуком')
                razryazh = types.KeyboardButton('Швидко розряджається')
                drugoe = types.KeyboardButton('Інше')
                broken = types.KeyboardButton('Ремонт')
                markup.add(connector, voda, gluk, razbit, zvyk, razryazh, drugoe, broken)
                problem = f'Проблема, яку ви спостерігаєте?'

                bot.send_message(message.chat.id, problem, reply_markup=markup)
            elif message.text.lower() == 'не заряджається':
                markup = types.InlineKeyboardMarkup(row_width=2)
                item_next = types.InlineKeyboardButton(text='Далі', callback_data='consultation_connector')
                markup.add(item_next)
                bot.send_message(message.chat.id,
                                 "Проблеми з зарядкою можуть бути повя'зані з:\nа: Несправний кабель \nб: Несправний блок живлення\nв: Забився, забруднився роз'єм в телефоні\nг: Сломався / розійшовся роз'єм",
                                 parse_mode='markdown', reply_markup=markup)
            elif message.text.lower() == 'впав у воду':
                markup = types.InlineKeyboardMarkup()
                item_next = types.InlineKeyboardButton(text='Далі', callback_data='consultation_voter')
                markup.add(item_next)
                bot.send_message(message.chat.id,
                                 'Якщо до вашого телефону потрапила волога, його необхідно негайно розібрати та промити плату спеціальною рідиною, яка не залишає жодних залишків. При цьому не пошкодити підсвічування дисплея, мікрофони та камеру. Взагалі чистку можуть виконати тільки в сервісному центрі.',
                                 reply_markup=markup)
            elif message.text.lower() == 'глючить, зависає':
                markup = types.InlineKeyboardMarkup()
                item_next = types.InlineKeyboardButton(text='Далі', callback_data='consultation_buggy')
                markup.add(item_next)

                bot.send_message(message.chat.id,
                                 'Що робити, якщо телефон зависає?\n[ПРИЧИНИ ЗАВИСАННЯ ТЕХНІКИ](https://teletype.in/@andrei_iph/P_-KoDBU2Sr)',
                                 parse_mode='markdown', reply_markup=markup)
            elif message.text.lower() == 'розбитий дисплей, тріщини':
                markup = types.InlineKeyboardMarkup(row_width=1)
                option1 = types.InlineKeyboardButton(text='Є тріщини, але користуватися можна',
                                                     callback_data='consultation_broken_option1')
                option2 = types.InlineKeyboardButton(text='Немає тріщин, але чорний екран',
                                                     callback_data='consultation_broken_option2')
                option3 = types.InlineKeyboardButton(text='Розбитий повністю, користуватися неможливо',
                                                     callback_data='consultation_broken_option3')
                markup.add(option1, option2, option3)

                bot.send_message(message.chat.id,
                                 " Якщо сталося так, що екран вашого смартфона постраждав, не засмучуйтесь, ми допоможемо вам виправити це якнайшвидше.\n   Але спочатку потрібно зрозуміти, наскільки сильні пошкодження зазнав гаджет.",
                                 reply_markup=markup)
            elif message.text.lower() == 'проблеми зі звуком':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item_next = types.InlineKeyboardButton(text='Далi', callback_data='consultation_sound')
                markup.add(item_next)

                bot.send_message(message.chat.id,
                                 " Не чуєте розмовника? Або розмовник вас не чує?\n    Це важливо, щоб правильно відповісти на це запитання, оскільки в першому випадку несправній динамік (розмовний динамік), а в другому - мікрофон.\n  У сучасному смартфоні вбудовано близько 3-4 мікрофонів та кілька динаміків, зазвичай один знизу та один, можливо, двоконтурний, зверху, якщо у вас стереозвук на телефоні."
                                 "\n   Сам динамік дуже рідко виходить з ладу, фізично завдати йому шкоди можна лише зiпсувавши мембрану голкою або дрібною металевою стружкою. В іншому випадку достатньо правильно прочистити захисну решітку.",
                                 reply_markup=markup)
            elif message.text.lower() == 'швидко розряджається':
                bot.send_message(message.chat.id,
                                 "Якщо ваш телефон швидко розряджається, спробуйте наступні кроки:\n   1. Перевірте налаштування батареї і додатків - вимкніть фонові програми, gps та bluetooth якщо ними не користуетесь."
                                 "\n  2. Оновіть програмне забезпечення телефону - в нових версіях можуть бути виправлені помилки, що впливають на роботу батареї."
                                 "\n  3. Якщо ваш телефон вже деякий час використовується (більше 2х років), батарея може бути вже зношеною і потребувати заміни. Також зніміть чохол та детально оглянте зазори між корпусом та дисплеєм та задньою кришко, бувае аккумулятор збільшується у розмірах, в такому випадку його не варто заряджаті, а треба замінити акумулятор."
                                 "\n  4. Напишіть нам - для подальшої діагностики та ремонту @GeniusMob55")
            elif message.text.lower() == 'інше':
                bot.send_message(message.chat.id, 'Напишiть нашому iнженеру @andrei_iph')

            elif check.check == True:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                back = types.KeyboardButton('Ремонт')
                contact = types.KeyboardButton('🖊️Подтвердить заказ', request_contact=True)
                markup.add(back, contact)

                check.problem = message.text  # записали проблему
                check.order = True
                bot.delete_message(message.chat.id, message.message_id - 1)
                bot.send_message(message.chat.id,
                                 f'Устройство: {check.model} 📱 \n\n🛠 {check.problem}\n\n   Пришлите сообщение еще раз если хотите изменить описание проблемы\n\n    Для того чтобы отправить запрос менеджеру, поделитесь номером телефона нажав кнопкку "Подтвердить". Или отправте контакт',
                                 reply_markup=markup)

            elif message.text != None:  # если человек вводит модель вручную в разделе "Ремонт"
                check.model = message.text
                markup = types.InlineKeyboardMarkup()  # клавиатура да нет
                yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
                no = types.InlineKeyboardButton(text='Нет', callback_data='no')
                markup.add(yes, no)
                bot.send_message(message.chat.id, f'Ваш телефон "{check.model}"?', reply_markup=markup)
        except:
            bot.send_message(message.chat.id, "Почнiть с команди /start")