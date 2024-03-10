from imports import *

def register_contact_handler(bot):
    @bot.message_handler(content_types=['contact'])
    def order_conact(message):
        try:
            check = user_dict[message.chat.id]  # открыл словарь проверки
            user = user_dict[message.chat.id]
            name = message.from_user.first_name
            contact = message.contact.phone_number
            contact_name = message.contact.first_name
            if check.check == True:  # Если человк вручную писал
                bot.forward_message(manager, message.chat.id, message_id=message.id)
                bot.send_message(message.chat.id, 'Мы поличили ва заказ❕')
                bot.send_message(manager, f' Новая заявка от {name}\n{contact_name}   {contact}  Устройство: {check.model} 📱 \n\n🛠 {check.problem}')

                order = f'{user.model}:\n🛠 {check.problem} грн\n\nИтого: {user.money} грн'
                bot.send_message(message.chat.id, f"Ваше замовлення сформоване. Ми зв'яжемося з вами найближчим часом. Дякую!\n\n{order}",  reply_markup=types.ReplyKeyboardRemove())

            elif check.check == False:
                problem = sheet[user.problem + '1'].value
                model = sheet['A' + user.model].value
                price = sheet[user.problem + user.model].value
                order = f'{user.phone} {model}:\n➕ {problem} {price} грн\n\nИтого: {user.money} грн'
                bot.send_message(message.chat.id,   f"Ваше замовлення сформоване. Ми зв'яжемося з вами найближчим часом. Дякую!\n\n{order}", reply_markup=types.ReplyKeyboardRemove())

                bot.send_message(manager, f'Новый заказ от {contact_name}\nНомер телефона: {contact}\n\n{order}')
        except TypeError:
            bot.send_message(message.chat.id, 'Спочатку оформiть заявку:\n - Натистiть, або напишiть "Ремонт" боту\n - Просто вiдправте модель свого смартфону боту потiм опишiть проблему')
            bot.send_message(group, f'{name}\n{contact}')
        except:
            bot.send_message(message.chat.id, "Почнiть с команди /start")