# Global E-commerce Admin API (Backend Developer Test- Muhammad Ahsan Submission)

![Dashboard](./screenshots/Dashboard.png)

A complete backend system with a visual dashboard built using **FastAPI**, **PostgreSQL**, and **HTML/Chart.js**, designed as a take-home test for backend developer evaluation.

---

## 🚀 Features

### API Endpoints (FastAPI)

* `POST /products/` - Add new product
* `GET /products/` - List all products
* `POST /inventory/` - Set inventory per product
* `PUT /inventory/{product_id}` - Update inventory
* `GET /inventory/` - View inventory with stock levels
* `POST /sales/` - Record a sale (auto-deduct stock)
* `GET /sales/` - List sales
* `GET /sales/summary?period=daily|monthly|yearly` - Revenue breakdown
* `GET /sales/totals` - Total revenue, order count, top selling products

### Web Dashboard (HTML/JS)

* 📊 Daily revenue line chart
* 🏆 Top 5 best-selling products
* 🛍️ Product grid with category and pricing
* ➕ Add Product form (client-side form)

---

## 🛠 Tech Stack

* **Backend**: Python 3.11, FastAPI, SQLAlchemy
* **Database**: PostgreSQL
* **Frontend**: Pure HTML/CSS + Chart.js
* **Demo Data**: Preloaded via script

---

## 📂 Project Structure

```
├── app/
│   ├── main.py
│   ├── database.py
│   ├── routers/
│   │   ├── products.py
│   │   ├── inventory.py
│   │   └── sales.py
│   ├── models/models.py
│   └── schemas/schemas.py
├── app/static/
│   ├── dashboard.html
│   └── add_product.html
├── populate_demo_data.py
├── requirements.txt
├── README.md
```

---

## 🧪 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/mangiai/global-ecommerce-api.git
cd global-ecommerce-api
```

### 2. Create `.env` File

```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/ecommerce_db
```

### 3. Create Virtual Environment & Install

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Create Tables & Populate Demo Data

```bash
python init_db.py
python populate_demo_data.py
```

### 5. Run FastAPI Server

```bash
uvicorn app.main:app --reload
```

Then open:

* Dashboard: [http://localhost:8000/dashboard](http://localhost:8000/dashboard)
* Add Product: [http://localhost:8000/add-product](http://localhost:8000/add-product)
* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📸 Screenshots

### Dashboard View

![Dashboard](./screenshots/Dashboard.png)

### Top Products

![Top Products](./screenshots/Top%20Selling%20Products.png)

### Product Grid

![Product Catalog](./screenshots/Catalog.png)

### Add Product Form

![Add Product](./screenshots/Add%20Product.png)

---

## 📄 Database Schema Overview

### `Product`

| Field    | Type       |
| -------- | ---------- |
| id       | Integer PK |
| name     | String     |
| category | String     |
| price    | Float      |

### `Inventory`

| Field       | Type          |
| ----------- | ------------- |
| id          | Integer PK    |
| product\_id | FK to Product |
| stock       | Integer       |

### `Sale`

| Field        | Type          |
| ------------ | ------------- |
| id           | Integer PK    |
| product\_id  | FK to Product |
| quantity     | Integer       |
| total\_price | Float         |
| sold\_at     | DateTime      |

---

## 🧑‍💻 Submission Note

This repository demonstrates full API design, clean backend structure, database interaction, and custom UI views — fully aligned with the take-home test scope.

🔗 GitHub: [github.com/mangiai/global-ecommerce-api](https://github.com/mangiai/global-ecommerce-api)

---

© Submitted for Backend Developer Evaluation — Powered by FastAPI ⚡
