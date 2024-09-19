import sqlite3
import logging
import cProfile
import io
import pstats
from flask import Flask, render_template, request, url_for, flash, redirect, g
from werkzeug.exceptions import abort

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['DATABASE'] = 'database.db'

def profile(fnc):
    """A decorator that uses cProfile to profile a function"""
    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval
    return inner

def get_db_connection():
    
    if app.config['TESTING']:
        # Use the test database connection
        conn = app.config['DB_CONNECTION']
    else:
        # Use a new connection for non-testing environments
        conn = sqlite3.connect(app.config['DATABASE'])
    
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def init_db(conn=None):
    if conn is None:
        conn = sqlite3.connect(app.config['DATABASE'])
    try:
        with app.open_resource('schema.sql', mode='r') as f:
            sql_script = f.read()
            logger.info("SQL script to be executed:")
            logger.info(sql_script)
            conn.executescript(sql_script)
        conn.commit()
        logger.info("Database initialized successfully")
        
        # Check if the table was created
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='posts';")
        table_exists = cursor.fetchone()
        if table_exists:
            logger.info("'posts' table created successfully")
        else:
            logger.error("Failed to create 'posts' table")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
    finally:
        if conn != app.config.get('DB_CONNECTION'):
            conn.close()

@app.route('/')
def index():
    logger.info("Accessing index route")
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    logger.info(f"Accessing post with id: {post_id}")
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    logger.info("Accessing create post route")
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            logger.info(f"Created new post: {title}")
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    logger.info(f"Accessing edit route for post id: {id}")
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            logger.info(f"Updated post with id: {id}")
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    logger.info(f"Deleting post with id: {id}")
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True, host='0.0.0.0', port=5009)
    logger.info("Flask application has shut down")
