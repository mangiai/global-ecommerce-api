from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.models import Inventory, Product
from app.schemas.schemas import InventoryBase, InventoryOut, InventoryUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=InventoryOut)
def create_inventory(data: InventoryBase, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing = db.query(Inventory).filter(Inventory.product_id == data.product_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Inventory already exists")

    inv = Inventory(**data.dict())
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv

@router.get("/", response_model=list[InventoryOut])
def list_inventory(db: Session = Depends(get_db)):
    return db.query(Inventory).all()

@router.put("/{product_id}", response_model=InventoryOut)
def update_stock(product_id: int, update: InventoryUpdate, db: Session = Depends(get_db)):
    inv = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory not found")

    inv.stock = update.stock
    db.commit()
    db.refresh(inv)
    return inv
    