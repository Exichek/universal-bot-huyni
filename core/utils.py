from telebot import types

def generate_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('😎 ASCII-арт Мемогенератор', callback_data='meme_generator'),
        types.InlineKeyboardButton('🎲 Генератор чисел', callback_data='random_number'),
        types.InlineKeyboardButton('💰 Курс валют $ € ₸', callback_data='currency_rates'),
        types.InlineKeyboardButton('📚 Рандомная вики статья', callback_data='random_article'),
        types.InlineKeyboardButton('🦜 Попугай с YouTube', callback_data='fresh_parrot'),
        types.InlineKeyboardButton('💀 ================', callback_data='feature_6'),
        types.InlineKeyboardButton('🚀 ================', callback_data='feature_7'),
        types.InlineKeyboardButton('🐙 ================', callback_data='feature_8'),
        types.InlineKeyboardButton('👽 ================', callback_data='feature_9'),
        types.InlineKeyboardButton('🔥 ================', callback_data='feature_10')
    )
    return markup

def generate_meme_buttons():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('😎 1 мем', callback_data='create_1'),
        types.InlineKeyboardButton('😎 3 мема', callback_data='create_3')
    )
    markup.add(
        types.InlineKeyboardButton('✍️ Свой текст', callback_data='create_custom'),
        types.InlineKeyboardButton('🎇 Бомбардировка', callback_data='bombard')
    )
    markup.add(
        types.InlineKeyboardButton('🔙 Назад в меню', callback_data='back_to_main')
    )
    return markup
