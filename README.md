# 🛍️ ShopSphere - Product Service (Backend)

This is the **Product Service Backend** for the ShopSphere project.

It is built using **FastAPI** and **Elasticsearch** and provides APIs to manage and search products.

---

## 🚀 Features

- Add new products
- Get all products
- Search products (with fuzzy search support)
- Elasticsearch integration for fast searching

---

## 🛠️ Tech Stack

- Python
- FastAPI
- Elasticsearch
- Docker

---

## 📁 Project Structure
```
shopsphere-product-service/
│
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── elastic.py
│   └── schemas.py
│
├── docker-compose.yml
├── requirements.txt
├── README.md                                                                                                          ## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Rakesh-562/ShopSphere.git
cd shopsphere-product-service
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run Elasticsearch (Docker)

```bash
docker-compose up -d
```

---

### 5. Start Backend Server

```bash
uvicorn app.main:app --reload
```                                                                                                                    ## 📌 API Endpoints

### 🔹 Get All Products

GET `/products`

---

### 🔹 Add Product

POST `/products`

#### Request Body:

```json
{
  "name": "Nike Shoes",
  "price": 2999,
  "description": "Running shoes"
}
```

---

### 🔹 Search Products

GET `/products/search?query=shoes`

- Supports fuzzy search (handles typos)                                                                             ## 🤝 Frontend Integration

Frontend developers can use the following APIs:

- GET `/products` → Fetch all products  
- POST `/products` → Add a new product  
- GET `/products/search?query=...` → Search products  

### Base URL:

```
http://127.0.0.1:8000
```

### API Documentation:

Open in browser:
http://127.0.0.1:8000/docs
