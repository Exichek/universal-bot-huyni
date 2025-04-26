from core.bot_core import UniversalBot

API_TOKEN = '7339896862:AAGUYCq0FgFcJEfF7uH2jsiIsw8PsQwx0eY'
YOUTUBE_API_KEY = 'AIzaSyBusydtybS9rJzSqaBqcs-KMQleG3AIjt8'

if __name__ == "__main__":
    bot = UniversalBot(API_TOKEN, YOUTUBE_API_KEY)
    bot.run()

