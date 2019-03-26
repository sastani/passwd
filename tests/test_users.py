import pytest, toml
from service.extract import ProcessUsers

conf_dic = toml.load('config.toml')
passwd_file = conf_dic['files']['test']['users']['path']
users = ProcessUsers()
users.set_path(passwd_file)


def test_get_users():
    all_users = users.get_users()
    assert len(all_users) == 36
    user_to_test = all_users[5]
    user = "sync:x:5:0:sync:/sbin:/bin/sync"
    assert user_to_test == _user_dict(user)
    user_to_test = all_users[28]
    user = {"name": "oprofile", "uid": 16, "gid": 16, "comment": "Special user account to be used by OProfile",
            "home": "/home/oprofile", "shell": "/sbin/nologin"}
    assert user_to_test == user



def test_get_by_uid():
    uid_to_test = 14
    user_info = users.get_user_by_uid(uid_to_test)








def _user_dict(user_str):
    name, passwd, uid, gid, comment, home, shell = user_str.split(":")
    user = {}
    user["name"] = name
    user["uid"] = int(uid)
    user["gid"] = int(gid)
    user["comment"] = comment
    user["home"] = home
    user["shell"] = shell
    return user
