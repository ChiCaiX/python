#coding:utf-8
import os

from gift.common.error import UserExitError, RoleError, LevelError
from gift.common.utils import check_file,timestamp_to_date
from gift.common.consts import ROLES,FIRSTLEVELS,SECONDLEVELS
import json,time

class Base(object):
    def __init__(self, user_json, gift_json):
        self.user_json = user_json
        self.gift_json = gift_json
        self.__check_user_json()
        self.__init_gifts()

    def __check_user_json(self):
       check_file(self.user_json)
    def __check_gift_json(self):
       check_file(self.gift_json)

       # 封装保存函数
    def __save(self, data, path):
        json_data = json.dumps(data)

        with open(path, 'w') as f:
            f.write(json_data)
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

# gifts
    def __read_gifts(self):
        with open(self.gift_json) as f:
            data = json.loads(f.read())
        return data
    # gifts 初始化
    """
    "level1": {
    "level1": {
      "HUAWEI": {
        "name": "HUAWEI",
        "count": 1320
      }
    },
    "level2": {},
    "level3": {}
    }
    """
    def __init_gifts(self):
        data = {
            'level1':{
                'level1':{},
                'level2':{},
                'level3':{}
            },
            'level2': {
                'level1': {},
                'level2': {},
                'level3': {}
            },
            'level3': {
                'level1': {},
                'level2': {},
                'level3': {}
            },
            'level4': {
                'level1': {},
                'level2': {},
                'level3': {}
            }
        }
        gifts = self.__read_gifts()
        if len(gifts)!=0:
            return
        json_data = json.dumps(data)
        with open(self.gift_json,'w') as f:
            f.write(json_data)
# 写入奖品
    def write_gift(self,first_level,second_level,gift_name,gift_count):
        if first_level not in FIRSTLEVELS:
            raise LevelError("firstlevel not exists")
        if second_level not in SECONDLEVELS:
            raise LevelError("second_level not exists")
        # 读取gifts
        gifts = self.__read_gifts()
        current_gift_pool = gifts[first_level]
        current_second_gift_pool = current_gift_pool[second_level]
        if gift_count <=0:
            gift_count = 1
        if gift_name in current_second_gift_pool:
            current_second_gift_pool[gift_name]['count'] = current_second_gift_pool[gift_name]['count'] + gift_count
        else :
            current_second_gift_pool[gift_name]={
                'name':gift_name,
                'count':gift_count
            }
        current_gift_pool[second_level] = current_second_gift_pool
        gifts[first_level] = current_gift_pool
        json_data = json.dumps(gifts)
        with open(self.gift_json,'w') as f:
            f.write(json_data)
        # self.__save(gifts, self.gift_json)
# gifts 修改（数量递减）
    def update_gift(self,first_level,second_level,gift_name,gift_count):
        if first_level not in FIRSTLEVELS:
            raise LevelError("firstlevel not exists")
        if second_level not in SECONDLEVELS:
            raise LevelError("second_level not exists")
            # 读取gifts
            gifts = self.__read_gifts()
            current_gift_pool = gifts[first_level]
            current_second_gift_pool = current_gift_pool[second_level]
            if gift_name not in level_two :
                return False


# gifts 删除
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
    base.write_gift(first_level='level1',second_level='level2',gift_name='iphone10',gift_count=5)
