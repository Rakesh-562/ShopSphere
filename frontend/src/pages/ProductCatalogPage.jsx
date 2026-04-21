import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getProducts } from "../api/products";
import { useCart } from "../context/CartContext";
import { useAuth } from "../context/AuthContext";

export default function ProductCatalogPage() {
  const { addToCart } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [page, setPage] = useState(1);

  useEffect(() => {
    // Backend requires JWT for /products — if not logged in, show a prompt
    if (!user) {
      setLoading(false);
      setError("Please log in to browse products.");
      return;
    }
    setLoading(true);
    setError("");
    getProducts({ search, category, page })
      .then((res) => setProducts(res.data.products || res.data))
      .catch((err) => {
        if (err.response?.status === 401) {
          setError("Session expired. Please log in again.");
        } else {
          setError("Failed to load products. The product service may not be running yet.");
        }
      })
      .finally(() => setLoading(false));
  }, [search, category, page, user]);

  return (
    <div className="catalog-page">
      <div className="catalog-header">
        <h1>All Products</h1>

        {/* Search bar */}
        <input
          type="text"
          className="search-input"
          placeholder="🔍 Search products..."
          value={search}
          onChange={(e) => { setSearch(e.target.value); setPage(1); }}
        />

        {/* Category filter */}
        <select
          className="filter-select"
          value={category}
          onChange={(e) => { setCategory(e.target.value); setPage(1); }}
        >
          <option value="">All Categories</option>
          <option value="electronics">Electronics</option>
          <option value="clothing">Clothing</option>
          <option value="books">Books</option>
          <option value="home">Home & Kitchen</option>
        </select>
      </div>

      {error && (
        <div className="error-msg">
          {error}{" "}
          {!user && (
            <Link to="/login" style={{ color: "inherit", fontWeight: 600, textDecoration: "underline" }}>
              Login here
            </Link>
          )}
        </div>
      )}

      {loading ? (
        <div className="loading">Loading products...</div>
      ) : products.length === 0 ? (
        <div className="empty-state">No products found.</div>
      ) : (
        <div className="product-grid">
          {products.map((product) => (
            <div key={product.id} className="product-card">
              <Link to={`/products/${product.id}`}>
                <img
                  src={product.image || "https://via.placeholder.com/200"}
                  alt={product.name}
                  className="product-img"
                />
                <h3 className="product-name">{product.name}</h3>
                <p className="product-price">₹{product.price}</p>
              </Link>
              <button
                className="btn-add-cart"
                onClick={() => addToCart(product)}
              >
                Add to Cart
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Pagination */}
      <div className="pagination">
        <button disabled={page === 1} onClick={() => setPage(page - 1)}>← Prev</button>
        <span>Page {page}</span>
        <button onClick={() => setPage(page + 1)}>Next →</button>
      </div>
    </div>
  );
}
