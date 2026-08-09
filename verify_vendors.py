from app import app, db
from database import Product, Vendor, OrderItem, Order

app.app_context().push()

# Check every product has a vendor
orphans = Product.query.filter(Product.vendor_id.is_(None)).count()
print('Products with no vendor:', orphans)

# Check every order item has vendor_id + payout set
missing = OrderItem.query.filter(OrderItem.vendor_id.is_(None)).count()
print('OrderItems with no vendor:', missing)

# Spot check: pick one order, verify item revenue vs payout math
o = Order.query.first()
print(f'Order #{o.id} total: {o.total}')
for item in o.items:
    line_total = item.quantity * item.price
    commission = line_total - item.vendor_payout
    rate = round((commission / line_total) * 100, 1) if line_total else 0
    print(f'  item: qty={item.quantity} price={item.price} line_total={line_total} '
          f'payout={item.vendor_payout} implied_commission_rate={rate}% vendor={item.vendor.name}')

# Vendor summary: total payout owed per vendor
print()
for v in Vendor.query.all():
    items = OrderItem.query.filter_by(vendor_id=v.id).all()
    total_payout = sum(i.vendor_payout for i in items)
    print(f'{v.name} (commission={v.commission_rate}%): {len(items)} line items, '
          f'total payout owed = {round(total_payout, 2)}')