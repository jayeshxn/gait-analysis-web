# models.py
from datetime import datetime
from extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    gait_disorder = db.Column(db.String(10), nullable=False)
    uploads = db.relationship('DataUpload', backref='author', lazy=True)

class DataUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(150), nullable=False)
    data_type = db.Column(db.String(20), nullable=False)
    additional_info = db.Column(db.Text, nullable=True)  # Renamed from `metadata`
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
