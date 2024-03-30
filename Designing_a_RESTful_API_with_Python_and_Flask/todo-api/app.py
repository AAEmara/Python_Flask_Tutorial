#!flask/bin/python3
"""Creating a simple web application."""


from flask import Flask, jsonify, abort, make_response


app = Flask(__name__)


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


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    """Routing to todo web service to retrieve the `tasks` resource."""
    return jsonify({'tasks': tasks})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Retrieving the `tasks` resource given by a specific task_id value."""
    if len(tasks):
        for task in tasks:
            if task['id'] == task_id:
                task_retrieved = task
                return jsonify({'task': task_retrieved})

    abort(404)


@app.errorhandler(404)
def not_found(error):
    """Returns a 404 error response in a JSON format."""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(debug=True)
