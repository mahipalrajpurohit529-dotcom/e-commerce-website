# LuxeThreads — Fashion E-Commerce Platform

A Zara-inspired premium fashion e-commerce website built with Python Flask, SQLite database, and K-Means clustering analytics.

## Project Structure

```
LuxeThreads/
├── app.py              # Main Flask application & routes
├── database.py         # SQLAlchemy models (Product, Order, Customer, etc.)
├── analytics.py        # K-Means clustering + dashboard aggregations
├── seed_data.py        # 24 products, 12 customers, 220 orders (6 months)
├── requirements.txt
├── static/
│   ├── css/style.css   # Full luxury dark theme stylesheet
│   └── js/main.js      # UI interactions
└── templates/
    ├── base.html        # Navbar, footer, flash messages
    ├── index.html       # Homepage with hero, categories, featured
    ├── shop.html        # Product listing with filters & pagination
    ├── product.html     # Product detail with add-to-cart
    ├── cart.html        # Shopping cart
    ├── checkout.html    # Checkout form
    ├── order_confirmation.html
    └── analytics.html  # Full business analytics dashboard
```

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run app (auto-seeds database on first run)
python app.py
```

Visit: http://localhost:5000

## Features

### E-Commerce
- Product catalog with 5 categories (Women, Men, Accessories, Outerwear, Footwear)
- 24 pre-loaded products with images, sizes, colors, stock tracking
- Shopping cart (session-based)
- Checkout → Order confirmation
- Customer & order records saved to SQLite

### Analytics Dashboard (/analytics)
- **KPIs**: Total Revenue, Orders, Customers, Avg Order Value
- **Monthly Trends**: Revenue + order count over 6 months
- **Category Sales**: Doughnut chart of revenue per category
- **Stock Status**: Pie chart of in/low/out-of-stock
- **Top 10 Products**: Horizontal bar chart
- **K-Means Clustering**: 3 segments — Star Products / Average / Underperformers
  - Pure Python implementation (no scikit-learn needed)
  - Scatter plot visualization
  - Features: normalized revenue, units sold, stock
- **Best & Low Performer tables**

## Database Models
- `Category` — product categories
- `Product` — full product info with pricing, stock, images
- `Customer` — buyer info
- `Order` — order with status (pending/confirmed/shipped/delivered)
- `OrderItem` — line items linking orders to products