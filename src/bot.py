import random
import time

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
    for chat_id in buffer:
        members = await bot.api.messages.get_conversation_members(peer_id=chat_id)
        storage.add_chat(
            chat_id=chat_id, members_ids=list(map(lambda x: x.member_id, members.items))
        )


@bot.on.chat_message()
async def chat_message(message: Message):
    if message.from_id in storage.muted:
        current_time = time.time()
        if current_time - storage.muted.get(message.from_id) > 60:
            storage.muted.pop(message.from_id)
            storage.chats.add_member(message.from_id)
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
        await bot.api.messages.send(
            user_id=message.from_id,
            random_id=random.getrandbits(128),
            message="Рады что вы решили присоединиться к нашему сообществу! Просьба подождать 1 минуту. Это проверка на спам ботов. Будем рады, если вы подождете!",
        )


if __name__ == "__main__":
    bot.loop_wrapper.add_task(on_startup())
    bot.run_forever()
