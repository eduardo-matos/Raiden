from uuid import uuid4
from flask import jsonify, request
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
