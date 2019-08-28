from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('groupe', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, titre, description, commentaire, groupe_id, username'
        ' FROM groupe p JOIN user u ON p.groupe_id = u.id'
        # ' ORDER BY created DESC'
    ).fetchall()
    return render_template('groupe/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']
        commentaire = request.form['commentaire']
        error = None

        if not titre:
            error = 'Mettre un titre.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (titre, description, commentaire, groupe_id)'
                ' VALUES (?, ?, ?)',
                (titre, description, commentaire, g.user['id'])
            )
            db.commit()
            return redirect(url_for('groupe.index'))

    return render_template('groupe/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, titre, description, commentaire, groupe_id, username'
        ' FROM groupe p JOIN user u ON p.groupe_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Groupe id {0} existe pas.".format(id))

    if check_author and post['groupe_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']
        commentaire = request.form['commentaire']
        error = None

        if not titre:
            error = 'Mettre un titre.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET titre = ?, description = ?, commentaire = ?'
                ' WHERE id = ?',
                (titre, description, commentaire, id)
            )
            db.commit()
            return redirect(url_for('groupe.index'))

    return render_template('groupe/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM groupe WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('groupe.index'))
