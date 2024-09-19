import pytest
import sqlite3
from app import app, init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DATABASE'] = ':memory:'
    
    with app.app_context():
        conn = sqlite3.connect(app.config['DATABASE'])
        app.config['DB_CONNECTION'] = conn
        
        print("Setting up test database...")
        
        # Print the contents of schema.sql
        with app.open_resource('schema.sql', mode='r') as f:
            print("Contents of schema.sql:")
            print(f.read())
        
        # Initialize the database
        init_db(conn)
        
        # Check if the table was created
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in the database after init_db:", tables)
        
        # Add some test data
        try:
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         ('Test Post', 'This is a test post content'))
            conn.commit()
            print("Test data inserted successfully")
        except sqlite3.OperationalError as e:
            print(f"Error inserting test data: {e}")
        
        # Check tables again
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in the database after inserting test data:", tables)
        
        # Check if there's any data in the posts table
        try:
            cursor.execute("SELECT * FROM posts")
            posts = cursor.fetchall()
            print(f"Posts in the database: {posts}")
        except sqlite3.OperationalError as e:
            print(f"Error fetching posts: {e}")
    
    yield app.test_client()
    
    # Close the connection after the test
    conn.close()

def test_index_route(client):
    response = client.get('/')
    print(f"Response data: {response.data}")
    assert response.status_code == 200
    assert b'Welcome to FlaskBlog' in response.data
    assert b'Test Post' in response.data

def test_empty_db(client):
    with app.app_context():
        conn = app.config['DB_CONNECTION']
        conn.execute('DELETE FROM posts')
        conn.commit()
    
    response = client.get('/')
    print(f"Response data for empty db: {response.data}")
    assert b'No posts yet.' in response.data