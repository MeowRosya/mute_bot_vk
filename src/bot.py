import random
import time
import asyncio

from config import bot

from storage import Storage
from vkbottle.bot import Message


storage = Storage()


async def delete(peer_id, message_id):
    await bot.api.messages.delete(
        cmids=[message_id], peer_id=peer_id, delete_for_all=True
    )


async def on_startup():
    conversations = await bot.api.messages.get_conversations()
    for chat in conversations.items:
        if chat.conversation.peer.id < 2000000000:
            continue
        members = await bot.api.messages.get_conversation_members(
            peer_id=chat.conversation.peer.id
            )
        map(lambda x: storage.add_id(x.member_id), members.items)


@bot.on.chat_message()
async def chat_message(message: Message):
    user_id = message.from_id
    peer_id = message.peer_id
    cmid = message.conversation_message_id
    if user_id in storage.trust_ids:
        pass
    elif user_id not in storage.muted_ids:
        storage.muted_ids.update({user_id: time.time()})
        await delete(peer_id, cmid)
        message_id = await bot.api.messages.send(
            peer_id=peer_id,
            random_id=random.getrandbits(128),
            message="К нам присоединился новый пользователь. Добро пожаловать! " +
                    "В течении первой минуты общения, вы не можете писать сообщения. " +
                    "Просим прощения за неудобство",
        )
        await asyncio.sleep(20)
        await bot.api.messages.delete(
            peer_id=peer_id,
            message_ids=[message_id],
            delete_for_all=True
            )
    else:
        if time.time() - storage.muted_ids.get(user_id) > 60:
            storage.muted_ids.pop(user_id)
            storage.add_id(user_id=user_id)
            return
        await delete(peer_id, cmid)

if __name__ == "__main__":
    bot.loop_wrapper.add_task(on_startup())
    bot.run_forever()
