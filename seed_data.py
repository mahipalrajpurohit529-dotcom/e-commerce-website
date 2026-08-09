import logging
from database import db, Category, Product, Customer, Order, OrderItem, Vendor
from datetime import datetime, timedelta
import random

logger = logging.getLogger('app')

def seed_database():
    # ── Categories ──────────────────────────────────
    categories_data = [
        {'name': 'Women', 'slug': 'women', 'image_url': 'https://images.unsplash.com/photo-1581044777550-4cfa60707c03?w=600'},
        {'name': 'Men', 'slug': 'men', 'image_url': 'https://images.unsplash.com/photo-1617137968427-85924c800a22?w=600'},
        {'name': 'Accessories', 'slug': 'accessories', 'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600'},
        {'name': 'Outerwear', 'slug': 'outerwear', 'image_url': 'https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=600'},
        {'name': 'Footwear', 'slug': 'footwear', 'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600'},
    ]
    cats = {}
    for c in categories_data:
        cat = Category(**c)
        db.session.add(cat)
        db.session.flush()
        cats[c['slug']] = cat

    # ── Vendors ──────────────────────────────────────
    vendors_data = [
        {'name': 'Aura Studio', 'email': 'partnerships@aurastudio.com', 'phone': '9811100001', 'commission_rate': 15.0},
        {'name': 'Northline Apparel', 'email': 'vendor@northlineapparel.com', 'phone': '9811100002', 'commission_rate': 18.0},
        {'name': 'Coastal Craft Co.', 'email': 'hello@coastalcraftco.com', 'phone': '9811100003', 'commission_rate': 12.0},
        {'name': 'Bramble & Bark', 'email': 'sales@brambleandbark.com', 'phone': '9811100004', 'commission_rate': 20.0},
        {'name': 'Ironwood Supply', 'email': 'contact@ironwoodsupply.com', 'phone': '9811100005', 'commission_rate': 15.0},
    ]
    vendors = []
    for vd in vendors_data:
        v = Vendor(**vd)
        db.session.add(v)
        db.session.flush()
        vendors.append(v)

    # ── Products ──────────────────────────────────
    products_data = [
        # Women
        {'name': 'Linen Blazer Coat', 'price': 3499, 'original_price': 4999, 'stock': 35, 'category': 'women', 'featured': True,
         'description': 'Elegant linen blend blazer with structured shoulders and relaxed fit.', 'colors': 'Beige,Ivory,Black',
         'image_url': 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=600'},
        {'name': 'Midi Wrap Dress', 'price': 2199, 'original_price': 2999, 'stock': 60, 'category': 'women', 'featured': True,
         'description': 'Fluid wrap dress in printed satin. Effortlessly transitions from day to evening.',
         'image_url': 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=600'},
        {'name': 'Wide Leg Trousers', 'price': 1899, 'original_price': None, 'stock': 45, 'category': 'women', 'featured': False,
         'description': 'High-waist wide leg trousers in premium crepe fabric.', 'colors': 'Black,Camel,Forest Green',
         'image_url': 'https://images.unsplash.com/photo-1594938298603-c8148c4b4571?w=600'},
        {'name': 'Ribbed Crop Knit', 'price': 1299, 'original_price': None, 'stock': 80, 'category': 'women', 'featured': True,
         'description': 'Soft ribbed cotton knit top. Perfect layering piece.',
         'image_url': 'https://images.unsplash.com/photo-1603344797033-f0f4f587ab60?w=600'},
        {'name': 'Flowy Maxi Skirt', 'price': 1599, 'original_price': 1999, 'stock': 30, 'category': 'women', 'featured': False,
         'description': 'Lightweight chiffon maxi skirt with elegant drape.', 'colors': 'Dusty Rose,Black,Navy',
         'image_url': 'https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=600'},
        {'name': 'Satin Slip Dress', 'price': 2499, 'original_price': 3199, 'stock': 20, 'category': 'women', 'featured': True,
         'description': 'Classic bias-cut satin slip dress. Minimalist luxury.',
         'image_url': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=600'},
        {'name': 'Tailored Cigarette Pants', 'price': 2099, 'original_price': None, 'stock': 55, 'category': 'women', 'featured': False,
         'description': 'Sharp tailored cigarette pants in stretch wool blend.',
         'image_url': 'https://images.unsplash.com/photo-1540208990079-2b4f1a3a2ba9?w=600'},
        {'name': 'Oversized Button Shirt', 'price': 1699, 'original_price': None, 'stock': 70, 'category': 'women', 'featured': False,
         'description': 'Relaxed poplin button-down shirt. Timeless wardrobe essential.',
         'image_url': 'https://images.unsplash.com/photo-1604881991720-f91add269bed?w=600'},
        # Men
        {'name': 'Slim Fit Chinos', 'price': 1999, 'original_price': None, 'stock': 65, 'category': 'men', 'featured': True,
         'description': 'Premium cotton slim fit chinos. Versatile and refined.',
         'colors': 'Khaki,Navy,Olive,Black', 'sizes': '28,30,32,34,36',
         'image_url': 'https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=600'},
        {'name': 'Merino Crew Sweater', 'price': 2799, 'original_price': 3499, 'stock': 40, 'category': 'men', 'featured': True,
         'description': '100% merino wool crew neck sweater. Incredibly soft.',
         'colors': 'Navy,Charcoal,Oatmeal', 'sizes': 'S,M,L,XL,XXL',
         'image_url': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=600'},
        {'name': 'Oxford Dress Shirt', 'price': 1599, 'original_price': None, 'stock': 90, 'category': 'men', 'featured': False,
         'description': 'Classic Oxford cloth dress shirt in regular fit.',
         'colors': 'White,Light Blue,Pink', 'sizes': 'S,M,L,XL',
         'image_url': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600'},
        {'name': 'Linen Drawstring Pants', 'price': 1799, 'original_price': None, 'stock': 50, 'category': 'men', 'featured': False,
         'description': 'Relaxed linen pants with elasticated waist. Perfect for warm weather.',
         'image_url': 'https://images.unsplash.com/photo-1560243563-062bfc001d68?w=600'},
        {'name': 'Structured Suit Jacket', 'price': 5999, 'original_price': 7999, 'stock': 15, 'category': 'men', 'featured': True,
         'description': 'Italian wool blend suit jacket. Impeccable construction.',
         'colors': 'Charcoal,Navy,Camel', 'sizes': 'S,M,L,XL',
         'image_url': 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=600'},
        {'name': 'Graphic Print Tee', 'price': 799, 'original_price': None, 'stock': 120, 'category': 'men', 'featured': False,
         'description': 'Premium cotton graphic t-shirt. Artistic screen print.',
         'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600'},
        # Accessories
        {'name': 'Leather Tote Bag', 'price': 4499, 'original_price': 5999, 'stock': 25, 'category': 'accessories', 'featured': True,
         'description': 'Full grain leather tote bag. Spacious and structured.', 'sizes': 'One Size',
         'colors': 'Cognac,Black,Cream',
         'image_url': 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600'},
        {'name': 'Silk Scarf', 'price': 1299, 'original_price': None, 'stock': 40, 'category': 'accessories', 'featured': False,
         'description': '100% silk scarf with hand-rolled edges. Collectible print.', 'sizes': 'One Size',
         'image_url': 'https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=600'},
        {'name': 'Minimalist Watch', 'price': 8999, 'original_price': None, 'stock': 18, 'category': 'accessories', 'featured': True,
         'description': 'Swiss movement minimalist watch. Sapphire crystal glass.', 'sizes': 'One Size',
         'colors': 'Silver/White,Gold/Black,Rose Gold',
         'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600'},
        {'name': 'Structured Belt', 'price': 899, 'original_price': None, 'stock': 75, 'category': 'accessories', 'featured': False,
         'description': 'Genuine leather belt with brushed metal buckle.', 'sizes': 'XS,S,M,L,XL',
         'colors': 'Black,Tan',
         'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600'},
        # Outerwear
        {'name': 'Wool Overcoat', 'price': 8499, 'original_price': 10999, 'stock': 12, 'category': 'outerwear', 'featured': True,
         'description': 'Double-faced wool overcoat. Dramatic silhouette with satin lining.',
         'colors': 'Camel,Black,Charcoal',
         'image_url': 'https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=600'},
        {'name': 'Quilted Puffer Jacket', 'price': 3999, 'original_price': 4999, 'stock': 30, 'category': 'outerwear', 'featured': True,
         'description': 'Down-filled quilted jacket. Warm without bulk.',
         'image_url': 'https://images.unsplash.com/photo-1547949003-9792a18a2601?w=600'},
        {'name': 'Trench Coat', 'price': 6999, 'original_price': 8499, 'stock': 20, 'category': 'outerwear', 'featured': False,
         'description': 'Classic gabardine trench coat. Timeless British heritage.',
         'colors': 'Camel,Black,Navy',
         'image_url': 'https://images.unsplash.com/photo-1548624313-0396c75e4b1a?w=600'},
        # Footwear
        {'name': 'Leather Chelsea Boots', 'price': 5499, 'original_price': 6999, 'stock': 28, 'category': 'footwear', 'featured': True,
         'description': 'Pull-on Chelsea boots in vegetable-tanned leather.', 'sizes': '36,37,38,39,40,41,42',
         'colors': 'Black,Tan',
         'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600'},
        {'name': 'White Leather Sneakers', 'price': 2999, 'original_price': None, 'stock': 60, 'category': 'footwear', 'featured': True,
         'description': 'Clean minimal leather sneakers. The perfect everyday shoe.',
         'image_url': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=600'},
        {'name': 'Block Heel Mule', 'price': 3299, 'original_price': 3999, 'stock': 22, 'category': 'footwear', 'featured': False,
         'description': 'Suede block heel mules with square toe. Refined everyday elegance.', 'sizes': '36,37,38,39,40,41',
         'colors': 'Nude,Black,Camel',
         'image_url': 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=600'},
    ]

    products = []
    for i, pd in enumerate(products_data):
        cat = cats[pd.pop('category')]
        vendor = vendors[i % len(vendors)]  # round-robin assign vendors across products
        p = Product(category_id=cat.id, vendor_id=vendor.id, **pd)
        db.session.add(p)
        db.session.flush()
        products.append(p)

    # ── Customers ──────────────────────────────────
    customers_data = [
        {'name': 'Priya Sharma', 'email': 'priya.sharma@gmail.com', 'phone': '9876543210', 'address': 'MG Road, Bangalore'},
        {'name': 'Arjun Mehta', 'email': 'arjun.mehta@gmail.com', 'phone': '9812345678', 'address': 'Connaught Place, Delhi'},
        {'name': 'Sneha Patel', 'email': 'sneha.patel@gmail.com', 'phone': '9988776655', 'address': 'FC Road, Pune'},
        {'name': 'Rohan Kapoor', 'email': 'rohan.kapoor@gmail.com', 'phone': '9123456789', 'address': 'Bandra West, Mumbai'},
        {'name': 'Anika Reddy', 'email': 'anika.reddy@gmail.com', 'phone': '9234567891', 'address': 'Jubilee Hills, Hyderabad'},
        {'name': 'Vikram Singh', 'email': 'vikram.singh@gmail.com', 'phone': '9345678912', 'address': 'C-Scheme, Jaipur'},
        {'name': 'Meera Nair', 'email': 'meera.nair@gmail.com', 'phone': '9456789123', 'address': 'Indiranagar, Bangalore'},
        {'name': 'Kabir Khan', 'email': 'kabir.khan@gmail.com', 'phone': '9567891234', 'address': 'Salt Lake, Kolkata'},
        {'name': 'Ishaan Gupta', 'email': 'ishaan.gupta@gmail.com', 'phone': '9678912345', 'address': 'Sector 18, Noida'},
        {'name': 'Diya Joshi', 'email': 'diya.joshi@gmail.com', 'phone': '9789123456', 'address': 'Navrangpura, Ahmedabad'},
        {'name': 'Rahul Verma', 'email': 'rahul.verma@gmail.com', 'phone': '9890234567', 'address': 'Koramangala, Bangalore'},
        {'name': 'Ananya Das', 'email': 'ananya.das@gmail.com', 'phone': '9901345678', 'address': 'Park Street, Kolkata'},
    ]
    customers = []
    for cd in customers_data:
        c = Customer(**cd)
        db.session.add(c)
        db.session.flush()
        customers.append(c)

    # ── Orders – 6 months of realistic sales data ──
    statuses = ['delivered', 'delivered', 'delivered', 'shipped', 'confirmed']
    # Weighted popularity: some products sell more
    product_weights = [8,12,6,10,4,9,5,7, 11,8,9,6,5,14, 10,7,9,6, 12,10,7, 13,11,6]
    # Trim weights to match products count
    product_weights = product_weights[:len(products)]
    total_weight = sum(product_weights)
    product_probs = [w / total_weight for w in product_weights]

    base_date = datetime.utcnow() - timedelta(days=180)
    for _ in range(220):  # 220 orders
        customer = random.choice(customers)
        days_offset = random.randint(0, 180)
        order_date = base_date + timedelta(days=days_offset)
        status = random.choice(statuses)

        num_items = random.randint(1, 4)
        chosen_products = random.choices(products, weights=product_probs, k=num_items)
        chosen_products = list(set(chosen_products))  # deduplicate

        order = Order(customer_id=customer.id, total=0, status=status, order_date=order_date,
                      payment_status='paid', channel='web')
        db.session.add(order)
        db.session.flush()

        total = 0
        for p in chosen_products:
            qty = random.randint(1, 3)
            line_total = qty * p.price
            vendor = p.vendor  # backref set via vendor_id on the product
            commission = line_total * (vendor.commission_rate / 100.0) if vendor else 0
            payout = round(line_total - commission, 2)

            item = OrderItem(order_id=order.id, product_id=p.id, quantity=qty, price=p.price,
                             vendor_id=p.vendor_id, vendor_payout=payout)
            db.session.add(item)
            total += line_total

        order.total = total

    db.session.commit()
    logger.info('Seeded: %s products, %s vendors, %s customers, 220 orders across 6 months.',
                len(products), len(vendors), len(customers))