# ShopSphere - Frontend

ReactJS frontend for the ShopSphere marketplace.

## Tech Stack
- React + Vite
- React Router DOM (page navigation)
- Axios (API calls with JWT)

## Getting Started

### 1. Install dependencies
```bash
cd frontend
npm install
```

### 2. Set up environment variables
```bash
cp .env.example .env
```
Then open `.env` and update the URLs to match where your teammates' services are running.

### 3. Start the dev server
```bash
npm run dev
```
App runs at: http://localhost:5173

---

## Folder Structure

```
src/
├── api/                  # All backend API calls
│   ├── axiosInstance.js  # JWT auto-attach setup
│   ├── auth.js           # Login, register, getMe
│   ├── products.js       # Get products, search
│   └── orders.js         # Place order, get orders
├── context/              # Global state
│   ├── AuthContext.jsx
│   └── CartContext.jsx
├── components/
│   ├── common/ProtectedRoute.jsx
│   └── layout/Navbar.jsx
├── pages/
│   ├── LoginPage.jsx
│   ├── SignupPage.jsx
│   ├── ProductCatalogPage.jsx
│   ├── ProductDetailPage.jsx
│   ├── CartPage.jsx
│   ├── CheckoutPage.jsx
│   └── DashboardPage.jsx
├── App.jsx
├── main.jsx
└── index.css
```

---

## Pages & URLs

| URL | Page | Login Required? |
|-----|------|----------------|
| /products | Product catalog grid | No |
| /products/:id | Single product detail | No |
| /cart | Shopping cart | No |
| /checkout | Place order | Yes |
| /dashboard | Profile + order history | Yes |
| /login | Login form | No |
| /signup | Register form | No |

---

## Backend API Expected Endpoints

### Auth Service (Flask, port 5000)
POST /auth/login       { email, password }       → { token, user }
POST /auth/register    { name, email, password }  → { token, user }
GET  /auth/me                                     → { id, name, email }

### Product Service (FastAPI, port 8000)
GET /products          ?search=&category=&page=  → { products: [...] }
GET /products/:id                                → { id, name, price, image, description }

### Orders Service (Django, port 8001)
GET  /orders/                                    → { orders: [...] }
POST /orders/          { items, address, total } → { id, status }
