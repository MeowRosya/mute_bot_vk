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
    buffer = []
    conversations = await bot.api.messages.get_conversations()
    for chat in conversations.items:
        if chat.conversation.peer.id > 2000000000:
            buffer.append(chat.conversation.peer.id)
    for chat_peer_id in buffer:
        members = await bot.api.messages.get_conversation_members(peer_id=chat_peer_id)
        storage.add_chat(
            chat_id=chat_peer_id, members_ids=list(map(lambda x: x.member_id, members.items))
        )


@bot.on.chat_message()
async def chat_message(message: Message):
    if message.from_id in storage.muted:
        current_time = time.time()
        if current_time - storage.muted.get(message.from_id) > 60:
            storage.muted.pop(message.from_id)
            storage.add_member(message.peer_id, message.from_id)
            return
        await delete(message.peer_id, message.conversation_message_id)
        return
    for i in storage.chats:
        if i.id == message.peer_id:
            chat = i
            break
    if message.from_id not in list(map(lambda x: x.id, chat.members)):
        storage.muted.update({message.from_id: time.time()})
        await delete(message.peer_id, message.conversation_message_id)
        message_id = await bot.api.messages.send(
            peer_id=message.peer_id,
            random_id=random.getrandbits(128),
            message="К нам присоединился новый пользователь. Добро пожаловать! В течении первой минуты общения, вы не можете писать сообщения. Просим прощения за неудобство",
        )
        await asyncio.sleep(20)
        await bot.api.messages.delete(peer_id=message.peer_id, message_ids=[message_id], delete_for_all=True)


if __name__ == "__main__":
    bot.loop_wrapper.add_task(on_startup())
    bot.run_forever()
