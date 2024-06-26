import math
from sqlalchemy import func
from saleapp import app,login
from flask import flash, render_template,request,redirect,url_for
import saleapp.utils
from flask_login import current_user, login_user, logout_user,login_required
from saleapp.models import *
from saleapp.admin import *
# Trang chủ
@app.route("/")
def home():
    tuKhoa=request.args.get('tuKhoa')
    A_gia=request.args.get('A_gia')
    Z_gia=request.args.get('Z_gia')
    id_danhmuc=request.args.get('id_danhmuc')
    page=request.args.get('page', 1)
    counter=saleapp.utils.demSanPham()
    products=saleapp.utils.laySanPham(id_danhmuc=id_danhmuc, tuKhoa=tuKhoa, A_gia=A_gia, Z_gia=Z_gia, page=int(page))
    return render_template('index.html',
                           products=products,pages=math.ceil(counter/app.config['PAGE_SIZE']))


#Xem chi tiết sản phẩm
@app.route("/product/<id_sanpham>") 
def chiTietSanPham(id_sanpham):
    product=SanPham.query.get(id_sanpham)
    return render_template("chitietsanpham.html",product=product)


#Ghim trang nào cx có phần mmnu đầu
@app.context_processor
def menu():
    return {
        'danhmuc': saleapp.utils.layDanhMuc()
    }


#Đăng ký người dung
@app.route("/dangky", methods=['get', 'post'])
def dangky_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone=request.form.get('phone')
        diachi = request.form.get('diachi')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password.strip() == confirm.strip():
            saleapp.utils.add_user(name=name, diachi=diachi,
                                        username=username, password=password,
                                          email=email, phone=phone, confirm=confirm)
            flash('Đăng Ký Thành Công!', 'success')
        else:
            flash('Mật khẩu không khớp', 'danger')

    return render_template('register.html')



#Đăng Nhập
@app.route('/dangnhap', methods=['get','post'])
def dangnhap_user():
    err=''
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        user=saleapp.utils.check_login(username=username, password=password)
        if user:
            #trang thai dang nhap
            login_user(user=user)
            next=request.args.get('next','home')
            return redirect(url_for(next))
        else:
            err='Tài khoản hoặc mật khẩu không chính xác!!'
        
    return render_template('login.html',err=err)


@app.route('/dangxuat')
def dangxuat():
    logout_user()
    return redirect(url_for('dangnhap_user'))
