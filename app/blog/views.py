from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app.blog.forms import PostForm
from app.models import Post
from app import db

posts = [
    {
        'author': 'Shashank',
        'title': 'How to make a Website',
        'date_posted': '12 April, 2019',
        'content': 'This is a post for creating a website.'
    }
]

blog_blueprint = Blueprint('blog', __name__, template_folder='templates/blog')

@blog_blueprint.route('/')
@login_required
def blog():
    blog_posts = Post.query.all()
    return render_template('blogs.html', title='Blogs', posts=blog_posts)

@blog_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def add():
    form = PostForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        user_id = current_user.id
        post = Post(title, content, user_id)

        db.session.add(post)
        db.session.commit()

        flash('Your new post has been added successfully', 'success')
        return redirect(url_for('blog.blog'))

    return render_template('add.html', title='New Post', form=form, header="Add New Post")

@blog_blueprint.route('/post/<post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@blog_blueprint.route('/post/<post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.users != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        db.session.add(post)
        db.session.commit()

        flash('Your post has been updated successfully.', 'success')
        return redirect(url_for('blog.post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('add.html', title='Update Post', form=form, header="Update Your Post", post=post)
