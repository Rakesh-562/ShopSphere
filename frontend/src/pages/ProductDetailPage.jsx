import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getProductById } from "../api/products";
import { useCart } from "../context/CartContext";

export default function ProductDetailPage() {
  const { id } = useParams(); // reads the :id from the URL
  const navigate = useNavigate();
  const { addToCart } = useCart();

  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [qty, setQty] = useState(1);
  const [added, setAdded] = useState(false);

  useEffect(() => {
    getProductById(id)
      .then((res) => setProduct(res.data))
      .catch(() => setError("Product not found."))
      .finally(() => setLoading(false));
  }, [id]);

  const handleAddToCart = () => {
    addToCart(product, qty);
    setAdded(true);
    setTimeout(() => setAdded(false), 2000); // reset message after 2 sec
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error-msg">{error}</div>;

  return (
    <div className="detail-page">
      <button className="btn-back" onClick={() => navigate(-1)}>← Back</button>

      <div className="detail-container">
        <img
          src={product.image || "https://via.placeholder.com/400"}
          alt={product.name}
          className="detail-img"
        />

        <div className="detail-info">
          <h1>{product.name}</h1>
          <p className="detail-price">₹{product.price}</p>
          <p className="detail-category">Category: {product.category}</p>
          <p className="detail-desc">{product.description}</p>

          <div className="qty-row">
            <label>Quantity:</label>
            <button onClick={() => setQty(Math.max(1, qty - 1))}>-</button>
            <span>{qty}</span>
            <button onClick={() => setQty(qty + 1)}>+</button>
          </div>

          <button className="btn-primary" onClick={handleAddToCart}>
            {added ? "✅ Added to Cart!" : "Add to Cart"}
          </button>

          <button className="btn-secondary" onClick={() => navigate("/cart")}>
            Go to Cart
          </button>
        </div>
      </div>
    </div>
  );
}
