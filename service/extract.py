import os
from service.exceptions import *

"""Logic for parsing passwd file and creating appropriate data structures
for efficient lookup of users"""
class ProcessUsers:

    def __init__(self):
        self.passwd_path = None
        self.last_modified = None
        self.users = []
        self.uid_to_user = dict()

    #set file path of passwd file
    def set_path(self, p):
        self.passwd_path = p

    #process passwd file
    def _read_file(self):
        #check if file has been modified since last time users were extracted from file
        time_modified = os.path.getmtime(self.passwd_path)
        if time_modified != self.last_modified:
            self.last_modified = time_modified
            try:
                with open(self.passwd_path, "r") as file:
                    for line in file:
                        line = line.strip()
                        fields = line.split(":")
                        #check if line contains all the necessary fields
                        if len(fields) != 7:
                            raise FormatError("Invalid passwd file; file is missing fields or incorrectly formatted.")
                        name = fields[0]
                        uid = int(fields[2])
                        gid = int(fields[3])
                        comment = fields[4]
                        home = fields[5]
                        shell = fields[6]
                        #create dictionary representing the user
                        u = {"name": name, "uid": uid, "gid": gid, "comment": comment, "home": home, "shell": shell}
                        #add user to list of users
                        self.users.append(u)
                        #create mapping from user id to user
                        self.uid_to_user[uid] = u
            except FileNotFoundError:
                print("No such file found.")
            except ValueError:
                print("User id and group id fields are invalid.")

    #returns list of users
    def get_users(self):
        self._read_file()
        return self.users

    #returns user for a given user id
    def get_user_by_uid(self, id):
        self._read_file()
        return self.uid_to_user[id]

    #returns user matching specified query
    def get_user_by_query(self, q):
        self._read_file()
        matching_users = []
        for u in self.users:
            user_found = True
            for key in q.keys():
                if q.get(key) != u.get(key):
                    user_found = False
                    break
            if user_found:
                matching_users.append(u)
        return matching_users


"""Logic for parsing group file and creating appropriate data structures
for efficient lookup of groups/groups for each user"""
class ProcessGroups:

    def __init__(self):
        self.group_path = None
        self.last_modified = None
        self.groups = []
        self.gid_to_group = dict()
        self.user_to_gids = dict()

    #set file path of group file
    def set_path(self, p):
        self.group_path = p

    #process group file
    def _read_file(self):
        #check if file has been modified since last time groups were extracted from file
        time_modified = os.path.getmtime(self.group_path)
        if time_modified != self.last_modified:
            self.last_modified = time_modified
            self.groups = []
            self.gid_to_group = dict()
            self.user_to_gids = dict()
            try:
                with open(self.group_path, "r") as file:
                    for line in file:
                        line = line.strip()
                        fields = line.split(":")
                        #check if line contains all the necessary fields
                        if len(fields) != 4:
                            raise FormatError("Invalid group file; file is missing fields or incorrectly formatted.")
                        name = fields[0]
                        gid = int(fields[2])
                        group_list = fields[3]
                        if len(group_list) == 0:
                            group_list = []
                        else:
                            group_list = [usr for usr in group_list.split(",")]
                        g = {"name": name, "gid": gid, "members": group_list}
                        #add group (represented as dictionary) to list of groups
                        self.groups.append(g)
                        #create mapping of group id to group
                        self.gid_to_group[gid] = g
                        #create mapping of user's uid to list of groups it is a member of
                        for member in group_list:
                            member_group_list = self.user_to_gids.get(member)
                            if member_group_list:
                                member_group_list.append(gid)
                            else:
                                self.user_to_gids[member] = [gid]
            except FileNotFoundError:
                print("No such file found.")
            except ValueError:
                print("Group id field is invalid.")

    #returns list of groups
    def get_groups(self):
        self._read_file()
        return self.groups

    #returns group for a given group id
    def get_group_by_gid(self, id):
        self._read_file()
        return self.gid_to_group[id]

    #returns group matching the specified query
    def get_group_by_query(self, q):
        self._read_file()
        matching_groups = []
        for g in self.groups:
            group_found = True
            for key in q.keys():
                if key == "members":
                    query_members = q.get(key)
                    group_members = g.get(key)
                    for m in query_members:
                        if m not in group_members:
                            group_found = False
                            break
                elif q.get(key) != g.get(key):
                    group_found = False
                    break
            if group_found:
                matching_groups.append(g)
        return matching_groups

    #returns list of all groups for given user name
    def get_groups_for_user(self, name):
        self._read_file()
        user_gids = self.user_to_gids.get(name)
        user_group_list = []
        if user_gids:
            for gid in user_gids:
                g = self.gid_to_group.get(gid)
                user_group_list.append(g)
        return user_group_list
