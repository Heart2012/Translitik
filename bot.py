import logging
import re
from aiogram import Bot, Dispatcher, executor, types
import os

# 🔐 Токен з BotFather
TOKEN = os.getenv("BOT_TOKEN")

# Ініціалізація
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# 🔤 Транслітерація (спрощена, як у Telegram username)
translit_map = {
    'а':'a','б':'b','в':'v','г':'h','ґ':'g','д':'d','е':'e','є':'ie','ж':'zh',
    'з':'z','и':'y','і':'i','ї':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
    'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'kh','ц':'ts',
    'ч':'ch','ш':'sh','щ':'shch','ь':'','ю':'iu','я':'ia',
    'А':'a','Б':'b','В':'v','Г':'h','Ґ':'g','Д':'d','Е':'e','Є':'ie','Ж':'zh',
    'З':'z','И':'y','І':'i','Ї':'i','Й':'i','К':'k','Л':'l','М':'m','Н':'n',
    'О':'o','П':'p','Р':'r','С':'s','Т':'t','У':'u','Ф':'f','Х':'kh','Ц':'ts',
    'Ч':'ch','Ш':'sh','Щ':'shch','Ь':'','Ю':'iu','Я':'ia'
}

def transliterate(text):
    result = ""
    for char in text:
        result += translit_map.get(char, char)
    result = re.sub(r'[^a-zA-Z0-9]+', '_', result)  # заміна пробілів і знаків
    result = re.sub(r'_+', '_', result).strip('_')   # очищення зайвих "_"
    return result.lower()

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.answer("👋 Привіт! Надішли мені слово або фразу українською — я зроблю транслітерацію, як у пошуку Telegram.\n\nНаприклад:\nновини → noviny\nкиївські новини → kyivski_novyny")

@dp.message_handler()
async def translit_message(msg: types.Message):
    text = msg.text.strip()
    result = transliterate(text)
    await msg.answer(result or "🤔 Не вдалося транслітерувати текст.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
