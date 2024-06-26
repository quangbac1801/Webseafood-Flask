from saleapp import db, admin
from flask_admin.contrib.sqla import ModelView

from saleapp.models import *

class SanPhamview(ModelView):
    can_view_details = True
    can_export = True #xuất dữ liệu excel
    edit_modal = True
    details_modal = True
    column_searchable_list =["name"]
    column_filters = ["name","gia","danh_muc.name"]
    column_list = ['id_sanpham','name', 'mota', 'gia', 'anh', 'danh_muc.name', 'ngaytao', 'ngaycapnhat']
    column_labels = {
        'id_sanpham':'Mã',
        'name': 'Tên sản phẩm',
        'mota': 'Mô tả',
        'gia': 'Giá',
        'anh': 'Ảnh',
        'danh_muc.name': 'Danh mục',
        'ngaytao': 'Ngày tạo',
        'ngaycapnhat': 'Ngày cập nhật'
    }

class DanhMucview(ModelView):
    can_view_details = True
    can_export = True 
    edit_modal = True
    details_modal = True
    column_searchable_list =["name"]
    column_filters = ["name"]
    column_list = ['id_danhmuc','name','ngaytao','ngaycapnhat']
    column_labels = {
        'id_danhmuc':'Mã',
        'name': 'Tên danh mục',
        'ngaytao': 'Ngày tạo',
        'ngaycapnhat': 'Ngày cập nhật'
    }

class DonHangView(ModelView):
    column_list = ['user.name', 'user.diachi', 'user.phone', 'cart.product.name', 'thanhtien', 'trangthai', 'ngaytao', 'ngaycapnhat']
    column_labels = {
        'user.name': 'Tên khách hàng',
        'user.diachi': 'Địa chỉ',
        'user.phone': 'Số điện thoại',
        'cart.product.name': 'Tên sản phẩm',
        'thanhtien': 'Thành tiền',
        'trangthai': 'Trạng thái',
        'ngaytao': 'Ngày tạo',
        'ngaycapnhat': 'Ngày cập nhật'
    }

admin.add_view(ModelView(User, db.session))
admin.add_view(DanhMucview(DanhMuc, db.session, name='Danh Mục'))
admin.add_view(SanPhamview(SanPham, db.session, name='Sản Phẩm'))
admin.add_view(DonHangView(DonHang, db.session, name='Đơn Hàng'))