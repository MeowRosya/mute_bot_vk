class Storage:
    def __init__(self):
        self.chats: Chat = []
        self.muted = {}

    def add_chat(self, chat_id: int, members_ids: list[int]):
        self.chats.append(Chat(chat_id=chat_id, members_ids=members_ids))


class Chat:
    def __init__(self, chat_id: int, members_ids: list[int]):
        self.id = chat_id
        self.members: Member = list(map(lambda x: Member(x), members_ids))

    def add_member(self, member_id: int):
        self.members.append(Member(member_id=member_id))


class Member:
    def __init__(self, member_id: int):
        self.id = member_id
