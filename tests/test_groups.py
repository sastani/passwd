import pytest, toml
from service.extract import ProcessGroups
from service.exceptions import FormatError

conf_dic = toml.load('config.toml')
group_file = conf_dic['files']['test']['group']
groups = ProcessGroups()
groups.set_path(group_file)


def test_get_groups():
    all_groups = groups.get_groups()
    assert len(all_groups) == 50
    group_to_test = all_groups[40]
    group = "rpcuser:x:29:"
    assert group_to_test == _convert_to_dict(group)


def test_get_by_gid():
    gid_to_test = 14
    group_to_test = groups.get_group_by_gid(gid_to_test)
    group = "uucp:x:14:uucp"
    assert group_to_test == _convert_to_dict(group)

    gid_to_test = 65534
    group_to_test = groups.get_group_by_gid(gid_to_test)
    group = "nfsnobody:x:65534:"
    assert group_to_test == _convert_to_dict(group)

def test_get_group_by_query():
    test_groups = ["wheel:x:10:root,bezroun,username", "games:x:20:username"]
    test_groups = [_convert_to_dict(u) for u in test_groups]
    group_list = groups.get_group_by_query({"members": ["username"]})
    assert test_groups == group_list

    test_groups = ["bin:x:1:root,bin,daemon", "daemon:x:2:root,bin,daemon", "adm:x:4:root,adm,daemon"]
    test_groups = [_convert_to_dict(u) for u in test_groups]
    group_list = groups.get_group_by_query({"members": ["root", "daemon"]})
    assert test_groups == group_list

    test_groups = ["root:x:0:root", "bin:x:1:root,bin,daemon",
                   "daemon:x:2:root,bin,daemon", "sys:x:3:root,bin,adm", "adm:x:4:root,adm,daemon", "disk:x:6:root",
                   "wheel:x:10:root,bezroun,username"]
    test_groups = [_convert_to_dict(u) for u in test_groups]
    group_list = groups.get_group_by_query({"members": ["root"]})
    assert test_groups == group_list

    test_groups = []
    group_list = groups.get_group_by_query({"members": ["alpha"]})
    assert test_groups == group_list

    test_groups = ["games:x:20:username"]
    test_groups = [_convert_to_dict(u) for u in test_groups]
    group_list = groups.get_group_by_query({"gid": 20, "members": ["username"]})
    assert test_groups == group_list

def test_get_group_for_user():
    test_user = "adm"
    test_user_groups = ["sys:x:3:root,bin,adm", "adm:x:4:root,adm,daemon"]
    test_user_groups = [_convert_to_dict(u) for u in test_user_groups]
    group_list = groups.get_groups_for_user(test_user)
    assert test_user_groups == group_list

    test_user = "gdm"
    test_user_groups = ["audio:x:63:gdm"]
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
        member_list = members.split(",")
        group["members"] = member_list
    return group
