#coding:utf-8
import os

from gift.common.error import UserExitError, RoleError
from gift.common.utils import check_file,timestamp_to_date
from gift.common.consts import ROLES
import json,time

class Base(object):
    def __init__(self, user_json, gift_json):
        self.user_json = user_json
        self.gift_json = gift_json
        self.__check_user_json()

    def __check_user_json(self):
       check_file(self.user_json)
    def __check_gift_json(self):
       check_file(self.gift_json)
    # 1. 读写user.json
    def __read_users(self,time_to_str =False):
        with open(self.user_json,'r',) as f :
            data = json.loads(f.read())
        if time_to_str == True:
            for username ,v in data.items():
                v['create_time'] = timestamp_to_date(v['create_time'])
                v['update_time'] = timestamp_to_date(v['update_time'])
            data['username']=v
        return data
    def __write_users(self,**user):
        if 'username' not in user:
            raise ValueError('missage username')
        if 'role' not in user:
            raise ValueError('missage role')
        user['active']=True
        user['create_time']=time.time()
        user['update_time']=time.time()
        user['gifts'] = []
        users = self.__read_users()
        if user['username'] in users:
            raise UserExitError('username %s had exists ' % user['username'])
        users.update({user['username']:user})
        json_users = json.dumps(users)
        with open(self.user_json,'w') as f:
            f.write(json_users)
# 2. 更改用户权限
    def __change_role(self,username,role):
        users = self.__read_users()
        user= users.get(username)
        if not user:
            return False
        if role not in ROLES:
            raise RoleError('not user role %s' % role)
        user['role']=role
        user['update_time']=time.time()
        users[username]=user
        json_users = json.dumps(users)
        with open(self.user_json,'w') as f:
            f.write(json_users)
        return True
# 3. 更改用户的active
    def __change_active(self,username):
        users = self.__read_users()
        user = users.get(username)
        if not user:
            return False
        user['active']= not user['active']
        user['update_time']=time.time()
        users[username]=user
        json_users = json.dumps(users)
        with open(self.user_json,'w') as f:
            f.write(json_users)
        return True
# 4. 删除用户
    def __delete_user(self,username):
        users = self.__read_users()
        user = users.get(username)
        if not user :
            return  False
        delete_user = users.pop(username)
        json_users = json.dumps(users)
        with open(self.user_json,'w') as f:
            f.write(json_users)
        return delete_user


if __name__ =='__main__':
    user_path = os.path.join(os.getcwd(),'storage','user.json')
    gift_path = os.path.join(os.getcwd(),'storage','gift.json')
    print(user_path)
    print(gift_path)
    base = Base(user_path,gift_path)
    # user = base.read_users(time_to_str=True)
    # print(user)
    # info = {"username":'cc1','role':'admin'}
    # base.write_users(**info)
    # base.change_role(username="cc1",role="normal")
    # base.change_active('cc1')
    # info =base.delete_user('cc1')
    # print(info)
    # user = base.read_users(time_to_str=True)
    # print(user)
