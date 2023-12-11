class Storage:
    def __init__(self):
        self.trust_ids: list[int] = []
        self.muted_ids = {}

    def add_id(self, user_id: int):
        self.trust_ids.append(user_id)
        self.trust_ids = list(set(self.trust_ids))
