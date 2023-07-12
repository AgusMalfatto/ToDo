from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from .auth import login_required
from .db import get_db

bp = Blueprint('todo', __name__)

@bp.route('/')
@login_required
def index():
    db, c = get_db()
    c.execute(
        'SELECT t.id, t.description, u.username, t.completed, t.created_at, t.priority, t.due_date FROM todo t JOIN user u ON t.created_by = u.id WHERE t.created_by = %s ORDER BY created_at DESC',
        (g.user['id'],)
    )
    todos = c.fetchall()

    return render_template('todo/index.html', todos=todos)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        description = request.form['description']
        priority = request.form.get('priority')
        dueDate = request.form.get('date')
        error = None

        if not description:
            error = 'Description is required'

        if error is not None:
            flash(error)    
        else:
            db, c = get_db()
            c.execute('insert into todo (description, completed, created_by, priority, due_date) values (%s, %s, %s, %s, %s)', (description, False, g.user['id'], priority, dueDate))
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('todo/create.html')
    
def get_todo(id):
    db, c = get_db()
    c.execute(
        'select t.id, t.description, t.completed, t.created_by, t.created_at, t.priority, t.due_date, u.username' 
        ' from todo t join user u on t.created_by = u.id where t.id = %s',
        (id,)
    )

    todo = c.fetchone()

    if todo is None:
        abort(404, "ToDo not exist")

    return todo

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    todo = get_todo(id)
    print(todo)

    if request.method == 'POST':
        description = request.form['description']
        completed = True if request.form.get('completed') == 'on' else False
        priority = request.form['priority']
        dueDate = request.form['date']
        error = None

        if not description:
            error = "Description is required"
        
        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute('update todo set description = %s, completed = %s, priority = %s, due_date = %s where id = %s and created_by = %s', (description,  completed, priority, dueDate, id, g.user['id']))
            db.commit()
            return redirect(url_for('todo.index'))
    return render_template('todo/update.html', todo=todo)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    db, c = get_db()
    c.execute('delete from todo where id = %s and created_by = %s', (id, g.user['id']))
    db.commit()
    return redirect(url_for('todo.index'))

@bp.route('/ordenar', methods=['POST'])
def ordenar():
    ordenamiento = request.form.get('ordenamiento')
    high = f"(select t.id, t.description, u.username, t.completed, t.created_at, t.priority, t.due_date from todo t JOIN user u on t.created_by = u.id where t.created_by = {g.user['id']} and t.priority = 'High' order by due_date desc)" 

    medium = f"(select t.id, t.description, u.username, t.completed, t.created_at, t.priority, t.due_date from todo t JOIN user u on t.created_by = u.id where t.created_by = {g.user['id']} and t.priority = 'Medium' order by due_date desc)"

    low = f"(select t.id, t.description, u.username, t.completed, t.created_at, t.priority, t.due_date from todo t JOIN user u on t.created_by = u.id where t.created_by = {g.user['id']} and t.priority = 'Low' order by due_date desc)"

    if ordenamiento == "HP":
        query = f"{high} UNION ALL {medium} UNION ALL {low}"
        return redirect(url_for('todo.order', query = query))
    
    query = f"{low} UNION ALL {medium} UNION ALL {high}"
    return redirect(url_for('todo.order', query = query))

@bp.route('/order/<query>')
def order(query):
    db, c = get_db()
    c.execute(query)
    todos = c.fetchall()

    return render_template('todo/index.html', todos=todos)

