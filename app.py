from app import app
from flask import render_template, redirect, url_for
from flask_login import current_user

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('blog.blog'))
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html', title="About")

if __name__ == '__main__':
    app.run(debug=True)
