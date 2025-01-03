import math

from flask import render_template, request, redirect, session, jsonify
import dao, utils
from app import app, login
from flask_login import login_user,logout_user
from app.models import UserRole


@app.route('/')
def index():

    page = request.args.get('page', 1, type=int)
    kw = request.args.get('kw')
    cate_id = request.args.get('category_id')
    books = dao.load_books(kw=kw, page=int(page), cate_id=cate_id)

    page_size = app.config['PAGE_SIZE']
    total = dao.count_books()

    return render_template('index.html', books=books, page=math.ceil(total/page_size))

@app.route('/register', methods=['GET', 'POST'])
def register_view():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if not password.__eq__(confirm):
            err_msg = 'Mật khẩu không khớp!!'
        else:
            data = request.form.copy()

            del data['confirm']
            avatar = request.files.get('avatar')
            dao.add_user(avatar=avatar, **data)
            return redirect("/login")


    return render_template('register.html', err_msg=err_msg)

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            next = request.args.get('next')
            return redirect('/' if next is None else next)

    return render_template('login.html')

@app.route('/login-admin', methods=['POST'])
def login_admin_view():
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password, role=UserRole.ADMIN)

        if user:
            login_user(user=user)

        return redirect("/admin")

@app.route('/logout')
def logout():
    logout_user()
    return redirect("/login")


@app.route('/api/carts', methods=['POST'])
def add_cart_view():
    cart = session.get('cart')
    if not cart:
        cart = {}

    id = str(request.json.get('id'))

    name = request.json.get('name')
    price = request.json.get('price')

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1
        }

    session['cart'] = cart

    return jsonify(utils.cart_stats(cart))

@app.route('/api/carts/<book_id>', methods=['put'])
def update_cart(book_id):
    quantity = int(request.json.get('quantity',0))

    cart = session.get('cart')
    if cart and book_id in cart:
        cart[book_id]['quantity'] = int(quantity)

    session['cart'] = cart
    return jsonify(utils.cart_stats(cart))


@app.route('/api/carts/<book_id>', methods=['delete'])
def delete_cart(book_id):
    cart = session.get('cart')
    if cart and book_id in cart:
        del cart[book_id]

    session['cart'] = cart
    return jsonify(utils.cart_stats(cart))

@app.route('/api/pay', methods=['post'])
def pay():
    cart = session.get('cart')
    try:
        dao.add_receipt(cart)
    except Exception as ex:
        return jsonify({'status':500, 'msg': str(ex)})
    else:
        del session['cart']
        return jsonify({'status':200,'msg':'successfull'})

@app.route('/carts')
def cart_view():
    return render_template('cart.html')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)

@app.context_processor
def common_response_data():
    return {
        'categories': dao.load_categories(),
        'cart_stats': utils.cart_stats(session.get('cart'))
    }

if __name__ == '__main__':
    with app.app_context():
        from app import admin
        app.run(debug=True)
