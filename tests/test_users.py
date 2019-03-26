import pytest, toml
from service.extract import ProcessUsers
from service.exceptions import FormatError

conf_dic = toml.load('config.toml')
passwd_file = conf_dic['files']['test']['passwd']
users = ProcessUsers()
users.set_path(passwd_file)


def test_get_users():
    all_users = users.get_users()
    assert len(all_users) == 37

    user_to_test = all_users[5]
    user = "sync:x:5:0:sync:/sbin:/bin/sync"
    assert user_to_test == _convert_to_dict(user)

    user_to_test = all_users[28]
    user = {"name": "oprofile", "uid": 16, "gid": 16, "comment": "Special user account to be used by OProfile",
            "home": "/home/oprofile", "shell": "/sbin/nologin"}
    assert user_to_test == user


def test_get_by_uid():
    uid_to_test = 14
    user_to_test = users.get_user_by_uid(uid_to_test)
    user = "ftp:x:14:50:FTP User:/var/ftp:/sbin/nologin"
    assert user_to_test == _convert_to_dict(user)

    uid_to_test = 97
    user_to_test = users.get_user_by_uid(uid_to_test)
    user = "dovecot:x:97:97:dovecot:/usr/libexec/dovecot:/sbin/nologin"
    assert user_to_test == _convert_to_dict(user)

def test_get_user_by_query():
    test_users = ["root:x:0:0:root:/root:/bin/bash", "sync:x:5:0:sync:/sbin:/bin/sync",
             "shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown", "halt:x:7:0:halt:/sbin:/sbin/halt",
                  "operator:x:11:0:operator:/root:/sbin/nologin"]
    test_users = [_convert_to_dict(u) for u in test_users]
    user_list = users.get_user_by_query({"gid": 0})
    assert test_users == user_list

    test_users = ["sync:x:5:0:sync:/sbin:/bin/sync",
             "shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown", "halt:x:7:0:halt:/sbin:/sbin/halt"]
    test_users = [_convert_to_dict(u) for u in test_users]
    user_list = users.get_user_by_query({"gid": 0, "home": "/sbin"})
    assert test_users == user_list

    test_users = []
    user_list = users.get_user_by_query({"name": "nfsnobody", "uid": 65537})
    assert test_users == user_list

    test_users = ["mailnull:x:47:51::/var/spool/mqueue:/sbin/nologin", "smmsp:x:51:51::/var/spool/mqueue:/sbin/nologin"]
    test_users = [_convert_to_dict(u) for u in test_users]
    user_list = users.get_user_by_query({"gid": 51, "home": "/var/spool/mqueue", "shell": "/sbin/nologin"})
    assert test_users == user_list

    test_users = ["mailnull:x:47:51::/var/spool/mqueue:/sbin/nologin"]
    test_users = [_convert_to_dict(u) for u in test_users]
    user_list = users.get_user_by_query({"uid": 47, "gid": 51, "home": "/var/spool/mqueue", "shell": "/sbin/nologin"})
    assert test_users == user_list



def _convert_to_dict(user_str):
    name, passwd, uid, gid, comment, home, shell = user_str.split(":")
    user = dict()
    user["name"] = name
    user["uid"] = int(uid)
    user["gid"] = int(gid)
    user["comment"] = comment
    user["home"] = home
    user["shell"] = shell
    return user
