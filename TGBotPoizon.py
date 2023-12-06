# 6790503114:AAE-2iL81qiap095r1csAObmZZ0mD9d2P0Q
import telebot
from telebot import types

# Передаем в переменную bot апи из BotFather
bot = telebot.TeleBot('6790503114:AAE-2iL81qiap095r1csAObmZZ0mD9d2P0Q')  # Замените "YOUR_BOT_TOKEN" на токен вашего бота

# Словарь для хранения описаний продуктов
product_descriptions = {
    'product1': 'С помощью этого мануала ты научишься самостоятельно пополянть китайский кошелек Alipay без '
                'каких-либо посредников и по самому выгодному курсу. В подарок ты получишь гайд как создать свой '
                'обменник и зарабатывать на этом',
    'product2': 'С помощью данного мануала ты научишься полностью самостоятельно выкупать вещи из Китая без '
                'посрдеников. В подарок ты получишь несколько проверенных складов в Китае с доставкой от 12 дней до '
                'Москвы.',
    'product3': 'Здесь ты можешь купить сразу же два продукта со скидкой.'
}

# Обработчик команды /start и создание клавиатуры
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    item_price = types.InlineKeyboardButton('Price', callback_data='price')
    item_products = types.InlineKeyboardButton('Products', callback_data='products')
    keyboard.add(item_price, item_products)
    bot.send_message(message.chat.id, 'Привет! Я бот телеграм канала PoizonLook. Здесь ты можешь посчитать примерную '
                                      'стоимость вещи с доставкой из Китая(она будет отличаться от конечной на +- 500 '
                                      'рублей). а также научиться самостоятельно выкупать'
                                      'товары из Китая и пополнять свой кошелек Alipay самостоятельно и без '
                                      'посредников. Выбери нужную тебе команду:', reply_markup=keyboard)


# Обработчик команды /price
@bot.callback_query_handler(func=lambda call: call.data == 'price')
def price_command(call):
    back_button = types.InlineKeyboardButton('Назад', callback_data='back')
    keyboard = types.InlineKeyboardMarkup().add(back_button)
    bot.send_message(call.message.chat.id, 'Введите стоимость товара в юанях:')
    # Устанавливаем состояние "waiting_for_price" для пользователя
    bot.register_next_step_handler(call.message, handle_price_input)

# Обработчик ввода числа
def handle_price_input(message):
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

# Обработка нажатия на кнопку "Products"
@bot.callback_query_handler(func=lambda call: call.data == 'products')
def products_command(call):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    item_product1 = types.InlineKeyboardButton('Самостоятельное пополнение Alipay + подарок', callback_data='product1')
    item_product2 = types.InlineKeyboardButton('Самостоятельный выкуп товаров с китайских маркетплейсов + подарок', callback_data='product2')
    item_product3 = types.InlineKeyboardButton('Оба обучения со скидкой', callback_data='product3')
    keyboard.add(item_product1, item_product2, item_product3)
    bot.send_message(call.message.chat.id, 'Выберите продукт:', reply_markup=keyboard)

# Обработка нажатия на кнопку с продуктом
@bot.callback_query_handler(func=lambda call: call.data.startswith('product'))
def product_description(call):
    product_id = call.data
    description = get_product_description(product_id)
    bot.send_message(call.message.chat.id, f"Описание продукта {product_id}:\n{description}")

# Реализация функции get_product_description()
def get_product_description(product_id):
    return product_descriptions.get(product_id, 'Описание не найдено.')

# Обработка нажатия на кнопку "назад"
@bot.callback_query_handler(func=lambda call: call.data == 'back')
def back_button_handler(call):
    # Вызываем обработчик команды /start
    start(call.message)

# Запуск бота
if __name__ == '__main__':
    bot.polling()




