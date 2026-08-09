from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import MetaData

# Naming convention so Alembic auto-generates constraint names instead of
# leaving them unnamed (SQLite's batch-mode ALTER TABLE requires named
# constraints, and we hit "Constraint must have a name" without this).
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=naming_convention)
db = SQLAlchemy(metadata=metadata)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    image_url = db.Column(db.String(300))
    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'


class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    commission_rate = db.Column(db.Float, nullable=False, default=15.0)  # percentage, e.g. 15.0 = 15%
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    products = db.relationship('Product', backref='vendor', lazy=True)
    order_items = db.relationship('OrderItem', backref='vendor', lazy=True)

    def __repr__(self):
        return f'<Vendor {self.name}>'


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float)
    stock = db.Column(db.Integer, default=50)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=True)
    image_url = db.Column(db.String(300))
    featured = db.Column(db.Boolean, default=False)
    sizes = db.Column(db.String(200), default='XS,S,M,L,XL')
    colors = db.Column(db.String(200), default='Black,White,Beige')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)

    @property
    def total_sold(self):
        return sum(item.quantity for item in self.order_items)

    @property
    def total_revenue(self):
        return sum(item.quantity * item.price for item in self.order_items)

    @property
    def discount_pct(self):
        if self.original_price and self.original_price > self.price:
            return int((1 - self.price / self.original_price) * 100)
        return 0

    def __repr__(self):
        return f'<Product {self.name}>'

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    whatsapp_number = db.Column(db.String(20))
    instagram_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='customer', lazy=True)

    def __repr__(self):
        return f'<Customer {self.name}>'

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, confirmed, shipped, delivered
    payment_status = db.Column(db.String(50), default='unpaid')  # unpaid, paid, failed, refunded
    payment_id = db.Column(db.String(150))  # Razorpay payment ID, set on webhook confirmation
    channel = db.Column(db.String(50), default='web')  # web, whatsapp, instagram
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return f'<Order #{self.id}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # price at time of purchase
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=True)
    vendor_payout = db.Column(db.Float, nullable=True)  # price*qty minus platform commission