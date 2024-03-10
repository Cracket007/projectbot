from imports import *
def register_comand_handlers(bot):
    @bot.message_handler(commands=['help'])
    def help(message):
        bot.send_message(message.chat.id, "/help - виводить список команд із поясненнями\n/chat_manager введіть цю команду, щоб написати менеджеру безпосередньо (на відповідь може знадобитися час)"
                                          "\n/status_order(у розробці) якщо вже залишили пристрій на ремонт і хочете дізнатися про статус ремонту. Буває 5 етапів: -новий; -чекає запчастини; -в роботі; -готовий; -відмова"
                                          "\n/give_feedback залишити відгук/враження якщо користувалися нашими послугами. Відкликання через бота ніде публікуватися не буде, його побачать лише керівники проекту."
                                          "\n\nДля того щоб отримати консультацію можна або скористатися відповідями на найпопулярніші запитання, написавши боту текст «Отримати консультацію» або відправити команду /chat_manager для зв'язку з вільним менеджером у робочий час."
                                          "\nЩоб залишити заявку на ремонт, напишіть «ремонт» і оберіть в меню модель вашого телефону потім вид ремонту. Якщо меню немає моделі вашого телефону - просто напишіть боту назву моделі потім уточніть несправнiсть і створіть заявку, менеджер"
                                          " зв'яжеться з вами для уточнень деталей. Для надсилання заявки потрібно поділитись контактом для зв'язку. Можна або поділитися своїм контактом, натиснувши на відповідну кнопку на клавіатурі або прикріпити контакт з телефонної книги та надіслати боту.")
    @bot.message_handler(commands=['chat_manager'])
    def chat_manager(message):
        bot.send_message(message.chat.id, "Напишiть менеджеру безпосередньо @GeniusMob55 (на відповідь може знадобитися час). \n\nРобочi години:\nПн-Пт з 10:00 до 18:00\nСб-Нд з 10:00 до 16:00")

    @bot.message_handler(commands=['status_order'])
    def status_order(message):
        bot.send_message(message.chat.id, "(у розробці) якщо вже залишили пристрій на ремонт і хочете дізнатися про статус ремонту. Буває 5 етапів: -новий; -чекає запчастини; -в роботі; -готовий; -відмова")

    @bot.message_handler(commands=['give_feedback'])
    def give_feedback(message):
        bot.send_message(message.chat.id, "Залишити відгук/враження якщо користувалися нашими послугами. Відкликання через бота ніде публікуватися не буде, його побачать лише керівники проекту.\n\n    Залиште фiтбек у вiдповiдь на це повiдомлення")

    @bot.message_handler(commands=['start'])
    def start(message):
        user_dict[message.chat.id] = User(message.text)  # создал словарь проверки
        check = user_dict[message.chat.id]  # открыл словарь проверки
        check.castom = False
        check.model = None
        check.check = False

        murkup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        consultation = types.KeyboardButton('Отримати консультацiю')
        broken = types.KeyboardButton('Ремонт')
        murkup.add(consultation, broken)
        privet = '<b>Я бот сервісного центру з ремонту смартфонів у Одесі!</b>\n\n<b>За моєю допомогою можна:</b>\n\n-Отримати консультацію та дізнатися вартість ремонту пристрою\n-Оформити заявку на ремонт\n\nДля консультації з менеджером залиште заявку на ремонт'
        bot.send_message(message.chat.id, privet, reply_markup=murkup, parse_mode='html')

