from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routers import sales, inventory, products

app = FastAPI(title="E-commerce Admin API")

app.include_router(sales.router, prefix="/sales", tags=["Sales"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
app.include_router(products.router, prefix="/products", tags=["Products"])


app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/dashboard", include_in_schema=False)
def get_dashboard():
    return FileResponse("app/static/dashboard.html")

@app.get("/add-product", include_in_schema=False)
def get_add_product_page():
    return FileResponse("app/static/add_product.html")
