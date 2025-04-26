import time
import random
import logging
import telebot
from telebot import types
from core import templates
from core.utils import generate_main_menu, generate_meme_buttons
from core.fetchers import search_parrot_short, fetch_currency_rates, fetch_random_article

logger = logging.getLogger(__name__)

class UniversalBot:
    def __init__(self, api_token, youtube_api_key):
        self.bot = telebot.TeleBot(api_token)
        self.user_states = {}
        self.user_stats = {}
        self.youtube_api_key = youtube_api_key
        self.register_handlers()

    def register_handlers(self):
        self.bot.message_handler(commands=['start'])(self.send_welcome)
        self.bot.message_handler(func=lambda m: m.text == '/help' or m.text == '❓ Помощь')(self.help_command)
        self.bot.message_handler(func=lambda m: m.text == '/about' or m.text == 'ℹ️ О боте')(self.about_command)
        self.bot.message_handler(commands=['stats'])(self.stats_command)
        self.bot.message_handler(func=lambda m: True)(self.handle_text)
        self.bot.callback_query_handler(func=lambda call: True)(self.handle_query)

    def send_welcome(self, message):
        reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        reply.add(
            types.KeyboardButton('❓ Помощь'),
            types.KeyboardButton('ℹ️ О боте')
        )
        self.bot.send_message(message.chat.id, "👑 Добро пожаловать в УНИВЕРСАЛЬНЫЙ БОТ ХУЙНИ!\n Нажми кнопку:", reply_markup=reply)
        self.bot.send_message(message.chat.id, "👇 Главное меню:", reply_markup=generate_main_menu())

    def help_command(self, message):
        self.bot.send_message(message.chat.id, "🛠 Команды бота:\n/start — вернуться в меню\n/stats — сколько мемов ты получил\n/about — о боте\n\nИспользуй кнопки для выбора!")

    def about_command(self, message):
        self.bot.send_message(message.chat.id, "👾 Этот бот создан по приколу🐲\nGitHub: https://github.com/ex1st-dev\nTelegram: @E25X55I75\n\nУНИВЕРСАЛЬНЫЙ БОТ ХУЙНИ — место, где правит хаос и мемы! 💣")

    def stats_command(self, message):
        count = self.user_stats.get(message.chat.id, 0)
        self.bot.send_message(message.chat.id, f"📈 Ты получил {count} мемов, во истину ты мемный магистр!")

    def handle_query(self, call):
        chat_id = call.message.chat.id
        self.bot.answer_callback_query(call.id)
        if call.data == 'meme_generator':
            self.bot.send_message(chat_id, "🎲 Добро пожаловать в ASCII-арт Мемогенератор!", reply_markup=generate_meme_buttons())
        elif call.data == 'random_number':
            self.bot.send_message(chat_id, "🎲 Введи минимальное число:")
            self.user_states[chat_id] = 'waiting_for_min'
        elif call.data.startswith('feature_'):
            self.bot.send_message(chat_id, "🚧 Функция в разработке!", reply_markup=generate_main_menu())
        elif call.data == 'back_to_main':
            self.bot.send_message(chat_id, "⬅️ Возвращаемся в главное меню.", reply_markup=generate_main_menu())
        elif call.data == 'create_1':
            self.increment_user_stats(chat_id)
            template = random.choice(templates.templates)
            self.bot.send_message(chat_id, f"👉 ASCII-арт мем:\n{template}", reply_markup=generate_meme_buttons())
        elif call.data == 'create_3':
            selected = random.sample(templates.templates, 3)
            for idx, template in enumerate(selected, start=1):
                self.increment_user_stats(chat_id)
                self.bot.send_message(chat_id, f"👉 ASCII-арт мем {idx}:\n{template}")
                time.sleep(0.1)
            self.bot.send_message(chat_id, "✅ Тройная порция мемов!", reply_markup=generate_meme_buttons())
        elif call.data == 'create_custom':
            self.bot.send_message(chat_id, "✍️ Напиши текст для мема:")
            self.user_states[chat_id] = 'waiting_for_text'
        elif call.data == 'bombard':
            self.bot.send_message(chat_id, "💣 Пошла жара! Бомбардировка мемами:")
            selected = random.sample(templates.templates, 10)
            for idx, template in enumerate(selected, start=1):
                self.increment_user_stats(chat_id)
                self.bot.send_message(chat_id, f"💥 Мем {idx}:\n{template}")
                time.sleep(0.3)
            self.bot.send_message(chat_id, "🎯 Всё поле завалено мемами!", reply_markup=generate_meme_buttons())
        elif call.data == 'currency_rates':
            try:
                data = fetch_currency_rates()
                usd_to_rub = round(data['rates']['RUB'], 2)
                eur_to_rub = round(data['rates']['RUB'] / data['rates']['EUR'], 2)
                kzt_to_rub = round(data['rates']['RUB'] / data['rates']['KZT'], 4)
                message = (
                    f"💰 *Курс валют к рублю:*\n\n"
                    f"🇺🇸 1 Доллар = {usd_to_rub} ₽\n"
                    f"🇪🇺 1 Евро = {eur_to_rub} ₽\n"
                    f"🇰🇿 1 Тенге = {kzt_to_rub} ₽\n"
                )
                self.bot.send_message(chat_id, message, parse_mode="Markdown", reply_markup=generate_main_menu())
            except Exception as e:
                logger.error(f"Ошибка получения курса валют: {e}")
                self.bot.send_message(chat_id, "🚫 Ошибка при получении курса валют.", reply_markup=generate_main_menu())
        elif call.data == 'random_article':
            try:
                data = fetch_random_article()
                title = data.get('title', 'Без названия')
                extract = data.get('extract', 'Нет описания')
                page_url = data.get('content_urls', {}).get('desktop', {}).get('page', 'Нет ссылки')
                message = f"📚 *{title}*\n\n{extract}\n\n[Читать статью полностью]({page_url})"
                self.bot.send_message(chat_id, message, parse_mode="Markdown", reply_markup=generate_main_menu())
            except Exception as e:
                logger.error(f"Ошибка получения статьи Википедии: {e}")
                self.bot.send_message(chat_id, "🚫 Ошибка при получении статьи.", reply_markup=generate_main_menu())
        elif call.data == 'fresh_parrot':
            link = search_parrot_short(self.youtube_api_key)
            if link:
                self.bot.send_message(chat_id, f"🦜 Лови попугая!\n{link}", reply_markup=generate_main_menu())
            else:
                self.bot.send_message(chat_id, "🚫 Не удалось найти попугая...", reply_markup=generate_main_menu())

    def handle_text(self, message):
        chat_id = message.chat.id
        state = self.user_states.get(chat_id)
        if state == 'waiting_for_text':
            user_text = message.text
            self.user_states.pop(chat_id, None)
            self.increment_user_stats(chat_id)
            template = random.choice(templates.templates)
            if "{твой текст сюда}" in template:
                meme = template.replace("{твой текст сюда}", user_text)
            else:
                meme = f"{template}\n\n🖊️ Твой текст: {user_text}"
            self.bot.send_message(chat_id, meme, reply_markup=generate_meme_buttons())
        elif state == 'waiting_for_min':
            try:
                self.user_states[chat_id] = {'min': int(message.text)}
                self.bot.send_message(chat_id, "✍️ Теперь введи максимальное число:")
            except ValueError:
                self.bot.send_message(chat_id, "🚫 Нужно ввести целое число! Попробуй ещё раз:")
        elif isinstance(state, dict) and 'min' in state:
            try:
                min_val = state['min']
                max_val = int(message.text)
                if max_val < min_val:
                    self.bot.send_message(chat_id, "🚫 Максимум должен быть больше минимума. Попробуй ещё раз.")
                    return
                random_number = random.randint(min_val, max_val)
                self.bot.send_message(chat_id, f"🎯 Случайное число от {min_val} до {max_val}: {random_number}", reply_markup=generate_main_menu())
                self.user_states.pop(chat_id, None)
            except ValueError:
                self.bot.send_message(chat_id, "🚫 Нужно ввести целое число! Попробуй ещё раз:")

    def increment_user_stats(self, chat_id):
        self.user_stats[chat_id] = self.user_stats.get(chat_id, 0) + 1

    def run(self):
        while True:
            try:
                self.bot.infinity_polling()
            except Exception as e:
                logger.error(f"💥 Ошибка подключения: {e}")
                time.sleep(3)