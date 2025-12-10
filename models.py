# models.py
# Defines SQLAlchemy database models for the Contact Book application
from extensions import db

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # 收藏功能
    is_favorite = db.Column(db.Boolean, default=False)
    
    # 级联删除：删人时，自动把该人的电话也删了
    methods = db.relationship('ContactMethod', backref='contact', lazy=True, cascade="all, delete-orphan")

class ContactMethod(db.Model):
    __tablename__ = 'contact_methods'
    id = db.Column(db.Integer, primary_key=True)
    method_type = db.Column(db.String(50), nullable=False) # 手机/邮箱/微信
    value = db.Column(db.String(100), nullable=False)      # 具体号码
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
