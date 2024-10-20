from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import jwt
import os
from functools import wraps
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Content-Type", "Authorization"]}})
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mysecret')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, nullable=False)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            token = token.split()[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        except Exception as e:
            return jsonify({'message': f'Token is invalid! Error: {str(e)}'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/posts', methods=['GET', 'OPTIONS'])
def get_posts():
    if request.method == 'OPTIONS':
        return '', 204
    posts = Post.query.all()
    return jsonify([{'id': post.id, 'title': post.title, 'content': post.content, 'author_id': post.author_id} for post in posts])

@app.route('/posts/<int:post_id>', methods=['GET', 'OPTIONS'])
def get_post(post_id):
    if request.method == 'OPTIONS':
        return '', 204
    post = Post.query.get_or_404(post_id)
    return jsonify({'id': post.id, 'title': post.title, 'content': post.content, 'author_id': post.author_id})

@app.route('/posts', methods=['POST', 'OPTIONS'])
@token_required
def create_post():
    if request.method == 'OPTIONS':
        return '', 204
    data = request.get_json()
    new_post = Post(title=data['title'], content=data['content'], author_id=data['author_id'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'New post created!'}), 201

@app.route('/posts/<int:post_id>', methods=['PUT', 'OPTIONS'])
@token_required
def update_post(post_id):
    if request.method == 'OPTIONS':
        return '', 204
    post = Post.query.get_or_404(post_id)
    data = request.get_json()
    post.title = data['title']
    post.content = data['content']
    db.session.commit()
    return jsonify({'message': 'Post updated!'})

@app.route('/posts/<int:post_id>', methods=['DELETE', 'OPTIONS'])
@token_required
def delete_post(post_id):
    if request.method == 'OPTIONS':
        return '', 204
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted!'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8084)