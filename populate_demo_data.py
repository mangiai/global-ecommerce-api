from app.database import SessionLocal
from app.models.models import Product, Inventory, Sale
from datetime import datetime, timedelta
import random

db = SessionLocal()

# Clear existing data
db.query(Sale).delete()
db.query(Inventory).delete()
db.query(Product).delete()
db.commit()

# Sample products (like Amazon/Walmart)
products_data = [
    {"name": "Wireless Mouse", "category": "Electronics", "price": 25.99},
    {"name": "Bluetooth Headphones", "category": "Electronics", "price": 79.99},
    {"name": "Organic Shampoo", "category": "Health & Beauty", "price": 10.50},
    {"name": "LED Desk Lamp", "category": "Home", "price": 45.00},
    {"name": "Men's Running Shoes", "category": "Fashion", "price": 65.00},
    {"name": "Fitness Tracker", "category": "Electronics", "price": 49.99},
    {"name": "Laptop Stand", "category": "Office", "price": 32.00},
    {"name": "Water Bottle", "category": "Home", "price": 8.25},
    {"name": "Desk Organizer", "category": "Office", "price": 15.75},
    {"name": "Face Moisturizer", "category": "Health & Beauty", "price": 18.00}
]

# Create products and inventory
products = []
for pdata in products_data:
    product = Product(**pdata)
    db.add(product)
    db.commit()
    db.refresh(product)
    products.append(product)

    inv = Inventory(product_id=product.id, stock=random.randint(100, 300))
    db.add(inv)

db.commit()

# Generate 100–200 random sales
num_sales = random.randint(100, 200)
for _ in range(num_sales):
    product = random.choice(products)
    qty = random.randint(1, 5)
    sold_at = datetime.now() - timedelta(days=random.randint(0, 30))
    total_price = qty * product.price

    sale = Sale(
        product_id=product.id,
        quantity=qty,
        total_price=total_price,
        sold_at=sold_at
    )
    db.add(sale)

    inv = db.query(Inventory).filter_by(product_id=product.id).first()
    inv.stock = max(inv.stock - qty, 0)

db.commit()
db.close()

print(f"✅ Populated {len(products)} products and {num_sales} sales.")
