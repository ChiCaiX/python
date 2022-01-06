#coding:utf-8
"""
admin类
1. admin 类的搭建
2. 获取用户的函数（包含验证身份）
3. 添加用户(判断当前身份是否是管理员)
4.冻结和恢复神父
5. 修改用户身份
"""
import os
from gift.base import Base
from gift.common.error import NotUserError,UserActiveError,RoleError
class Admin(Base):
    def __init__(self,username,user_json,gift_json):
        self.username=username
        super().__init__(user_json,gift_json)
        self.get_user()
# 获取用户的函数（包含验证身份）
    def get_user(self):
        users = self._Base__read_users()
        current_user = users.get(self.username)
        if current_user == None:
            raise NotUserError('not user %s' % self.username)
        if current_user.get('active') == False:
            raise UserActiveError('the user %s  had not use' % self.username)
        if current_user.get('role') != 'admin':
            raise RoleError('permission by admin ')
        self.user = current_user
        self.role = current_user.get('role')
        self.name = current_user.get('username')
        self.active = current_user.get('active')

    def __check(self, message):
        self.get_user()
        if self.role != 'admin':
            raise Exception(message)
# 2. 添加用户
    def add_user(self,username,role):
        # self.__check('permission')
        self._Base__write_users(username=username,role=role)
#冻结和恢复神父
    def update_user_active(self,username):
        self._Base_change_active(username=username)
#   修改用户身份
    def change_user_role(self,username,role):
        self._Base_change_role(username=username,role=role)
if __name__ =="__main__":
    gift_path = os.path.join(os.getcwd(), 'storage', 'gift.json')
    user_path = os.path.join(os.getcwd(), 'storage', 'user.json')
    print(gift_path)
    print(user_path)
    # amdin = Admin('ccc',user_path,gift_path)
    admin = Admin('ccc', user_json=user_path, gift_json=gift_path)
    print(admin.name,admin.role)
    # admin.add_user(username="fs1",role="normal")