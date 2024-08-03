import telebot # pip install pyTelegramBotAPI
from MukeshAPI import api # pip install MukeshAPI
from g4f.client import Client # pip install g4f, pip install curl_cffi
from g4f.Provider import Liaobots # pip install g4f, pip install curl_cffi

token = input(f'Введи свой токен: ')
bot = telebot.TeleBot(token)

def ai_request(message: telebot.types.Message, type_of_neyro: int):
    if type_of_neyro == 1:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, Client().chat.completions.create([{'role':'user', 'content':message.text}], 'gpt-3.5-turbo', Liaobots), reply_markup=telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton('Завершить чат', callback_data='cancel')))
        bot.register_next_step_handler(message, ai_request, 1)
    if type_of_neyro == 2:
        bot.send_chat_action(message.chat.id, 'upload_photo')
        bot.send_photo(message.chat.id, api.ai_image(message.text), f'Изображение по Вашему запросу. Если Вы не получили, что Вам надо, измените формуляровку, или язык, на котором был написан запрос.')
    

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Привет! Для взаимодействия с ИИ воспользуйся INLINE-кнопками ниже.\n\n\nMade by FlorestDev. (@florestchannel)', reply_markup=telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton('ChatGPT', callback_data='chatgpt-request'), telebot.types.InlineKeyboardButton('Нарисовать картинку', callback_data='mukeshapi-request')))

@bot.callback_query_handler(lambda query: True)
def query(query: telebot.types.CallbackQuery):
    if query.data == 'chatgpt-request':
        bot.edit_message_text('Напиши любое сообщение ChatGPT.', query.message.chat.id, query.message.id, None, None, None, None, None)
        bot.register_next_step_handler(query.message, ai_request, 1)
    if query.data == 'cancel':
        bot.clear_step_handler_by_chat_id(query.message.chat.id)
        bot.send_message(query.message.chat.id, f'Чат с нейросетью был завершен. Чтобы вновь взаимодействовать с ИИ напишите команду `/start`.', parse_mode='Markdown')
    if query.data == 'mukeshapi-request':
        bot.edit_message_text('Напиши запрос, по которому нейросеть будет генирировать текст.', query.message.chat.id, query.message.id)
        bot.register_next_step_handler(query.message, ai_request, 2)

bot.infinity_polling()