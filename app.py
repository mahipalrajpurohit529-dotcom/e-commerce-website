from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from database import db, Product, Order, OrderItem, Customer, Category
from analytics import run_kmeans_analysis, get_dashboard_data
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', f"sqlite:///{os.path.join(basedir, 'instance', 'luxethreads.db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-change-me')

from flask_migrate import Migrate

db.init_app(app)
migrate = Migrate(app, db)

# ─── ROUTES ───────────────────────────────────────────────────

@app.route('/')
def index():
    featured = Product.query.filter_by(featured=True).limit(8).all()
    categories = Category.query.all()
    new_arrivals = Product.query.order_by(Product.id.desc()).limit(4).all()
    return render_template('index.html', featured=featured, categories=categories, new_arrivals=new_arrivals)

@app.route('/shop')
def shop():
    category_id = request.args.get('category')
    search = request.args.get('q', '')
    sort = request.args.get('sort', 'name')
    page = request.args.get('page', 1, type=int)

    query = Product.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.name)

    products = query.paginate(page=page, per_page=12)
    categories = Category.query.all()
    selected_category = Category.query.get(category_id) if category_id else None
    return render_template('shop.html', products=products, categories=categories,
                           selected_category=selected_category, search=search, sort=sort)

@app.route('/product/<int:pid>')
def product_detail(pid):
    product = Product.query.get_or_404(pid)
    related = Product.query.filter_by(category_id=product.category_id).filter(Product.id != pid).limit(4).all()
    return render_template('product.html', product=product, related=related)

@app.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    products = []
    total = 0
    for pid, qty in cart_items.items():
        p = Product.query.get(int(pid))
        if p:
            products.append({'product': p, 'qty': qty, 'subtotal': p.price * qty})
            total += p.price * qty
    return render_template('cart.html', products=products, total=total)

@app.route('/add-to-cart/<int:pid>', methods=['POST'])
def add_to_cart(pid):
    qty = int(request.form.get('qty', 1))
    cart = session.get('cart', {})
    cart[str(pid)] = cart.get(str(pid), 0) + qty
    session['cart'] = cart
    flash('Item added to cart!', 'success')
    return redirect(request.referrer or url_for('shop'))

@app.route('/remove-from-cart/<int:pid>')
def remove_from_cart(pid):
    cart = session.get('cart', {})
    cart.pop(str(pid), None)
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = session.get('cart', {})
    if not cart_items:
        return redirect(url_for('cart'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        phone = request.form.get('phone')

        customer = Customer.query.filter_by(email=email).first()
        if not customer:
            customer = Customer(name=name, email=email, address=address, phone=phone)
            db.session.add(customer)
            db.session.flush()

        total = 0
        order_items = []
        for pid, qty in cart_items.items():
            p = Product.query.get(int(pid))
            if p:
                total += p.price * qty
                order_items.append(OrderItem(product_id=p.id, quantity=qty, price=p.price))
                p.stock = max(0, p.stock - qty)

        order = Order(customer_id=customer.id, total=total,
                      status='confirmed', order_date=datetime.utcnow())
        db.session.add(order)
        db.session.flush()

        for item in order_items:
            item.order_id = order.id
            db.session.add(item)

        db.session.commit()
        session.pop('cart', None)
        flash(f'Order #{order.id} placed successfully!', 'success')
        return redirect(url_for('order_confirmation', oid=order.id))

    products = []
    total = 0
    for pid, qty in cart_items.items():
        p = Product.query.get(int(pid))
        if p:
            products.append({'product': p, 'qty': qty, 'subtotal': p.price * qty})
            total += p.price * qty
    return render_template('checkout.html', products=products, total=total)

@app.route('/order/<int:oid>')
def order_confirmation(oid):
    order = Order.query.get_or_404(oid)
    return render_template('order_confirmation.html', order=order)

# ─── ANALYTICS DASHBOARD ──────────────────────────────────────

@app.route('/analytics')
def analytics():
    data = get_dashboard_data()
    kmeans_data = run_kmeans_analysis()
    return render_template('analytics.html', data=data, kmeans=kmeans_data)

@app.route('/api/analytics')
def api_analytics():
    data = get_dashboard_data()
    return jsonify(data)

@app.route('/api/kmeans')
def api_kmeans():
    return jsonify(run_kmeans_analysis())

# ─── INIT DB ──────────────────────────────────────────────────

@app.cli.command('init-db')
def init_db():
    from seed_data import seed_database
    db.create_all()
    seed_database()
    print("Database initialized with sample data!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if Product.query.count() == 0:
            from seed_data import seed_database
            seed_database()
    app.run(debug=True)