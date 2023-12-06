import telebot
from telebot import types

# Передаем в переменную bot апи из BotFather
bot = telebot.TeleBot('YOUR_BOT_TOKEN')  # Замените "YOUR_BOT_TOKEN" на токен вашего бота

# Словарь для хранения состояний пользователей
user_states = {}

# Обработчик команды /start и создание клавиатуры
@bot.message_handler(commands=['start'])
def start(message):
    # Инлайн-клавиатура
    inline_keyboard = types.InlineKeyboardMarkup(row_width=2)
    item_price = types.InlineKeyboardButton('Price', callback_data='price')
    item_products = types.InlineKeyboardButton('Products', callback_data='products')
    inline_keyboard.add(item_price, item_products)

    # Неинлайн (Reply) клавиатура
    reply_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    reply_price = types.KeyboardButton('Price')
    reply_products = types.KeyboardButton('Products')
    reply_keyboard.add(reply_price, reply_products)

    user_states[message.chat.id] = {'state': 'start'}  # Начальное состояние
    bot.send_message(message.chat.id, 'Привет! Я бот. Выберите одну из команд:', reply_markup=inline_keyboard)
    bot.send_message(message.chat.id, 'Или используйте неинлайн клавиатуру:', reply_markup=reply_keyboard)

# Обработчик команды /price
@bot.message_handler(func=lambda message: message.text.lower() == 'price')
def price_command(message):
    bot.send_message(message.chat.id, 'Введите число:')
    user_states[message.chat.id]['state'] = 'waiting_for_price'  # Устанавливаем состояние "waiting_for_price"
    # Устанавливаем команду "назад" в неинлайн клавиатуре
    reply_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    reply_back = types.KeyboardButton('Назад')
    reply_keyboard.add(reply_back)
    bot.send_message(message.chat.id, 'Используйте неинлайн клавиатуру:', reply_markup=reply_keyboard)

# Обработчик ввода числа
@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'waiting_for_price')
def handle_price_input(message):
    if message.text.lower() == 'назад':
        user_states[message.chat.id]['state'] = 'start'  # Возвращаемся на начальное состояние
        start(message)
    else:
        try:
            number = float(message.text)
            result = number * 13 + 500
            # Отправляем сообщение с результатом и кнопкой "назад"
            back_button = types.InlineKeyboardButton('Назад', callback_data='back')
            keyboard = types.InlineKeyboardMarkup().add(back_button)
            bot.send_message(message.chat.id, f"Результат: {result}", reply_markup=keyboard)
        except ValueError:
            bot.send_message(message.chat.id, "Введите корректное число.")
            # Заново вызываем обработчик ввода числа для текущей команды
            bot.register_next_step_handler(message, handle_price_input)

# Обработчик команды /products
@bot.message_handler(func=lambda message: message.text.lower() == 'products')
def products_command(message):
    # Инлайн-клавиатура
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    item_product1 = types.InlineKeyboardButton('Product 1', callback_data='product1')
    item_product2 = types.InlineKeyboardButton('Product 2', callback_data='product2')
    item_product3 = types.InlineKeyboardButton('Product 3', callback_data='product3')
    keyboard.add(item_product1, item_product2, item_product3)

    # Неинлайн (Reply) клавиатура
    reply_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    reply_back = types.KeyboardButton('Назад')
    reply_keyboard.add(reply_back)

    user_states[message.chat.id]['state'] = 'waiting_for_products'  # Устанавливаем состояние "waiting_for_products"
    bot.send_message(message.chat.id, 'Выберите продукт:', reply_markup=keyboard)
    bot.send_message(message.chat.id, 'Или используйте неинлайн клавиатуру:', reply_markup=reply_keyboard)

# Обработчка нажатия на кнопку "назад"
@bot.callback_query_handler(func=lambda call: call.data == 'back')
def back_button_handler(call):
    # Вызываем обработчик команды /start
    start(call.message)

# Запуск бота
if __name__ == '__main__':
    bot.polling()
