from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, date
from app.database import SessionLocal
from app.models.models import Sale, Product, Inventory
from app.schemas.schemas import SaleBase, SaleOut, RevenueSummary

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SaleOut)
def create_sale(sale: SaleBase, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == sale.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    inventory = db.query(Inventory).filter(Inventory.product_id == sale.product_id).first()
    if not inventory or inventory.stock < sale.quantity:
        raise HTTPException(status_code=400, detail="Insufficient inventory")

    total_price = product.price * sale.quantity
    new_sale = Sale(product_id=sale.product_id, quantity=sale.quantity, total_price=total_price)
    db.add(new_sale)

    inventory.stock -= sale.quantity
    db.commit()
    db.refresh(new_sale)
    return new_sale

@router.get("/", response_model=list[SaleOut])
def list_sales(db: Session = Depends(get_db)):
    return db.query(Sale).all()

@router.get("/summary", response_model=list[RevenueSummary])
def revenue_summary(period: str = Query("daily", enum=["daily", "monthly", "yearly"]), db: Session = Depends(get_db)):
    try:
        if period == "daily":
            group_by_expr = func.date_trunc('day', Sale.sold_at)
        elif period == "monthly":
            group_by_expr = func.to_char(Sale.sold_at, "YYYY-MM")
        elif period == "yearly":
            group_by_expr = func.extract('year', Sale.sold_at)
        else:
            raise HTTPException(status_code=400, detail="Invalid period")

        query = db.query(
            group_by_expr.label("period"),
            func.sum(Sale.total_price).label("total_revenue")
        ).group_by(group_by_expr).order_by(group_by_expr)

        results = query.all()

        return [{"period": str(row.period), "total_revenue": row.total_revenue} for row in results]

    except Exception as e:
        print("🔥 Revenue summary error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/totals")
def sales_totals(db: Session = Depends(get_db)):
    total_revenue = db.query(func.sum(Sale.total_price)).scalar() or 0
    total_orders = db.query(Sale).count()

    top_products = (
        db.query(Product.name, func.sum(Sale.quantity).label("qty"))
        .join(Sale, Product.id == Sale.product_id)
        .group_by(Product.name)
        .order_by(func.sum(Sale.quantity).desc())
        .limit(5)
        .all()
    )

    return {
        "total_revenue": float(round(total_revenue, 2)),
        "total_orders": total_orders,
        "top_products": [{"name": name, "qty": qty} for name, qty in top_products]
    }
