import os

class AllUsers:
    def __init__(self):
        self.passwd_path = None
        self.last_modified = None
        self.users = []
        self.users_by_uid = dict()

    def set_path(self, p):
        self.passwd_path = p

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
                        u = {"name": name, "uid": uid, "gid": gid, "comment": comment, "home": home, "shell": shell}
                        self.users.append(u)
                        self.users_by_uid[uid] = u
            except FileNotFoundError:
                print("No such file found.")
            except ValueError:
                print("User id and group id fields are invalid.")

    def get_users(self):
        self._read_file()
        return self.users

    def get_user_by_uid(self, id):
        self._read_file()
        return self.users_by_uid[id]

    def get_user_by_query(self, q):
        self._read_file()
        matching_users = []
        for u in self.users:
            user_found = True
            for key in q.keys():
                if q[key] != u[key]:
                    user_found = False
                    break
            if user_found:
                matching_users.append(u)
        return matching_users

class AllGroups:

    def __init__(self):
        self.group_path = None
        self.last_modified = None
        self.groups = []
        self.groups_by_gid = dict()

    def set_path(self, p):
        self.group_path = p

    def _read_file(self):
        #check if file has been modified since last time groups were extracted from file
        time_modified = os.path.getmtime(self.group_path)
        if time_modified != self.last_modified:
            self.last_modified = time_modified
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
                        self.groups.append(g)
                        self.groups_by_gid[gid] = g
            except FileNotFoundError:
                print("No such file found.")
            except ValueError:
                print("Group id field is invalid.")

    def get_groups(self):
        self._read_file()
        return self.groups

    def get_group_by_gid(self, id):
        self._read_file()
        return self.groups_by_gid[id]

    def get_group_by_query(self, q):
        self._read_file()
        matching_groups = []
        for g in self.groups:
            group_found = True
            for key in q.keys():
                if key == "members":
                    for m in q[key]:
                        if m not in g[key]:
                            group_found = False
                elif q[key] != g[key]:
                    group_found = False
                    break
            if group_found:
                matching_groups.append(g)
        return matching_groups

class FormatError(Exception):
    pass