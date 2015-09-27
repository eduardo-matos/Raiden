from uuid import uuid4
from flask import jsonify, request, render_template
from . import app, db, socketio
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

    socketio.emit('new_task', dict(title=task.title, slug=task.slug, item_count=task.item_count, current_count=0))
    return jsonify({'slug': task.slug, 'success': True, 'msg': ''})


@app.route('/progress-task/<slug>', methods=['POST'])
def progress_task(slug):
    try:
        current_count = int(request.form['current_count'])
        count = db.session.query(Task).filter(Task.slug == slug).update({Task.current_count: current_count})
        db.session.commit()

        socketio.emit('progress_task', dict(slug=slug, current_count=current_count))

        return jsonify(dict(success=True, current_count=current_count, updated=count))
    except ValueError:
        return jsonify(dict(success=False, msg="'current_count' should be an integer")), 400


@app.route('/tasks', methods=['GET'])
def tasks():
    return render_template('tasks.html')


@socketio.on('connect')
def on_connect():
    pass
