# app.py
from flask import Flask, render_template, redirect, url_for, flash, request
from werkzeug.utils import secure_filename
from config import Config
from extensions import db  # Import db from extensions
from models import User, DataUpload
from forms import RegistrationForm, LoginForm, UploadForm
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)  # Initialize db with app
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=form.password.data,
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,
            height=form.height.data,
            weight=form.weight.data,
            gait_disorder=form.gait_disorder.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    uploads = DataUpload.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', uploads=uploads)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.data.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        upload = DataUpload(
            tag=form.tag.data,
            file_path=filename,
            data_type=form.data_type.data,
            additional_info=form.metadata.data,
            author=current_user
        )
        db.session.add(upload)
        db.session.commit()
        flash('Data uploaded successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('upload.html', form=form)

@app.route('/analysis/<int:data_id>')
@login_required
def analysis(data_id):
    dataset = DataUpload.query.get_or_404(data_id)
    return render_template('analysis.html', dataset=dataset)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
