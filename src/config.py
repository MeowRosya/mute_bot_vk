from vkbottle import Bot

TOKEN = ""


with open("src/TOKEN", "r") as f:
    TOKEN = f.read().replace("\n", "")

bot = Bot(token=TOKEN)
