// API Base URL
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Simple API fetching utility
const api = {
    async get(endpoint) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`);
            const data = await response.json();
            return { data, ok: response.ok, status: response.status };
        } catch (error) {
            console.error('API GET Error:', error);
            return { data: null, ok: false, status: 0 };
        }
    },

    async post(endpoint, data, token = null) {
        try {
            const headers = { 'Content-Type': 'application/json' };
            if (token) headers['Authorization'] = `Token ${token}`;

            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(data)
            });
            const responseData = await response.json();
            return { data: responseData, ok: response.ok, status: response.status };
        } catch (error) {
            console.error('API POST Error:', error);
            return { data: null, ok: false, status: 0 };
        }
    },

    async put(endpoint, data, token = null) {
        try {
            const headers = { 'Content-Type': 'application/json' };
            if (token) headers['Authorization'] = `Token ${token}`;

            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'PUT',
                headers: headers,
                body: JSON.stringify(data)
            });
            const responseData = await response.json();
            return { data: responseData, ok: response.ok, status: response.status };
        } catch (error) {
            console.error('API PUT Error:', error);
            return { data: null, ok: false, status: 0 };
        }
    },

    async delete(endpoint, token = null) {
        try {
            const headers = {};
            if (token) headers['Authorization'] = `Token ${token}`;

            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'DELETE',
                headers: headers
            });
            return { ok: response.ok, status: response.status };
        } catch (error) {
            console.error('API DELETE Error:', error);
            return { ok: false, status: 0 };
        }
    }
};

// Toast Utility
const showToast = (message, type = 'success') => {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
};

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('BlogHive Frontend Initialized');

    // Update Navigation based on Auth State
    const updateNav = () => {
        const token = localStorage.getItem('bloghive_token');
        const navLinks = document.querySelector('.nav-links');
        const heroBtn = document.getElementById('hero-action-btn');

        if (token) {
            const userJson = localStorage.getItem('bloghive_user');
            const user = userJson ? JSON.parse(userJson) : { username: 'User' };

            if (navLinks) {
                navLinks.innerHTML = `
                        <li><a href="index.html">Home</a></li>
                        <li><a href="view-blogs.html">Blogs</a></li>
                        <li><a href="categories.html">Categories</a></li>
                        <li><a href="create-blog.html" class="btn-primary">Create Blog</a></li>
                        <li><a href="#" id="logout-btn">Logout (${user.username || 'User'})</a></li>
                    `;

                document.getElementById('logout-btn').addEventListener('click', (e) => {
                    e.preventDefault();
                    localStorage.removeItem('bloghive_token');
                    localStorage.removeItem('bloghive_user');
                    showToast('Logged out successfully!');
                    setTimeout(() => window.location.href = 'index.html', 800);
                });
            }

            if (heroBtn) {
                heroBtn.innerText = 'Read Blogs';
                heroBtn.href = 'view-blogs.html';
            }
        }
    };

    updateNav();

    // Check if on login page
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            const { data, ok } = await api.post('/login/', { username, password });
            if (ok && data.token) {
                localStorage.setItem('bloghive_token', data.token);
                localStorage.setItem('bloghive_user', JSON.stringify(data.user));
                showToast('Login successful! Redirecting...');
                setTimeout(() => window.location.href = 'index.html', 800);
            } else {
                let errorMsg = 'Login failed.';
                if (data && data.error) errorMsg = data.error;
                showToast(errorMsg, 'error');
            }
        });
    }

    // Check if on register page
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const firstName = document.getElementById('first_name')?.value || '';
            const lastName = document.getElementById('last_name')?.value || '';
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            const { data, ok } = await api.post('/register/', {
                username,
                email,
                password,
                first_name: firstName,
                last_name: lastName
            });

            if (ok && data.username) {
                showToast('Registration successful! Redirecting to login...');
                setTimeout(() => window.location.href = 'login.html', 1500);
            } else {
                let errorMsg = 'Registration failed.';
                if (data && typeof data === 'object') {
                    const firstError = Object.values(data)[0];
                    errorMsg = Array.isArray(firstError) ? firstError[0] : firstError;
                }
                showToast(errorMsg, 'error');
            }
        });
    }

    // Populate Category Dropdowns
    const populateCategories = async () => {
        const categorySelects = document.querySelectorAll('#category');
        if (categorySelects.length === 0) return;

        const { data, ok } = await api.get('/categories/');
        if (ok && data) {
            categorySelects.forEach(select => {
                const currentValue = select.value;
                select.innerHTML = '<option value="">Select a category</option>' +
                    data.map(cat => `<option value="${cat.id}" ${currentValue == cat.id ? 'selected' : ''}>${cat.name}</option>`).join('');
            });
        }
    };

    populateCategories();

    // Check if on create blog page
    const createBlogForm = document.getElementById('create-blog-form');
    if (createBlogForm) {
        createBlogForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const title = document.getElementById('title').value;
            const category = document.getElementById('category').value;
            const content = document.getElementById('content').value;
            const tagsInput = document.getElementById('tags')?.value || '';
            const tags = tagsInput.split(',').map(tag => tag.trim()).filter(tag => tag !== '');
            const token = localStorage.getItem('bloghive_token');

            if (!token) {
                showToast('You must be logged in to create a blog.', 'error');
                setTimeout(() => window.location.href = 'login.html', 1500);
                return;
            }

            const { data, ok } = await api.post('/blogs/', {
                title,
                category,
                content,
                tags,
                status: 'published'
            }, token);

            if (ok && data.id) {
                showToast('Blog published successfully!');
                setTimeout(() => window.location.href = 'index.html', 1500);
            } else {
                showToast('Failed to publish blog. Please try again.', 'error');
            }
        });
    }

    // List Blogs on Home and View-Blogs page
    const blogList = document.getElementById('blog-container') || document.getElementById('blog-list');
    if (blogList) {
        const loadBlogs = async () => {
            const urlParams = new URLSearchParams(window.location.search);
            const catSlug = urlParams.get('category');
            const tagSlug = urlParams.get('tag');

            let endpoint = '/blogs/';
            if (catSlug) endpoint = `/blogs/?category=${catSlug}`;
            else if (tagSlug) endpoint = `/blogs/?tag=${tagSlug}`;

            const { data, ok } = await api.get(endpoint);

            if (ok && data.length > 0) {
                blogList.innerHTML = data.map(blog => `
                    <div class="blog-card">
                        <div class="content">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                <span class="category">${blog.category_name || 'General'}</span>
                                <div style="display: flex; gap: 5px; flex-wrap: wrap;">
                                    ${(blog.tag_names || []).map(tag => `<a href="view-blogs.html?tag=${tag}" style="font-size: 0.7rem; background: #e0e7ff; color: #4338ca; padding: 2px 8px; border-radius: 12px; text-decoration: none; font-weight: 600;">#${tag}</a>`).join('')}
                                </div>
                            </div>
                            <h3>${blog.title}</h3>
                            <p>${blog.content.substring(0, 120)}...</p>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
                                <a href="blog-detail.html?slug=${blog.slug}" class="read-more" style="color:var(--primary-color); font-weight:600; text-decoration:none;">Read More →</a>
                                ${localStorage.getItem('bloghive_token') ? `
                                    <div style="display: flex; gap: 10px;">
                                        <a href="edit-blog.html?slug=${blog.slug}" style="color: var(--text-muted); text-decoration: none; font-size: 0.8rem;">Edit</a>
                                        <a href="#" class="delete-blog" data-slug="${blog.slug}" style="color: #ef4444; text-decoration: none; font-size: 0.8rem;">Delete</a>
                                    </div>
                                ` : ''}
                            </div>
                        </div>
                    </div>
                `).join('');

                // Add delete listeners
                document.querySelectorAll('.delete-blog').forEach(btn => {
                    btn.addEventListener('click', async (e) => {
                        e.preventDefault();
                        const slug = e.target.dataset.slug;
                        if (confirm(`Are you sure you want to delete the blog "${slug}"?`)) {
                            const token = localStorage.getItem('bloghive_token');
                            const success = await api.delete(`/blogs/${slug}/`, token);
                            if (success) {
                                showToast('Blog deleted successfully!');
                                loadBlogs();
                            } else {
                                showToast('Failed to delete blog. You might not have permission.', 'error');
                            }
                        }
                    });
                });
            } else if (data) {
                blogList.innerHTML = '<p style="grid-column: 1/-1; text-align: center;">No blogs found matching this category.</p>';
            }
        };
        loadBlogs();
    }

    // Check if on edit blog page
    const editBlogForm = document.getElementById('edit-blog-form');
    if (editBlogForm) {
        const urlParams = new URLSearchParams(window.location.search);
        const slug = urlParams.get('slug');

        const loadBlogData = async () => {
            const { data, ok } = await api.get(`/blogs/${slug}/`);
            if (ok && data) {
                document.getElementById('title').value = data.title;
                document.getElementById('category').value = data.category || '';
                document.getElementById('content').value = data.content;
                const tagsInput = document.getElementById('tags');
                if (tagsInput && data.tag_names) {
                    tagsInput.value = data.tag_names.join(', ');
                }
            }
        };

        if (slug) {
            const initEdit = async () => {
                await populateCategories();
                await loadBlogData();
            };
            initEdit();
        }

        editBlogForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const title = document.getElementById('title').value;
            const category = document.getElementById('category').value;
            const content = document.getElementById('content').value;
            const tagsInput = document.getElementById('tags')?.value || '';
            const tags = tagsInput.split(',').map(tag => tag.trim()).filter(tag => tag !== '');
            const token = localStorage.getItem('bloghive_token');

            const { data, ok } = await api.put(`/my-blogs/${slug}/`, {
                title,
                category,
                content,
                tags,
                status: 'published'
            }, token);

            if (ok && data.id) {
                showToast('Blog updated successfully!');
                setTimeout(() => window.location.href = 'view-blogs.html', 1500);
            } else {
                showToast('Failed to update blog.', 'error');
            }
        });
    }

    // Check if on blog detail page
    const blogDetailContent = document.getElementById('blog-detail-content');
    const commentsList = document.getElementById('comments-list');
    const commentFormContainer = document.getElementById('comment-form-container');
    const loginToComment = document.getElementById('login-to-comment');

    if (blogDetailContent) {
        const urlParams = new URLSearchParams(window.location.search);
        const slug = urlParams.get('slug');
        let currentBlogId = null;

        const loadComments = async (blogSlug) => {
            const { data, ok } = await api.get(`/comments/?blog=${blogSlug}`);
            if (ok && data) {
                if (data.length === 0) {
                    commentsList.innerHTML = '<p style="color: var(--text-muted); font-style: italic;">No comments yet. Be the first to share your thoughts!</p>';
                } else {
                    commentsList.innerHTML = data.map(comment => `
                        <div style="background: #fff; padding: 20px; border-radius: 12px; margin-bottom: 15px; border: 1px solid #f1f5f9; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                <strong>${comment.user_name}</strong>
                                <span style="font-size: 0.8rem; color: var(--text-muted);">${new Date(comment.created_at).toLocaleDateString()}</span>
                            </div>
                            <p style="color: #475569;">${comment.content}</p>
                        </div>
                    `).join('');
                }
            }
        };

        const loadBlogDetail = async () => {
            const { data, ok } = await api.get(`/blogs/${slug}/`);
            if (ok && data) {
                currentBlogId = data.id;
                document.title = `${data.title} | BlogHive`;
                blogDetailContent.innerHTML = `
                    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; align-items: center;">
                        <span class="category" style="background: #e0e7ff; color: var(--primary-color); padding: 5px 15px; border-radius: 20px; font-weight: 600;">${data.category_name || 'General'}</span>
                        ${(data.tag_names || []).map(tag => `<a href="view-blogs.html?tag=${tag}" style="background: #e0e7ff; color: #4338ca; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; text-decoration: none;">#${tag}</a>`).join('')}
                    </div>
                    <h1 style="font-size: 3rem; margin-bottom: 20px; line-height: 1.1;">${data.title}</h1>
                    <div style="display: flex; align-items: center; gap: 15px; color: var(--text-muted); margin-bottom: 40px; font-size: 0.9rem;">
                        <span>By <strong>${data.author_name}</strong></span>
                        <span>•</span>
                        <span>${new Date(data.created_at).toLocaleDateString()}</span>
                    </div>
                    <div style="font-size: 1.2rem; line-height: 1.8; color: #334155;">
                        ${data.content.split('\n').map(p => p.trim() ? `<p style="margin-bottom: 25px;">${p}</p>` : '').join('')}
                    </div>
                `;

                // Handle comments visibility
                const token = localStorage.getItem('bloghive_token');
                if (token) {
                    commentFormContainer.style.display = 'block';
                    loginToComment.style.display = 'none';
                }

                loadComments(slug);
            } else {
                blogDetailContent.innerHTML = `<p style="text-align: center;">Blog not found.</p>`;
            }
        };

        const commentForm = document.getElementById('comment-form');
        if (commentForm) {
            commentForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const content = document.getElementById('comment-content').value;
                const token = localStorage.getItem('bloghive_token');

                if (!token) {
                    showToast('Please login to comment', 'error');
                    return;
                }

                const { data, ok } = await api.post('/comments/', {
                    blog: currentBlogId,
                    content: content
                }, token);

                if (ok) {
                    showToast('Comment posted!');
                    document.getElementById('comment-content').value = '';
                    loadComments(slug);
                } else {
                    showToast('Failed to post comment', 'error');
                }
            });
        }

        if (slug) {
            loadBlogDetail();
        } else {
            blogDetailContent.innerHTML = `<p style="text-align: center;">Invalid blog slug.</p>`;
        }
    }

    // Load Categories on Categories page
    const categoryGrid = document.getElementById('category-grid');
    if (categoryGrid) {
        const loadCategories = async () => {
            const { data, ok } = await api.get('/categories/');
            if (ok && data && data.length > 0) {
                categoryGrid.innerHTML = data.map(cat => `
                    <a href="view-blogs.html?category=${cat.slug}" class="category-card">
                        <h3>${cat.name}</h3>
                        <p>${cat.description || 'Explore stories in ' + cat.name}</p>
                    </a>
                `).join('');
            }
        };
        loadCategories();

        // Add Category Logic
        const token = localStorage.getItem('bloghive_token');
        const addCategoryAction = document.getElementById('add-category-action');
        const showAddBtn = document.getElementById('show-add-category-btn');
        const modal = document.getElementById('add-category-modal');
        const closeBtn = document.getElementById('close-modal-btn');
        const addForm = document.getElementById('add-category-form');

        if (token && addCategoryAction) {
            addCategoryAction.style.display = 'block';
        }

        if (showAddBtn) {
            showAddBtn.addEventListener('click', () => modal.style.display = 'flex');
        }

        if (closeBtn) {
            closeBtn.addEventListener('click', () => modal.style.display = 'none');
        }

        if (addForm) {
            addForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const name = document.getElementById('cat-name').value;
                const description = document.getElementById('cat-description').value;

                const { data, ok } = await api.post('/categories/', {
                    name,
                    description
                }, token);

                if (ok && data.id) {
                    showToast('Category created successfully!');
                    modal.style.display = 'none';
                    addForm.reset();
                    loadCategories();
                } else {
                    showToast('Failed to create category. Please try again.', 'error');
                }
            });
        }
    }

    // Load Tags on Tags page
    const tagGrid = document.getElementById('tag-grid');
    if (tagGrid) {
        const loadTags = async () => {
            const { data, ok } = await api.get('/tags/');
            if (ok && data && data.length > 0) {
                tagGrid.innerHTML = data.map(tag => `
                    <a href="view-blogs.html?tag=${tag.name}" class="tag-card">
                        <h3>#${tag.name}</h3>
                    </a>
                `).join('');
            } else if (ok) {
                tagGrid.innerHTML = '<p style="grid-column: 1/-1; text-align: center;">No tags found.</p>';
            }
        };
        loadTags();
    }

});
