from database import db, Product, Order, OrderItem, Category
from sqlalchemy import func
from datetime import datetime, timedelta
import json

def get_dashboard_data():
    """Aggregate all analytics data for dashboard."""
    
    # ── Total Revenue ──────────────────────────────
    total_revenue = db.session.query(func.sum(Order.total)).scalar() or 0
    total_orders = Order.query.count()
    total_customers = db.session.execute(db.text('SELECT COUNT(DISTINCT customer_id) FROM orders')).scalar()
    avg_order_value = total_revenue / total_orders if total_orders else 0

    # ── Top Selling Products ───────────────────────
    top_products_raw = db.session.query(
        Product.id, Product.name, Product.price,
        func.sum(OrderItem.quantity).label('units_sold'),
        func.sum(OrderItem.quantity * OrderItem.price).label('revenue')
    ).join(OrderItem).group_by(Product.id).order_by(
        func.sum(OrderItem.quantity * OrderItem.price).desc()
    ).limit(10).all()

    top_products = [
        {'id': r.id, 'name': r.name, 'price': r.price,
         'units_sold': int(r.units_sold or 0), 'revenue': float(r.revenue or 0)}
        for r in top_products_raw
    ]

    # ── Category-wise Sales ────────────────────────
    cat_sales_raw = db.session.query(
        Category.name,
        func.sum(OrderItem.quantity).label('units'),
        func.sum(OrderItem.quantity * OrderItem.price).label('revenue')
    ).join(Product, Product.category_id == Category.id
    ).join(OrderItem, OrderItem.product_id == Product.id
    ).group_by(Category.id).all()

    category_sales = [
        {'category': r.name, 'units': int(r.units or 0), 'revenue': float(r.revenue or 0)}
        for r in cat_sales_raw
    ]

    # ── Monthly Order Trends (last 6 months) ──────
    six_months_ago = datetime.utcnow() - timedelta(days=180)
    monthly_raw = db.session.query(
        func.strftime('%Y-%m', Order.order_date).label('month'),
        func.count(Order.id).label('orders'),
        func.sum(Order.total).label('revenue')
    ).filter(Order.order_date >= six_months_ago
    ).group_by(func.strftime('%Y-%m', Order.order_date)
    ).order_by('month').all()

    monthly_trends = [
        {'month': r.month, 'orders': int(r.orders), 'revenue': float(r.revenue or 0)}
        for r in monthly_raw
    ]

    # ── Stock Status ───────────────────────────────
    all_products = Product.query.all()
    stock_status = {
        'out_of_stock': sum(1 for p in all_products if p.stock == 0),
        'low_stock': sum(1 for p in all_products if 0 < p.stock <= 15),
        'in_stock': sum(1 for p in all_products if p.stock > 15),
    }

    # ── Best & Low Performing ─────────────────────
    all_perf = db.session.query(
        Product.id, Product.name, Product.price,
        func.coalesce(func.sum(OrderItem.quantity), 0).label('units_sold'),
        func.coalesce(func.sum(OrderItem.quantity * OrderItem.price), 0).label('revenue')
    ).outerjoin(OrderItem).group_by(Product.id).all()

    perf_list = sorted(
        [{'id': r.id, 'name': r.name, 'units_sold': int(r.units_sold), 'revenue': float(r.revenue)} for r in all_perf],
        key=lambda x: x['revenue'], reverse=True
    )
    best_performers = perf_list[:5]
    low_performers = perf_list[-5:][::-1]

    return {
        'total_revenue': round(total_revenue, 2),
        'total_orders': total_orders,
        'total_customers': total_customers,
        'avg_order_value': round(avg_order_value, 2),
        'top_products': top_products,
        'category_sales': category_sales,
        'monthly_trends': monthly_trends,
        'stock_status': stock_status,
        'best_performers': best_performers,
        'low_performers': low_performers,
    }


def run_kmeans_analysis():
    """
    K-Means Clustering on products.
    Features: units_sold, revenue, stock
    Clusters: 3 — Star, Average, Underperformer
    Pure Python implementation (no sklearn dependency).
    """
    import math
    import random

    all_products = db.session.query(
        Product.id, Product.name, Product.price, Product.stock,
        func.coalesce(func.sum(OrderItem.quantity), 0).label('units_sold'),
        func.coalesce(func.sum(OrderItem.quantity * OrderItem.price), 0).label('revenue')
    ).outerjoin(OrderItem).group_by(Product.id).all()

    data = [
        {
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'stock': int(p.stock),
            'units_sold': int(p.units_sold),
            'revenue': float(p.revenue)
        }
        for p in all_products
    ]

    if len(data) < 3:
        return {'clusters': [], 'products': data}

    # ── Normalize features ─────────────────────────
    def normalize(values):
        mn, mx = min(values), max(values)
        if mx == mn:
            return [0.5] * len(values)
        return [(v - mn) / (mx - mn) for v in values]

    units = [d['units_sold'] for d in data]
    revenues = [d['revenue'] for d in data]
    stocks = [d['stock'] for d in data]

    norm_units = normalize(units)
    norm_rev = normalize(revenues)
    norm_stock = normalize(stocks)

    points = [(norm_rev[i], norm_units[i], norm_stock[i]) for i in range(len(data))]

    # ── K-Means (k=3, max 100 iterations) ─────────
    k = 3
    random.seed(42)
    centroids = random.sample(points, k)

    def dist(a, b):
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

    def mean_point(pts):
        n = len(pts)
        if n == 0:
            return (0, 0, 0)
        return tuple(sum(p[i] for p in pts) / n for i in range(3))

    assignments = [0] * len(points)

    for _ in range(100):
        new_assignments = [min(range(k), key=lambda c: dist(p, centroids[c])) for p in points]
        if new_assignments == assignments:
            break
        assignments = new_assignments
        for c in range(k):
            cluster_pts = [points[i] for i in range(len(points)) if assignments[i] == c]
            if cluster_pts:
                centroids[c] = mean_point(cluster_pts)

    # ── Label clusters based on avg revenue ───────
    cluster_avg_rev = {}
    for c in range(k):
        pts_rev = [data[i]['revenue'] for i in range(len(data)) if assignments[i] == c]
        cluster_avg_rev[c] = sum(pts_rev) / len(pts_rev) if pts_rev else 0

    sorted_clusters = sorted(range(k), key=lambda c: cluster_avg_rev[c], reverse=True)
    labels = {sorted_clusters[0]: 'Star Products', sorted_clusters[1]: 'Average Performers', sorted_clusters[2]: 'Underperformers'}
    colors = {sorted_clusters[0]: '#22c55e', sorted_clusters[1]: '#f59e0b', sorted_clusters[2]: '#ef4444'}

    # ── Build result ───────────────────────────────
    clustered_products = []
    for i, d in enumerate(data):
        c = assignments[i]
        clustered_products.append({
            **d,
            'cluster': c,
            'cluster_label': labels[c],
            'cluster_color': colors[c],
            'norm_rev': norm_rev[i],
            'norm_units': norm_units[i],
        })

    cluster_summary = []
    for c in range(k):
        members = [p for p in clustered_products if p['cluster'] == c]
        cluster_summary.append({
            'id': c,
            'label': labels[c],
            'color': colors[c],
            'count': len(members),
            'avg_revenue': round(sum(m['revenue'] for m in members) / len(members), 2) if members else 0,
            'avg_units': round(sum(m['units_sold'] for m in members) / len(members), 2) if members else 0,
            'products': [m['name'] for m in members[:5]]
        })

    return {
        'clusters': cluster_summary,
        'products': clustered_products,
    }