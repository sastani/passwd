import pytest, toml
from service.extract import ProcessGroups
from service.exceptions import FormatError

conf_dic = toml.load('config.toml')
group_file = conf_dic['files']['test']['group']
groups = ProcessGroups()
groups.set_path(group_file)


def test_get_groups():
    all_groups = groups.get_groups()
    assert len(all_groups) == 42

    group_to_test = all_groups[41]
    group = "syslog:x:103:"
    assert group_to_test == _convert_to_dict(group)


def test_get_by_gid():
    gid_to_test = 10
    group_to_test = groups.get_group_by_gid(gid_to_test)
    group = "uucp:x:10:"
    assert group_to_test == _convert_to_dict(group)

    gid_to_test = 65534
    group_to_test = groups.get_group_by_gid(gid_to_test)
    group = "nogroup:x:65534:"
    assert group_to_test == _convert_to_dict(group)

def test_get_group_by_query():
    test_groups = ["adm:x:4:username", "dialout:x:20:username", "cdrom:x:24:username, username1",
                   "www-data:x: 33:username", "plugdev:x:46:username"]
    test_groups = [_convert_to_dict(u) for u in test_groups]
    group_list = groups.get_group_by_query({"members": ["username"]})
    assert test_groups == group_list

    test_groups = ["cdrom:x:24:username, username1"]
    test_groups = [_convert_to_dict(u) for u in test_groups]
    group_list = groups.get_group_by_query({"members": ["username", "username1"]})
    assert test_groups == group_list

    test_groups = []
    group_list = groups.get_group_by_query({"members": ["alpha"]})
    assert test_groups == group_list

    test_groups = ["dialout:x:20:username"]
    test_groups = [_convert_to_dict(u) for u in test_groups]
    group_list = groups.get_group_by_query({"gid": 20, "members": ["username"]})
    assert test_groups == group_list

def test_get_group_for_user():
    test_user = "username"
    test_user_groups = ["adm:x:4:username", "dialout:x:20:username", "cdrom:x:24:username, username1",
                        "www-data:x:33:username", "plugdev:x: 46:username"]
    test_user_groups = [_convert_to_dict(u) for u in test_user_groups]
    group_list = groups.get_groups_for_user(test_user)
    assert test_user_groups == group_list

    test_user = "pulse"
    test_user_groups = ["audio:x:29:pulse"]
    test_user_groups = [_convert_to_dict(u) for u in test_user_groups]
    group_list = groups.get_groups_for_user(test_user)
    assert test_user_groups == group_list

    test_user = "alpha"
    test_user_groups = []
    group_list = groups.get_groups_for_user(test_user)
    assert test_user_groups == group_list


def _convert_to_dict(group_str):
    name, passwd, gid, members = group_str.split(":")
    group = dict()
    group["name"] = name
    group["gid"] = int(gid)
    if members == '':
        group["members"] = []
    else:
        member_list = members.split(", ")
        group["members"] = member_list
    return group
