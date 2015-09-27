from flask import jsonify
from . import app, db
from .models import Task


@app.route('/api/tasks', methods=['GET'])
def api_tasks():
    tasks = [dict(title=task.title, item_count=task.item_count, current_count=task.current_count, slug=task.slug)
             for task in db.session.query(Task.title, Task.item_count, Task.current_count, Task.slug)]

    return jsonify({'data': tasks, 'success': True})