@app.route('/admin/login', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login_admin.html')

#Trang cá nhân người dùng
@app.route('/profile')
def profile():
    user = current_user 
    donhangs = DonHang.query.filter_by(id_user=user.id_user).all() 
    return render_template('profile.html', user=user, donhangs=donhangs)


#Sửa thông tin dành cho người dùng
@app.route('/suataikhoan', methods=['get', 'post'])
def suataikhoan():
    id_user = request.args.get('id_user')
    user = User.query.get(id_user)
    if request.method == 'POST':
        id_user = user.id_user
        name=request.form.get('name')
        username=user.username
        password=user.password
        email=request.form.get('email')
        phone=request.form.get('phone')
        diachi=request.form.get('diachi')
        vaitro=user.vaitro
        saleapp.utils.update_user(id_user=id_user, name=name, username=username, password=password, email=email, phone=phone, diachi=diachi, vaitro=vaitro)
        flash('Đã cập nhật tài khoản thành công', 'success')
        return redirect(url_for('profile'))
    return render_template('suataikhoan.html', user=user)


#Tuwj goi khi dang nhap thanh cong
@login.user_loader
def user_load(id_user):
    return User.query.get(id_user)


#Trang giỏ hàng
@app.route('/giohang')
def gioHang():
    giohang_sp = GioHang.query.filter_by(id_user=current_user.id_user, tinhTrang='chuathanhtoan').all()
    tong_tien = sum(item.thanhtien for item in giohang_sp)
    return render_template('giohang.html', giohang_sp=giohang_sp, tong_tien=tong_tien)


#Thêm vào giỏ hàng
@app.route('/dat-hang', methods=['POST'])
@login_required
def dat_hang():
    id_sanpham = request.form.get('id_product')
    gia = request.form.get('gia')
    soluong = request.form.get('soluong', default=1)
    id_user = current_user.id_user
    tinhTrang="chuathanhtoan"  
    thanhtien = int(soluong) * float(gia)
    # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
    check_item = GioHang.query.filter_by(id_user=id_user, id_sanpham=id_sanpham, tinhTrang='chuathanhtoan').first()
    if check_item:
        check_item.soluong += int(soluong)
        check_item.thanhtien += thanhtien
    else:
        giohang = GioHang(id_user=id_user, id_sanpham=id_sanpham, soluong=soluong, gia=gia, thanhtien=thanhtien, tinhTrang=tinhTrang)
        db.session.add(giohang)
    db.session.commit()

    flash('Thêm vào giỏ hàng thành công!', 'success')
    return redirect(request.referrer)


#Xóa khỏi giỏ hàng
@app.route('/xoa-giohang', methods=['POST'])
def xoa_giohang():
    ds_items = request.form.getlist('select_items')
    for item_id in ds_items:
        giohang_item = GioHang.query.get(item_id)
        if giohang_item:
            db.session.delete(giohang_item)
    db.session.commit()
    flash('Đã xóa khỏi giỏ hàng!', 'info')
    return redirect(url_for('gioHang'))


#Chức năng thanh toán
@app.route("/thanhtoan", methods=['GET', 'POST'])
def thanhtoan():
    cart_nguoidung = GioHang.query.filter_by(id_user=current_user.id_user, tinhTrang='chuathanhtoan').all()
    if request.method == 'POST':
        donhang_info = {
            'id_user': current_user.id_user,
            'id_giohang': cart_nguoidung[0].id_giohang,
            'thanhtien': sum(item.thanhtien for item in cart_nguoidung),
            'trangthai': 'Chờ Xác Nhận',
            'ngaytao': datetime.now()
        }
        don_hang = DonHang(**donhang_info)
        db.session.add(don_hang)
        id_giohang_list = [item.id_giohang for item in cart_nguoidung]
        GioHang.query.filter(GioHang.id_giohang.in_(id_giohang_list)).update({'tinhTrang': "dathanhtoan"}, synchronize_session=False)
        db.session.commit()
        flash('Đặt hàng thành công!', 'success')
        return redirect(url_for('gioHang'))

    return render_template('thanhtoan.html', user_info=current_user, cart_nguoidung=cart_nguoidung)


#Trang admin
@app.route('/quantri', methods=['GET', 'POST'])
def quantri():
    sum_danhmuc=DanhMuc.query.count()
    sum_sanpham=SanPham.query.count()
    sum_donhang = DonHang.query.count()
    doanhso = db.session.query(func.sum(DonHang.thanhtien)).scalar() or 0
    if request.method == 'POST':
        thongke = request.form.get('thongke')
        kq = db.session.query(SanPham, DanhMuc).filter(
            SanPham.id_danhmuc == DanhMuc.id_danhmuc,
            db.or_(
                SanPham.name.ilike(f'%{thongke}%'),
                DanhMuc.name.ilike(f'%{thongke}%')
            )
        ).all()
        return render_template('quantri.html', sum_donhang=sum_donhang, doanhso=doanhso, kq=kq, thongke=thongke, sum_danhmuc=sum_danhmuc, sum_sanpham=sum_sanpham)
    return render_template('quantri.html', sum_donhang=sum_donhang, doanhso=doanhso, sum_danhmuc=sum_danhmuc, sum_sanpham=sum_sanpham)


###Quản lý danh muc###
@app.route('/quanlydanhmuc')
def quanlydanhmuc():
    id_danhmuc=request.args.get('id_danhmuc')
    tuKhoa=request.args.get('tuKhoa')
    danhmucs=saleapp.utils.timKiemDanhMuc(id_danhmuc=id_danhmuc, tukhoa=tuKhoa)
    return render_template('quanlydanhmuc.html', danhmucs=danhmucs)


@app.route('/themdanhmuc', methods=['get','post'])
def themDanhMuc():
    if request.method=='POST':
        id_danhmuc=request.form.get('id_danhmuc')
        name=request.form.get('name')
        existing_danhmuc = DanhMuc.query.filter_by(id_danhmuc=id_danhmuc).first()
        if existing_danhmuc:
            flash(f'Danh mục với Id Danh Mục={id_danhmuc} đã tồn tại', 'danger')
        else:
            saleapp.utils.add_danhmuc(id_danhmuc=id_danhmuc, name=name)
            flash('Đã thêm thành công', 'success')
            return redirect(url_for('themDanhMuc'))
    return render_template('add_danhmuc.html')


@app.route('/capnhatdanhmuc', methods=['get', 'post'])
def capNhatDanhMuc():
    id_danhmuc = request.args.get('id_danhmuc')
    danh_muc = DanhMuc.query.get(id_danhmuc)
    if request.method == 'POST':
        id_danhmuc = request.form.get('id_danhmuc')
        name = request.form.get('name')
        saleapp.utils.update_danhmuc(id_danhmuc=id_danhmuc, name=name)
        flash('Đã cập nhật danh mục thành công', 'success')
        return redirect(url_for('quanlydanhmuc'))
    
    return render_template('update_danhmuc.html',danh_muc=danh_muc)


@app.route('/xoadanhmuc', methods=['GET'])
def xoaDanhMuc():
    id_danhmuc = request.args.get('id_danhmuc')
    saleapp.utils.delete_danhmuc(id_danhmuc)
    flash('Đã xóa danh mục thành công', 'success')
    return redirect(url_for('quanlydanhmuc'))


###Quản lý Sản phẩm###
@app.route('/quanlysanpham')
def quanlysanpham():
    id_sanpham=request.args.get('id_sanpham')
    tuKhoa=request.args.get('tuKhoa')
    masanpham=request.args.get('masanpham')
    products=saleapp.utils.timKiemSanPham(id_sanpham=id_sanpham, tukhoa=tuKhoa, masanpham=masanpham)
    return render_template('quanlysanpham.html', products=products)


@app.route('/themsanpham', methods=['get','post'])
def themSanPham():
    danh_muc_list = DanhMuc.query.all()
    if request.method=='POST':
        id_sanpham=request.form.get('id_sanpham')
        name=request.form.get('name')
        mota=request.form.get('mota')
        gia=request.form.get('gia')
        anh=request.form.get('anh')
        id_danhmuc = request.form['id_danhmuc']
        existing_danhmuc = SanPham.query.filter_by(id_sanpham=id_sanpham).first()
        if existing_danhmuc:
            flash(f'Sản phẩm với Id ={id_sanpham} đã tồn tại', 'error')
        else:
            saleapp.utils.add_sanpham(id_sanpham=id_sanpham, name=name, mota=mota, gia=gia, anh=anh, id_danhmuc=id_danhmuc)
            flash('Đã thêm thành công', 'success')
            return redirect(url_for('themSanPham'))
    return render_template('add_sanpham.html',danh_muc_list=danh_muc_list)


@app.route('/capnhatsanpham', methods=['get', 'post'])
def capNhatSanPham():
    danh_muc_list = DanhMuc.query.all()
    id_sanpham = request.args.get('id_sanpham')
    sp = SanPham.query.get(id_sanpham)
    if request.method == 'POST':
        id_sanpham = request.form.get('id_sanpham')
        name = request.form.get('name')
        mota=request.form.get('mota')
        anh=request.form.get('anh')
        gia=request.form.get('gia')
        id_danhmuc = request.form['id_danhmuc']
        saleapp.utils.update_sanpham(id_sanpham=id_sanpham, name=name, mota=mota, gia=gia, anh=anh, id_danhmuc=id_danhmuc)
        flash('Đã cập nhật sản phẩm thành công', 'success')
        return redirect(url_for('quanlysanpham'))
    return render_template('update_sanpham.html', sp=sp, danh_muc_list=danh_muc_list)


@app.route('/xoasanpham', methods=['GET'])
def xoaSanPham():
    id_sanpham = request.args.get('id_sanpham')
    saleapp.utils.delete_sanpham(id_sanpham)
    flash('Đã xóa sản phẩm thành công', 'success')
    return redirect(url_for('quanlysanpham'))


###Quản lý người dùng###
@app.route('/quanlynguoidung')
def quanlynguoidung():
    id_user = request.args.get('id_user')
    name = request.args.get('name')
    username = request.args.get('username')
    users = saleapp.utils.timKiemNguoiDung(id_user=id_user, name=name, username=username)
    return render_template('quanlynguoidung.html', users=users)


@app.route('/capnhatnguoidung', methods=['get', 'post'])
def capNhatNguoiDung():
    id_user = request.args.get('id_user')
    user = User.query.get(id_user)
    if request.method == 'POST':
        id_user = request.form.get('id_user')
        name=request.form.get('name')
        username=request.form.get('username')
        password=request.form.get('password')
        email=request.form.get('email')
        phone=request.form.get('phone')
        diachi=request.form.get('diachi')
        vaitro=request.form.get('vaitro')
        saleapp.utils.update_user(id_user=id_user, name=name, username=username, password=password, email=email, phone=phone, diachi=diachi, vaitro=vaitro)
        flash('Đã cập nhật tài khoản thành công', 'success')
        return redirect(url_for('quanlynguoidung'))
    return render_template('update_user.html', user=user)


@app.route("/themtaikhoan", methods=['get', 'post'])
def add_taikhoan():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        diachi = request.form.get('diachi')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        vaitro = request.form.get('vaitro')
        if password.strip() == confirm.strip():
            saleapp.utils.add_user(name=name, diachi=diachi,
                                        username=username, password=password,
                                          email=email, phone=phone, confirm=confirm, vaitro=vaitro)
            flash('Thêm Tài Khoản Thành Công!', 'success')
        else:
            flash('Mật khẩu không khớp', 'danger')

    return render_template('add_user.html')


@app.route('/xoataikhoan', methods=['GET'])
def xoaTaiKhoan():
    id_user=request.args.get('id_user')
    saleapp.utils.delete_user(id_user)
    flash('Đã xóa tài khoản thành công', 'success')
    return redirect(url_for('quanlynguoidung'))


###Quản lý đơn hàng###
@app.route('/quanlydonhang')
def quanlydonhang():
    id_donhang = request.args.get('id_donhang')
    donhangs = saleapp.utils.timKiemDonHang(id_donhang=id_donhang)
    return render_template('quanlydonhang.html', donhangs=donhangs)
 

@app.route('/capnhatdonhang', methods=['get', 'post'])
def capNhatDonHang():
    id_donhang = request.args.get('id_donhang')
    donhang = DonHang.query.get(id_donhang)
    if request.method == 'POST':
        id_donhang = request.form.get('id_donhang')
        id_user=request.form.get('id_user')
        id_giohang=request.form.get('id_giohang')
        thanhtien=request.form.get('thanhtien')
        trangthai=request.form.get('trangthai')
        saleapp.utils.update_donhang(id_donhang=id_donhang, id_user=id_user, id_giohang=id_giohang, thanhtien=thanhtien, trangthai=trangthai)
        flash('Đã cập nhật đơn hàng thành công', 'success')
        return redirect(url_for('quanlydonhang'))
    return render_template('update_donhang.html', donhang=donhang)


@app.route('/xoadonhang', methods=['GET'])
def xoaDonHang():
    id_donhang = request.args.get('id_donhang')
    saleapp.utils.delete_donhang(id_donhang)
    flash('Đã xóa đơn hàng thành công', 'success')
    return redirect(request.referrer)

if __name__ == '__main__':
        app.run(debug=True)