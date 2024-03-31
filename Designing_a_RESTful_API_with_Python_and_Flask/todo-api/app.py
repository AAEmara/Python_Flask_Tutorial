#!flask/bin/python3
"""Creating a simple web application."""


from flask import Flask, jsonify, abort, make_response
from flask import request
from flask import url_for
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
auth = HTTPBasicAuth()

tasks = [
    {
        'id': 1,
        'title': 'Buy groceries',
        'description': 'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': 'Learn Python',
        'description': 'Need to find a good python tutorial on the web',
        'done': False
    }
]


# Routing by Flask.
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    """Routing to todo web service to retrieve the `tasks` resource."""
    retrieved_tasks = []
    for task in tasks:
        retrieved_tasks.append(make_public_task(task))
    return jsonify({'tasks': retrieved_tasks})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Retrieving the `task` resource given by a specific task_id value."""
    if len(tasks):
        for task in tasks:
            if task['id'] == task_id:
                task_retrieved = task
                return jsonify({'task': task_retrieved})

    abort(404)


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    """Creates a new `task` resource through a request from the user."""
    if not request.json or 'title' not in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return (jsonify({'task': task}), 201)


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Updates the content of a `task` resource."""
    if len(tasks):
        for task in tasks:
            if task['id'] == task_id:
                task_retrieved = task
    elif not len(tasks):
        abort(404)

    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) is not unicode:
        abort(400)
    if ('description' in request.json and
            type(request.json['description']) is not unicode):
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)

    task_retrieved['title'] = request.json.get('title',
                                               task_retrieved['title'])
    task_retrieved['description'] = request.json.get(
                                               'description',
                                               task_retrieved['description'])
    task_retrieved['done'] = request.json.get('done',
                                              task_retrieved['done'])
    return jsonify({'task': task_retrieved})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Deleting the content of a certain `task` resource for a given id."""
    if len(tasks):
        for task in tasks:
            if task['id'] == task_id:
                tasks.remove(task)
                return (jsonify({'result': True}))
    abort(404)


# Authentication.
@auth.get_password
def get_password(username):
    """Obtains the password for a given user."""
    if username == 'emara':
        return 'python'
    return None


# Handling Errors.
@app.errorhandler(404)
def not_found(error):
    """Returns a 404 error response in a JSON format."""
    return make_response(jsonify({'error': 'Not found'}), 404)


@auth.error_handler
def unauthorized():
    """Returns a 401 error message for an unauthorized user in JSON Format."""
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


# Helper Functions.
def make_public_task(task):
    """A helper functionn to substitute the `id` key with a `uri` field."""
    new_task = {}
    for key in task:
        if key == 'id':
            new_task['uri'] = url_for('get_task',
                                      task_id=task['id'],
                                      _external=True)
        else:
            new_task[key] = task[key]
    return (new_task)


if __name__ == "__main__":
    app.run(debug=True)
