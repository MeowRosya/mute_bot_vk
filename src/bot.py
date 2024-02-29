import asyncio
import random
import time
from enum import Enum
from typing import Any

from user import UserStorage, mute, trust, unmute
from vkbottle import GroupEventType, GroupTypes, Keyboard, KeyboardButtonColor, Text
from vkbottle.bot import Message

from config import (
    DOMAIN,
    DOMAIN_18,
    GROUP_ID,
    HELLO_TEXT,
    HORNY_GROUP_ID,
    MESSAGE_UNDER_NEW_POST,
    TRIGGER,
    bot,
)
from wall import (
    get_wall_posts,
    handle_hent_group_posts,
    handle_main_group_posts,
    update_databases,
)


class Ref:
    def __init__(self, value: list[Any]):
        self = value


photos = []
jokes = []
quotes = []
audios = []
mix = []
horny_photos = []
horny_jokes = []


class ButtonsLabels(Enum):
    PHOTO = "Картинка"
    JOKE = "Шутка"
    QUOTE = "Цитата"
    AUDIO = "Музычка"
    MIX = "MIX"
    HORNY_PHOTO = "Хорни"
    HORNY_JOKE = "Хорни шутка"


equality = {
    ButtonsLabels.PHOTO: photos,
    ButtonsLabels.JOKE: jokes,
    ButtonsLabels.QUOTE: quotes,
    ButtonsLabels.AUDIO: audios,
    ButtonsLabels.MIX: mix,
    ButtonsLabels.HORNY_PHOTO: horny_photos,
    ButtonsLabels.HORNY_JOKE: horny_jokes,
    
}

keyboard = (
    Keyboard(one_time=False, inline=False)
    .add(Text(ButtonsLabels.PHOTO), color=KeyboardButtonColor.POSITIVE)
    .add(Text(ButtonsLabels.JOKE), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text(ButtonsLabels.AUDIO), color=KeyboardButtonColor.NEGATIVE)
    .add(Text(ButtonsLabels.MIX), color=KeyboardButtonColor.NEGATIVE)
    .row()
    .add(Text(ButtonsLabels.QUOTE), color=KeyboardButtonColor.POSITIVE)
    .add(Text(ButtonsLabels.HORNY_PHOTO), color=KeyboardButtonColor.POSITIVE)
    .add(Text(ButtonsLabels.HORNY_JOKE), color=KeyboardButtonColor.POSITIVE)
    .get_json()
)


async def delete(peer_id, message_id):
    await bot.api.messages.delete(
        cmids=[message_id], peer_id=peer_id, delete_for_all=True
    )


async def init():
    global photos, audios, jokes, quotes, mix, horny_jokes, horny_photos
    # obtaining posts from groups
    posts = await get_wall_posts(domain=DOMAIN, group_id=GROUP_ID)
    res = handle_main_group_posts(posts)
    photos += res.photos
    audios += res.audios
    jokes += res.jokes
    quotes += res.quotes
    mix += res.mix

    posts = await get_wall_posts(domain=DOMAIN_18, group_id=HORNY_GROUP_ID)
    res = handle_hent_group_posts(posts)
    horny_photos += res.horny_photos
    horny_jokes += res.horny_jokes

    # adding to storage people that are already in chats to prevent delete message
    conversations = await bot.api.messages.get_conversations()
    for chat in conversations.items or []:
        if chat.conversation.peer.id < 2000000000:
            continue
        members = await bot.api.messages.get_conversation_members(
            peer_id=chat.conversation.peer.id
        )
        for member in members.items:
            user = UserStorage.get_user(member.member_id)
            trust(user)

@bot.on.chat_message()
async def chat_message(message: Message):
    user_id = message.from_id
    peer_id = message.peer_id
    cmid = message.conversation_message_id
    user = UserStorage.get_user(user_id)
    if user.is_trusted:
        if message.text == "Начать":
            await message.answer("Врываюсь", keyboard=keyboard)
        elif message.text.startswith(TRIGGER):
            command = message.text.replace(TRIGGER, "")
            if command in equality:
                await message.answer(
                    command, attachment=random.choice(equality[command])
                )
    elif not user.is_muted:
        mute(user)
        await delete(peer_id, cmid)
        message_id = await bot.api.messages.send(
            peer_id=peer_id,
            random_id=random.getrandbits(128),
            message="К нам присоединился новый пользователь. Добро пожаловать! "
            + "В течении первой минуты общения, вы не можете писать сообщения. "
            + "Просим прощения за неудобство",
        )
        await asyncio.sleep(20)
        await delete(peer_id=peer_id, message_id=message_id)
    elif user.is_muted and user.is_time_to_umnute():
        unmute(user)
        trust(user)
    else:
        await delete(peer_id, cmid)
        return


@bot.on.private_message(text="Начать")
async def start(message: Message):
    await message.answer(HELLO_TEXT, keyboard=keyboard)


@bot.on.private_message(text="Статистика")
async def show_statistic(message: Message):
    text = f"""Артов -- {len(photos)}
Шуток -- {len(jokes)}
Цитат -- {len(quotes)}
Хорни -- {len(horny_photos)}
Хорни шутки -- {len(horny_jokes)}
MIX -- {len(mix)}"""
    await message.answer(text)


@bot.on.private_message()
async def send_message_private(message: Message):
    if message.text not in equality:
        return
    await message.answer(
        message.text, attachment=random.choice(equality[message.text])
    )


@bot.on.raw_event(GroupEventType.WALL_POST_NEW, dataclass=GroupTypes.WallPostNew)
async def new_post(event: GroupTypes.WallPostNew):
    global photos, audios, jokes, quotes, mix
    res = handle_main_group_posts([event.object])
    photos += res.photos
    audios += res.audios
    jokes += res.jokes
    quotes += res.quotes
    mix += res.mix
    if event.object.id:
        await bot.api.wall.create_comment(
            post_id=event.object.id,
            owner_id=GROUP_ID,
            message=MESSAGE_UNDER_NEW_POST,
        )


@bot.loop_wrapper.interval(seconds=60)
async def new_post_from_horny():
    global horny_jokes, horny_photos
    border_time = int(time.time()) - 60
    posts = await update_databases(DOMAIN_18)
    if posts is None:
        return
    res = handle_hent_group_posts(posts=posts, border_time=border_time)
    horny_jokes += res.horny_jokes
    horny_photos += res.horny_photos


def main():
    bot.loop_wrapper.on_startup.append(init())
    bot.run_forever()


if __name__ == "__main__":
    main()
