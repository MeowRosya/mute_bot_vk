from vkbottle.bot import Bot
from vkbottle.api import API
import os

TOKEN = os.getenv("TOKEN")
SERVICE_TOKEN = os.getenv("SERVICE_TOKEN")


GROUP_ID = -208044622
HORNY_GROUP_ID = -208875807

HELLO_TEXT = (
    "__________________________\n"
    + "🎭| Приветствуем в Синдикате !\n"
    + "Наша задача ,помимо легализации Виабу культуры в странах СНГ - объединение всех Анимешников под нашими знаменами !\n"
    + "🎌| Мы собираемся полностью завладеть рынками сбыта Wifu и диктовать наши условия по всему Содружеству или за его пределами !\n"
    + "🎨| Вступай в наши ряды и вместе мы сделаем Виабу культуру Great Again!\n\n"
    + "🐈| Каждому члену дается право на обладание 1-ой КошкоЖеной !\n"
    + "________________________________\n"
    + "🎬| P.S. Присылайте нам свои работы , мы будем только рады! Опубликуем как художественные произведения, так и видео с музыкой...\n\n"
    + "Наш ютуб - https://www.youtube.com/channel/UCxeUa6xIypztkoEEg0j5IUw"
)

MESSAGE_UNDER_NEW_POST = f"⭐| Понравилось? Не забудь [https://vk.com/widget_community.php?act=a_subscribe_box&oid={GROUP_ID}&state=1|ПОДПИСАТЬСЯ] и поставить лайк!"

TRIGGER = "[club208044622|@anime_syndi_cute] "

service_api = API(token=SERVICE_TOKEN)
bot = Bot(token=TOKEN)
