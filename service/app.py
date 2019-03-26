import os
from flask import Flask, request, abort, json, jsonify
from extract import ProcessUsers, ProcessGroups, FormatError

app = Flask("passwd")
users = ProcessUsers()
groups = ProcessGroups()

'''view functions'''

@app.route('/users')
def get_users():
    #get list of all users in system
    try:
        user_list = users.get_users()
    except (FormatError, FileNotFoundError) as e:
        raise InvalidFile('Invalid file. File is malformed or does not exist.')
    return json.dumps(user_list, sort_keys=False)

@app.route('/users/query')
def get_user_query():
    #get user/users matching a specific query
    query = request.args
    valid_fields = ["name", "uid", "gid", "comment", "home", "shell"]
    fields = list(query.keys())
    q = {}
    for f in fields:
        if f not in valid_fields:
            raise InvalidUsage('Invalid query. Please check query fields.')
        else:
            if f == "uid":
                uid = query.get("uid")
                if not represents_int(uid):
                    raise InvalidUsage('Invalid uid passed. Uid must be an int.')
                q["uid"] = int(uid)
            elif f == "gid":
                gid = query.get("gid")
                if not represents_int(gid):
                    raise InvalidUsage('Invalid gid passed. Gid must be an int.')
                q["gid"] = int(gid)
            else:
                q[f] = query.get(f)
    try:
        user = users.get_user_by_query(q)
    except (FormatError, FileNotFoundError) as e:
        raise InvalidFile('Invalid file. File is malformed or does not exist.')
    if not user:
        raise NotFound("No user found for that query.")
    return json.dumps(user, sort_keys=False)

@app.route('/users/<uid>')
def get_user_by_uid(uid):
    #get user matching some uid
    if not represents_int(uid):
        raise InvalidUsage('Invalid uid passed. Uid must be an int.')
    try:
        user = users.get_user_by_uid(int(uid))
    except (FormatError, FileNotFoundError) as e:
        raise InvalidFile('Invalid file. File is malformed or does not exist.')
    if not user:
        raise NotFound("No user found for that uid.")
    return json.dumps(user, sort_keys=False)

@app.route('/users/<uid>/groups')
def get_user_groups(uid):
    #get all groups a user is a member of, given a user id
    if not represents_int(uid):
        raise InvalidUsage('Invalid uid passed. Uid must be an int.')
    try:
        user = users.get_user_by_uid(int(uid))
    except (FormatError, FileNotFoundError) as e:
        raise InvalidFile('Invalid file. File is malformed or does not exist.')
    if not user:
        raise NotFound("No user found for that uid.")
    user_name = user.get("name")
    group_list = groups.get_groups_for_user(user_name)

    return json.dumps(group_list, sort_keys=False)

@app.route('/groups')
def get_groups():
    #get list of all groups in system
    try:
        group_list = groups.get_groups()
    except (FormatError, FileNotFoundError) as e:
        raise InvalidFile('Invalid file. File is malformed or does not exist.')
    return json.dumps(group_list, sort_keys=False)

@app.route('/groups/query')
def get_group_query():
    #get group/groups matching a specified query
    query = request.args
    valid_fields = ["name", "gid", "member"]
    fields = list(query.keys())
    q = {}
    member_list = []
    for f in fields:
        if f not in valid_fields:
            raise InvalidUsage('Invalid query. Please check query fields.')
        else:
            if f == "gid":
                gid = query.get("gid")
                if not represents_int(gid):
                    raise InvalidUsage('Invalid gid passed. Gid must be an int.')
                q["gid"] = int(gid)
            elif f == "member":
                members = query.getlist("member")
                for m in members:
                    member_list.append(m)
                q["members"] = member_list
            else:
                q[f] = query.get(f)
    try:
        group_list = groups.get_group_by_query(q)
    except (FormatError, FileNotFoundError) as e:
        raise InvalidFile('Invalid file. File is malformed or does not exist.')
    if not group_list:
        raise NotFound('No groups found for that query.')
    return json.dumps(group_list, sort_keys=False)

@app.route('/groups/<gid>')
def get_group_by_gid(gid):
    #get group matching some gid
    if not represents_int(gid):
        raise InvalidUsage('Invalid gid passed. Gid must be an int.')
    try:
        group = groups.get_group_by_gid(int(gid))
    except (FormatError, FileNotFoundError) as e:
        raise InvalidFile('Invalid file. File is malformed or does not exist.')
    if not group:
        raise NotFound('That gid was not found.')
    return json.dumps(group, sort_keys=False)


'''exceptions and error handlers'''
#custom exception for queries that are invalid
class InvalidUsage(Exception):
    def __init__(self, message, status_code=400, payload=None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        d = dict(self.payload or ())
        d['message'] = self.message
        return d

#custom exception for files that are invalid
class InvalidFile(Exception):
    def __init__(self, message, status_code=500, payload=None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        d = dict(self.payload or ())
        d['message'] = self.message
        return d

#custom exception for user or group not found
class NotFound(Exception):
    def __init__(self, message, status_code=404, payload=None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        d = dict(self.payload or ())
        d['message'] = self.message
        return d

#check if parameter string is an integer
def represents_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

#error handler that returns response for InvalidFile exception
@app.errorhandler(InvalidFile)
@app.errorhandler(InvalidUsage)
@app.errorhandler(NotFound)
def handle_invalid_file(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def run(user_path, group_path, port):
    users.set_path(user_path)
    groups.set_path(group_path)
    app.run(port=port)