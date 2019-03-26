import os
from flask import Flask, request, abort, json, jsonify
from extract import AllUsers, AllGroups

app = Flask("passwd")
users = AllUsers()
groups = AllGroups()

'''view functions'''
@app.route('/users', methods=['GET'])
def get_users():
    user_list = users.get_users()
    if not user_list:
        abort(404)
    return json.dumps(user_list, sort_keys=False)

@app.route('/users/query')
def get_user_query():
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
        abort(404)
    return json.dumps(user, sort_keys=False)

@app.route('/users/<uid>', methods=['GET'])
def get_user_by_uid(uid):
    user = users.get_user_by_uid(int(uid))
    return json.dumps(user, sort_keys=False)

@app.route('/users/<uid>/groups')
def get_user_groups(uid):
    user = users.get_user_by_uid(int(uid))
    user_name = user["name"]
    group_list = groups.get_groups_for_user(user_name)
    return json.dumps(group_list, sort_keys=False)


@app.route('/groups', methods=['GET'])
def get_groups():
    group_list = groups.get_groups()
    if not group_list:
        abort(404)
    return json.dumps(group_list, sort_keys=False)

'''exceptions and error handlers'''
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

@app.errorhandler(InvalidUsage)
def handle_invalid_query(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def run(user_path, group_path, port):
    users.set_path(user_path)
    groups.set_path(group_path)
    app.run(port=port)