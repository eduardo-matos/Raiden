from uuid import uuid4
from flask import jsonify, request, render_template
from . import app, db
from .models import Task


@app.route('/create-task', methods=['POST'])
def create_task():
    if not request.form.get('title'):
        return jsonify(dict(success=False, msg="'title' field is mandatory")), 400

    if not request.form.get('item_count'):
        return jsonify(dict(success=False, msg="'item_count' field is mandatory")), 400

    if not request.form['item_count'].isdigit():
        return jsonify(dict(success=False, msg="'item_count' should be an integer")), 400

    task = Task(title=request.form['title'], item_count=request.form['item_count'], slug=uuid4().hex)
    db.session.add(task)
    db.session.commit()

    return jsonify({'slug': task.slug, 'success': True, 'msg': ''})


@app.route('/progress-task/<slug>', methods=['POST'])
def progress_task(slug):
    try:
        current_count = int(request.form['current_count'])
        db.session.query(Task).filter(Task.slug == slug).update({Task.current_count: current_count})

        return jsonify(dict(success=True, current_count=current_count))
    except ValueError:
        return jsonify(dict(success=False, msg="'current_count' should be an integer")), 400


@app.route('/tasks', methods=['GET'])
def tasks():
    tasks_ = [(task[0], task.slug)
             for task in db.session.query((Task.current_count * 100 / Task.item_count), Task.slug)]
    return render_template('tasks.html', tasks=tasks_)
