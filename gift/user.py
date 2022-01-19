#coding:utf-8


from gift.base import Base
class User(Base):
    def __init__(self,username,user_json,gift_json):
        self.username=username
        self.user_json=user_json
        self.gift_json = gift_json
        super().__init__(user_json,gift_json)

