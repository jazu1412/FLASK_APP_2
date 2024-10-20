let token = '';

async function register() {
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;

    try {
        const response = await fetch('http://localhost:8083/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();
        if (response.ok) {
            alert('Registration successful. Please login.');
        } else {
            alert(`Registration failed: ${data.message}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during registration.');
    }
}

async function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch('http://localhost:8083/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();
        if (response.ok) {
            token = data.token;
            document.getElementById('auth-section').style.display = 'none';
            document.getElementById('post-section').style.display = 'block';
            getPosts();
        } else {
            alert(`Login failed: ${data.message}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during login.');
    }
}

async function createPost() {
    const title = document.getElementById('post-title').value;
    const content = document.getElementById('post-content').value;

    try {
        const response = await fetch('http://localhost:8084/posts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify({ title, content }),
        });

        const data = await response.json();
        if (response.ok) {
            alert('Post created successfully.');
            document.getElementById('post-title').value = '';
            document.getElementById('post-content').value = '';
            getPosts();
        } else {
            alert(`Failed to create post: ${data.message}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while creating the post.');
    }
}

async function getPosts() {
    try {
        const response = await fetch('http://localhost:8084/posts', {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        const data = await response.json();
        if (response.ok) {
            const postsContainer = document.getElementById('posts-container');
            postsContainer.innerHTML = '';
            data.forEach(post => {
                const postElement = document.createElement('div');
                postElement.className = 'post';
                postElement.innerHTML = `
                    <h3>${post.title}</h3>
                    <p>${post.content}</p>
                `;
                postsContainer.appendChild(postElement);
            });
        } else {
            alert(`Failed to fetch posts: ${data.message}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while fetching posts.');
    }
}

// Initial call to get posts
getPosts();