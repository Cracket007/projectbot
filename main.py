from imports import *

register_comand_handlers(bot)
# register_callback_handler(bot)
register_message_handlers(bot)



bot.polling(none_stop=True)
