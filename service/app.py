import os
from flask import Flask, request, abort, json
from extract import AllUsers, AllGroups

app = Flask("passwd")
users = AllUsers()
groups = AllGroups()

@app.route('/users', methods=['GET'])
def get_users():
    user_list = users.get_users()
    if not user_list:
        abort(404)
    return json.dumps(user_list, sort_keys=False)

@app.route('/users/<uid>', methods=['GET'])
def get_user_by_uid(uid):
    user = users.get_user_by_uid(int(uid))
    return json.dumps(user, sort_keys=False)

@app.route('/groups', methods=['GET'])
def get_groups():
    group_list = groups.get_groups()
    if not group_list:
        abort(404)
    return json.dumps(group_list, sort_keys=False)

def run(user_path, group_path, port):
    users.set_path(user_path)
    groups.set_path(group_path)
    app.run(port=port)