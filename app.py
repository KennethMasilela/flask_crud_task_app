import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask app config
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback_dev_key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database and Migrations
db = SQLAlchemy(app)


# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    status = db.Column(db.String(20))
    due_date = db.Column(db.String(20))
    priority = db.Column(db.String(10))
    assigned_to = db.Column(db.String(100))
    category = db.Column(db.String(100))
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Routes
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    tasks = Task.query.filter_by(user_id=session['user_id']).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    new_task = Task(
        title=request.form['title'],
        description=request.form['description'],
        status=request.form['status'],
        due_date=request.form['due_date'],
        priority=request.form['priority'],
        assigned_to=request.form['assigned_to'],
        category=request.form['category'],
        notes=request.form['notes'],
        user_id=session['user_id']
    )
    db.session.add(new_task)
    db.session.commit()
    flash("Task added successfully!", "success")
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    if task.user_id != session.get('user_id'):
        flash("Unauthorized access", "danger")
        return redirect(url_for('index'))
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "danger")
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != session.get('user_id'):
        flash("Unauthorized access", "danger")
        return redirect(url_for('index'))

    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.status = request.form['status']
        task.due_date = request.form['due_date']
        task.priority = request.form['priority']
        task.assigned_to = request.form['assigned_to']
        task.category = request.form['category']
        task.notes = request.form['notes']
        db.session.commit()
        flash("Task updated successfully!", "info")
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)


@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    task = Task.query.get(id)
    task.title = request.form['title']
    task.description = request.form['description']
    task.status = request.form['status']
    task.due_date = request.form['due_date']
    task.priority = request.form['priority']
    task.assigned_to = request.form['assigned_to']
    task.category = request.form['category']
    task.notes = request.form['notes']

    db.session.commit()
    flash("Task updated successfully!", "info")
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash("Username already exists", "warning")
            return redirect(url_for('register'))
        hashed_pw = generate_password_hash(password)
        user = User(username=username, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Registered successfully!", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            session['username'] = user.username
            flash("Logged in!", "success")
            return redirect(url_for('index'))
        flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for('login'))

# Entry point
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
