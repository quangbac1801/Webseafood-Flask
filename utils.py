from saleapp import app,db
from saleapp.models import DanhMuc,SanPham,User,GioHang,DonHang
import hashlib
from sqlalchemy import func


def laySanPham(id_danhmuc, tuKhoa, A_gia=None, Z_gia=None, page=1):
    products=db.session.query(SanPham)
    if id_danhmuc:
        products=products.filter(SanPham.id_danhmuc==(id_danhmuc))
    if tuKhoa:
        products = products.filter(SanPham.name.ilike(f"%{tuKhoa}%"))
    if A_gia:
        products=products.filter(SanPham.gia>=(A_gia))
    if Z_gia:
        products=products.filter(SanPham.gia<=(Z_gia)) 
    page_size=app.config['PAGE_SIZE']
    start=(page-1)*page_size
    end=start +page_size
    return products.slice(start,end).all()   


#Thêm người Dùng
def add_user(name, username, password, **kwargs):
    user_check = User.query.filter_by(username=username).first()

    if user_check:
        raise ValueError("Username đã tồn tại. Vui lòng chọn một username khác.")
    else:
        password_hash = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        user = User(
            name=name.strip(),
            username=username.strip(),
            password=password_hash,
            email=kwargs.get('email'),
            phone=kwargs.get('phone'),
            diachi=kwargs.get('diachi'),
            vaitro=kwargs.get('vaitro')
        )
        db.session.add(user)
        db.session.commit()



#Kiểm tra đăng nhập
def check_login(username, password):
    hash_password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(
        User.username == username.strip(),
        User.password == hash_password
    ).first()


###################Quản Lí Danh Mục############
def timKiemDanhMuc(id_danhmuc, tukhoa):
    dm=db.session.query(DanhMuc)
    if id_danhmuc:
        dm=dm.filter(DanhMuc.id_danhmuc==id_danhmuc)
    if tukhoa:
        dm=dm.filter(DanhMuc.name.ilike(f'%{tukhoa}%'))
    return dm

def layDanhMuc():
    danhmuc=DanhMuc.query.all()
    return danhmuc

def add_danhmuc(id_danhmuc, name):
    dm = DanhMuc(id_danhmuc=id_danhmuc, name=name)
    db.session.add(dm)
    db.session.commit()

def update_danhmuc(id_danhmuc, name):
    danh_muc = DanhMuc.query.get(id_danhmuc)
    danh_muc.name = name
    db.session.commit()

def delete_danhmuc(id_danhmuc):
    danh_muc=DanhMuc.query.get(id_danhmuc)
    db.session.delete(danh_muc)
    db.session.commit()

#############Quản lí Sản Phẩm ############
def timKiemSanPham(id_sanpham, tukhoa, masanpham):
    sp=db.session.query(SanPham)
    if id_sanpham:
        sp=sp.filter(SanPham.id_sanpham==id_sanpham)
    if tukhoa:
        sp=sp.filter(SanPham.name.ilike(f'%{tukhoa}%'))
    if masanpham:
        sp=sp.filter(SanPham.id_danhmuc==masanpham)
    return sp

def add_sanpham(id_sanpham, name, mota, gia, anh, id_danhmuc):
    sp=SanPham(id_sanpham=id_sanpham, name=name, mota=mota, gia=gia, anh=anh, id_danhmuc=id_danhmuc)
    db.session.add(sp)
    db.session.commit()

def update_sanpham(id_sanpham, name, mota, gia, anh, id_danhmuc):
    sp = SanPham.query.get(id_sanpham)
    sp.name = name
    sp.mota=mota
    sp.gia=gia
    sp.anh=anh
    sp.id_danhmuc=id_danhmuc
    db.session.commit()

def delete_sanpham(id_sanpham):
    sp = SanPham.query.get(id_sanpham)
    if sp:
        db.session.delete(sp)
        db.session.commit()

def demSanPham():
    return SanPham.query.count()

######Quản lý người dùng########
def timKiemNguoiDung(id_user, name, username):
    users = db.session.query(User)
    if id_user:
        users = users.filter(User.id_user == id_user)
    if name:
        users = users.filter(User.name.ilike(f'%{name}%'))
    if username:
        users = users.filter(User.username.ilike(f'%{username}%'))
    return users

def update_user(id_user, name, username, password, email, phone, diachi, vaitro):
    user = User.query.get(id_user)
    user.name=name,
    user.username=username,
    user.password=password,
    user.email=email,
    user.phone=phone,
    user.diachi=diachi,
    user.vaitro=vaitro
    db.session.commit()

def delete_user(id_user):
    user = User.query.get(id_user)
    db.session.delete(user)
    db.session.commit()


############Quản lý đơn hàng####
def timKiemDonHang(id_donhang):
    donhang = db.session.query(DonHang)
    if id_donhang:
        donhang = donhang.filter(DonHang.id_donhang == id_donhang)
    return donhang

def update_donhang(id_donhang, id_user, id_giohang, thanhtien, trangthai):
    donhang = DonHang.query.get(id_donhang)
    donhang.id_user=id_user,
    donhang.id_giohang=id_giohang,
    donhang.thanhtien=thanhtien,
    donhang.trangthai=trangthai
    db.session.commit()

def delete_donhang(id_donhang):
    donhang = DonHang.query.get(id_donhang)
    db.session.delete(donhang)
    db.session.commit()