from unicodedata import category

from app import db, app
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
import hashlib
from enum import Enum as RoleEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100), nullable=True)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref="user", lazy=True)

class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    books = relationship('Book', backref="category", lazy=True)

    def __str__(sefl):
        return sefl.name


class Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(1000), nullable=True)
    price = Column(Float, default=0)
    image = Column(String(200), nullable=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    detail = relationship('ReceiptDetails', backref="book", lazy=True)

class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    detail = relationship('ReceiptDetails', backref="receipt", lazy=True)

class ReceiptDetails(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # user = User(name="admin", username="admin", password=str(hashlib.md5("123456".encode("utf-8")).hexdigest()),
        #             avatar="https://res.cloudinary.com/dauhkaecb/image/upload/v1734619951/bookstore_ndloky.png",
        #             user_role=UserRole.ADMIN)

        # db.session.add(user)
        # db.session.commit()
        #
        # c1 = Category(name="Giáo trình")
        # c2 = Category(name="Truyện tranh")
        # c3 = Category(name ="Tiểu Thuyết")
        # c4 = Category(name="Sức khỏe")
        # c5 = Category(name="Khoa học - nghiên cứu")
        # c6 = Category(name="Mỹ thuật")
        # c7 = Category(name="Lịch sử")
        # c8 = Category(name="Truyền cảm hứng")
        # c9 = Category(name="Dạy nấu ăn")
        #
        # db.session.add_all([c1, c2, c3, c4, c5, c6, c7, c8, c9])
        # db.session.commit()
        #
        # data = [{
        #     "name": "Tư tưởng Hồ Chí Minh",
        #     "description": "aksjcbhiocnpa",
        #     "price": 70000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025509/tu_tuong_HCM_x7cap7.jpg",
        #     "category_id": 1
        # }, {
        #     "name": "Truyện Tấm Cám",
        #     "description": "ksdmfpsodfm",
        #     "price": 50000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025507/truyen2_gfkqgr.png",
        #     "category_id": 2
        # }, {
        #     "name": "Doraemon tập 150",
        #     "description": "anjdfnpk",
        #     "price": 30000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025506/truyen7_aewwce.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "Connan",
        #     "description": "dlsjbfidjs",
        #     "price": 30000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025486/conan_um7pjb.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "7 viên ngọc rồng",
        #     "description": "kdjfnlsdf",
        #     "price": 80000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025506/Truyen-tranh-Bay-vien-ngoc-rong_lz6kpw.webp",
        #     "category_id": 2
        # }, {
        #     "name": "Truyện Conan",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 60000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025506/truyen5_nxp9og.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "Túp lều Bác tom",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 70000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025494/tieu-thuyet2_cfhwfw.png",
        #     "category_id": 3
        # }, {
        #     "name": "Di tích lịch sử...",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 90000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025491/lichsu5_ewa4lg.webp",
        #     "category_id": 7
        # }, {
        #     "name": "Truyện Chú bé chăn cừu",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 20000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025506/Truyen3_kzfyag.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "Triết học Mác-Lênin",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 60000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025495/triet_hoc_Mac_s9pj2y.jpg",
        #     "category_id": 1
        # }, {
        #     "name": "Truyện Cổ tích Việt Nam",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 30000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025494/Truyen1_or2pen.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "Lập trình OOP",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 65000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025492/oop_umsngn.webp",
        #     "category_id": 1
        # }, {
        #     "name": "Toán cao cấp",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 50000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025493/toan_cao_cap_a4toiw.jpg",
        #     "category_id": 1
        # }, {
        #     "name": "Khải huyền muộn",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 55000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025494/tieu-thuyet3_w58t6p.jpg",
        #     "category_id": 7
        # }, {
        #     "name": "Tây Du Ký",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 75000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025493/tieu-thuyet4_l6mc66.png",
        #     "category_id": 7
        # }, {
        #     "name": "Bí mật dinh dưỡng",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 60000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025492/suc-khoe_mbjwzo.webp",
        #     "category_id": 4
        # }, {
        #     "name": "Truyện Cò và cáo",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 20000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025494/truyen_pnacrq.jpg",
        #     "category_id": 2
        # }, {
        #     "name": "Hiểu và thưởng thức...",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 120000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025492/Mythuat1_aqn3xp.jpg",
        #     "category_id": 6
        # }, {
        #     "name": "Luật hiến pháp",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 50000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025492/Luathienphap_cwgq9j.png",
        #     "category_id": 1
        # }, {
        #     "name": "Pháp luật đại cương",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 45000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025492/PLDC_xubcxn.jpg",
        #     "category_id": 1
        # }, {
        #     "name": "Đại Việt sử ký",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 96000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025491/lichsu2_ivxilj.jpg",
        #     "category_id": 7
        # }, {
        #     "name": "5 centimet trên giây",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 67000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025493/tieu-thuyet1_ehs5xn.jpg",
        #     "category_id": 3
        # }, {
        #     "name": "Lịch sử mỹ thuật VN",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 59000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025492/Mythuat2_tam5uf.png",
        #     "category_id": 6
        # }, {
        #     "name": "Chúa tể chiếc nhẫn",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 20000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025492/tieu-thuyet_v2utji.jpg",
        #     "category_id": 3
        # }, {
        #     "name": "PP nghiên cứu KH",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 150000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025491/nghien-cuu-khoa-hoc_lx7hvu.jpg",
        #     "category_id": 5
        # }, {
        #     "name": "PP nghiên cứu Y học",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 150000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025491/nghien-cuu-y-hoc_zcr7eu.webp",
        #     "category_id": 5
        # }, {
        #     "name": "Công chúa tóc cam",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 32000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025489/cong-chua-toc-cam_ijt3cb.webp",
        #     "category_id": 2
        # }, {
        #     "name": "Dinh dưỡng là chìa ...",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 50000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025489/dinh-duong_wqelod.jpg",
        #     "category_id": 4
        # }, {
        #     "name": "Món ăn Nhật",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 58000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025489/nauan5_lqjfhs.jpg",
        #     "category_id": 9
        # }, {
        #     "name": "Về nhà nấu cơm",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 320000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025489/nauan4_xq9lel.webp",
        #     "category_id": 9
        # }, {
        #     "name": "Hướng dẫn nấu 200 món",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 45000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025488/nauan3_vqzhjf.jpg",
        #     "category_id": 9
        # }, {
        #     "name": "500 món ăn ngon",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 67000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025487/nauan2_v2kyx1.webp",
        #     "category_id": 9
        # }, {
        #     "name": "Nghĩ giàu làm giàu",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 56000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025487/camhung2_lvdxgo.jpg",
        #     "category_id": 8
        # }, {
        #     "name": "Cơ thể tự chữa lành",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 49000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025487/C%C6%A1-Th%E1%BB%83-T%E1%BB%B1-Ch%E1%BB%AFa-L%C3%A0nh_ajxbiv.jpg",
        #     "category_id": 4
        # }, {
        #     "name": "Đọc dùm bạn các cách...",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 150000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025487/camhung3_opytxf.webp",
        #     "category_id": 8
        # }, {
        #     "name": "Hành thành mọi việc không hề khó",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 120000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025486/camhung4_koorbe.webp",
        #     "category_id": 8
        # }, {
        #     "name": "Đánh thức con người phi thường",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 110000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025485/camhung1_xss6nx.jpg",
        #     "category_id": 8
        # }, {
        #     "name": "555 món ăn Việt Nam",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 89000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025487/nauan1_iortv2.webp",
        #     "category_id": 9
        # }, {
        #     "name": "10 điều răn dành cho doanh nhân",
        #     "description": "aslkfnmdksfmsd",
        #     "price": 150000,
        #     "image": "https://res.cloudinary.com/dauhkaecb/image/upload/v1735025485/camhung6_ncbvsr.jpg",
        #     "category_id": 8
        # }]
        #
        # for p in data:
        #     book = Book(name=p['name'], description=p['description'], price=p['price'], image=p['image'], category_id=p['category_id'])
        #     db.session.add(book)
        #
        # db.session.commit()