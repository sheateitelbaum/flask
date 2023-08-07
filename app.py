import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_mysqldb import MySQL
from werkzeug.exceptions import abort
import sqlalchemy as sa
import pandas as pd


def get_db_connection():
    # DEFINE THE DATABASE CREDENTIALS
    user = 'root'
    # password = 'password'
    host = 'localhost'
    port = 3306
    database = 'test'

    # PYTHON FUNCTION TO CONNECT TO THE MYSQL DATABASE AND
    # RETURN THE SQLACHEMY ENGINE OBJECT
    engine = sa.create_engine(
        url=f"mysql+pymysql://{user}@{host}:{port}/{database}"
    )

    return engine


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


def get_post(post_id):
    engine = get_db_connection()
    with engine.connect() as conn:
        post = conn.execute(sa.text(f'SELECT * FROM posts WHERE id = :post_id'), {'post_id': post_id}).fetchone()
        ## post = dict(row.rowproxy)
    # conn.close()
    print('posts', post)
    print('hello', type(post))
    if post is None:
        abort(404)
    return post

def get_time(time_id):
    engine = get_db_connection()
    with engine.connect() as conn:
        time = conn.execute(sa.text(f'SELECT * FROM times WHERE id = :time_id'), {'time_id': time_id}).fetchone()
        ## post = dict(row.rowproxy)
    # conn.close()

    if time is None:
        abort(404)
    return time


@app.route('/init')
def init():
    try:

        # GET THE CONNECTION OBJECT (ENGINE) FOR THE DATABASE
        engine = get_db_connection()
        print(
            f"Connection to the for user  created successfully.")
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)


@app.route('/')
def index():
    engine = get_db_connection()
    stmt = 'SELECT * FROM posts'
    with engine.connect() as conn:
        data = conn.execute(sa.text(stmt))
    print('posts', type(data))
    # conn.close()
    return render_template('index.html', posts=data)

@app.route('/times')
def times():
    engine = get_db_connection()
    stmt = 'SELECT * FROM times'
    with engine.connect() as conn:
        data = conn.execute(sa.text(stmt))
    print('posts', type(data))
    # conn.close()
    return render_template('times.html', times=data)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/time/<int:time_id>')
def time(time_id):
    time = get_time(time_id)
    return render_template('time.html', time=time)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            engine = get_db_connection()
            with engine.connect() as conn:
                conn.execute(sa.text(f'INSERT INTO posts (title, content) VALUES (:title , :content)'),
                             {'title': title, 'content': content})
                conn.commit()
                conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            engine = get_db_connection()
            with engine.connect() as conn:
                conn.execute(sa.text('UPDATE posts SET title = :title, content = :content WHERE id = :id'),
                             {'title': title, 'content': content, 'id': id})
                conn.commit()
                conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/edit_time', methods=('GET', 'POST'))
def edit_time(id):
    pass
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            engine = get_db_connection()
            with engine.connect() as conn:
                conn.execute(sa.text('UPDATE posts SET title = :title, content = :content WHERE id = :id'),
                             {'title': title, 'content': content, 'id': id})
                conn.commit()
                conn.close()
            return redirect(url_for('index'))

    return render_template('edit_time.html', post=post)


@app.route('/<int:id>/delete', methods=('GET', 'POST'))
def delete(id):
    post = get_post(id)
    print('type', type(post))

    engine = get_db_connection()
    with engine.connect() as conn:
        conn.execute(sa.text('DELETE FROM posts WHERE id = :id'), ({'id': id}))
        conn.commit()
        conn.close()

    flash(f"{post[2]} was successfully deleted!")
    return redirect(url_for('index'))


# @app.route('/<int:id>/loop', methods=('GET', 'POST'))
# def loop(id):
#     post = get_post(id)
#     for k,v in post:
#         print(k,v)
#
#     #flash(f"{post[2]} was successfully deleted!")
#     return redirect(url_for('index'))

@app.route('/import')
def import_csv():
    if request.method == 'POST':
        engine = get_db_connection()

        yt = pd.read_excel('yt.xlsx')
        yt.index.name = 'id'
        yt.to_sql('times', con=engine, if_exists='append', chunksize=1000, index=False)
    return render_template('import.html', post=post)
