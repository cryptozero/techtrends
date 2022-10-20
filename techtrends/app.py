import sqlite3
import logging

from webbrowser import get

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# Function to get a database connection.
# This function connects to database with the name `database.db`

def set_db_connection_count(connection):
    connection.execute('UPDATE metrics SET value = value+1 WHERE id = ? LIMIT 1',('db_connection_count',))
    connection.commit()

def get_db_connection_count(connection: sqlite3.Connection ):
    db_connection_count = connection.execute('SELECT value FROM metrics WHERE id= ?',('db_connection_count',)).fetchone()
    return db_connection_count['value']

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    set_db_connection_count(connection)
    return connection

# Function to get a post using its ID


def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                              (post_id,)).fetchone()
    connection.close()
    return post

def get_post_count():
    connection = get_db_connection()
    post_count = connection.execute('SELECT COUNT() FROM posts').fetchone()
    connection.close()
    return post_count[0]  

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application


@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.info(f'Not found article: returning 404')
        return render_template('404.html'), 404
    else:
        app.logger.info(f'Retrieved post: { post["title"] }')
        return render_template('post.html', post=post)

# Define the About Us page


@app.route('/about')
def about():
    app.logger.info(f'Retrieved page: About Us')
    return render_template('about.html')

# Define the post creation functionality


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                               (title, content))
            connection.commit()
            connection.close()

            app.logger.info(f'New article created: { title }')

            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/healthz')
def healthz():
    response = app.response_class(
        response=json.dumps({"result": "OK - healthy"}),
        status=200,
        mimetype='application/json'
    )
    app.logger.info('Healthz request successfull')
    return response

# get_db_connection_count includes the connections to sqlite db for the healthz an metrics endpoints

@app.route('/metrics')
def metrics():
    metrics={}
    metrics['post_count'] = get_post_count()
    connection=get_db_connection()
    metrics['db_connection_count'] = get_db_connection_count(connection)
    connection.close()
    response = app.response_class(
        response=json.dumps(metrics),
        status=200,
        mimetype='application/json'
    )
    app.logger.info('Metrics request successfull')
    return response


# start the application on port 3111
if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', port='3111')
