from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))
    diachi = db.Column(db.String(250))
    vaitro = db.Column(db.String(10), default='user')
    active = db.Column(db.Boolean, default=True)
    ngaytao = db.Column(db.DateTime, default=datetime.now)
    ngaycapnhat = db.Column(db.DateTime, onupdate=datetime.now)

    def get_id(self):
        return str(self.id_user)
    def __str__(self):
        return self.name
    

class DanhMuc(db.Model):
    __tablename__ = 'danhmuc'
    id_danhmuc = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ngaytao = db.Column(db.DateTime, default=datetime.now)
    ngaycapnhat = db.Column(db.DateTime, onupdate=datetime.now)

    def __str__(self):
        return self.name


class SanPham(db.Model):
    __tablename__ = 'sanpham'
    id_sanpham = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mota = db.Column(db.String)
    gia = db.Column(db.Float, nullable=False)
    anh = db.Column(db.String(100))
    id_danhmuc = db.Column(db.Integer, db.ForeignKey('danhmuc.id_danhmuc'), nullable=False)
    ngaytao = db.Column(db.DateTime, default=datetime.now)
    ngaycapnhat = db.Column(db.DateTime, onupdate=datetime.now)

    danh_muc = db.relationship('DanhMuc', backref=db.backref('sanphams', lazy=True))

    def __str__(self):
        return self.name

class GioHang(db.Model):
    __tablename__ = 'giohang'
    id_giohang = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    id_sanpham = db.Column(db.Integer, db.ForeignKey('sanpham.id_sanpham'), nullable=False)
    soluong = db.Column(db.Integer, nullable=False)
    gia = db.Column(db.Float, nullable=False)
    thanhtien = db.Column(db.Float, nullable=False)
    tinhTrang = db.Column(db.String, default='chuathanhtoan')

    user = db.relationship('User', backref=db.backref('giohangs', lazy=True))
    product = db.relationship('SanPham', backref=db.backref('giohangs', lazy=True))



class DonHang(db.Model):
    __tablename__ = 'donhang'
    id_donhang = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    id_giohang= db.Column(db.Integer, db.ForeignKey('giohang.id_giohang'), nullable=False)
    thanhtien = db.Column(db.Float, nullable=False)
    trangthai=db.Column(db.String)
    ngaytao = db.Column(db.DateTime, default=datetime.now)
    ngaycapnhat = db.Column(db.DateTime, onupdate=datetime.now)

    user = db.relationship('User', backref=db.backref('donhangs', lazy=True))
    cart = db.relationship('GioHang', backref=db.backref('donhangs', lazy=True))

