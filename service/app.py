import os
from flask import Flask, request, abort, json, jsonify
from extract import ProcessUsers, ProcessGroups

app = Flask("passwd")
users = ProcessUsers()
groups = ProcessGroups()

'''view functions'''

@app.route('/users')
def get_users():
    #get list of all users in system
    user_list = users.get_users()
    if not user_list:
        abort(404, "No users found.")
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
            raise InvalidUsage('Invalid query. Please check query fields.', status_code=400)
        else:
            if f == "uid":
                q["uid"] = int(query.get("uid"))
            elif f == "gid":
                q["gid"] = int(query.get("gid"))
            else:
                q[f] = query.get(f)
    user = users.get_user_by_query(q)
    if not user:
        abort(404, 'No users found for that query')
    return json.dumps(user, sort_keys=False)

@app.route('/users/<int:uid>')
def get_user_by_uid(uid):
    #get user matching some uid
    user = users.get_user_by_uid(uid)
    if not user:
        abort(404, "That uid was not found.")
    return json.dumps(user, sort_keys=False)

@app.route('/users/<int:uid>/groups')
def get_user_groups(uid):
    #get all groups a user is a member of, given a user id
    user = users.get_user_by_uid(uid)
    if not user:
        abort(404, "That uid was not found.")
    user_name = user["name"]
    group_list = groups.get_groups_for_user(user_name)

    return json.dumps(group_list, sort_keys=False)

@app.route('/groups')
def get_groups():
    #get list of all groups in system
    group_list = groups.get_groups()
    if not group_list:
        abort(404, "No groups found.")
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
            raise InvalidUsage('Invalid query. Please check query fields.', status_code=400)
        else:
            if f == "gid":
                q["gid"] = int(query.get("gid"))
            elif f == "member":
                members = query.getlist("member")
                for m in members:
                    member_list.append(m)
                q["members"] = member_list
            else:
                q[f] = query.get(f)
    group_list = groups.get_group_by_query(q)
    if not group_list:
        abort(404, 'No groups found for that query')
    return json.dumps(group_list, sort_keys=False)

@app.route('/groups/<int:gid>')
def get_group_by_gid():
    #get group matching some gid
    group = groups.get_group_by_gid()
    if not group:
        abort(404, "That gid was not found.")
    return json.dumps(group, sort_keys=False)


'''exceptions and error handlers'''
#custom exception for invalid API calls
class InvalidUsage(Exception):
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

#error handler that returns response for InvalidUsage exception
@app.errorhandler(InvalidUsage)
def handle_invalid_query(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def run(user_path, group_path, port):
    users.set_path(user_path)
    groups.set_path(group_path)
    app.run(port=port)