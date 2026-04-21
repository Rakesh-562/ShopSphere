import { Link, useNavigate } from "react-router-dom";
import { useCart } from "../context/CartContext";

export default function CartPage() {
  const { items, removeFromCart, updateQuantity, totalPrice, clearCart } = useCart();
  const navigate = useNavigate();

  if (items.length === 0) {
    return (
      <div className="empty-cart">
        <h2>Your cart is empty 🛒</h2>
        <Link to="/products" className="btn-primary">Browse Products</Link>
      </div>
    );
  }

  return (
    <div className="cart-page">
      <h1>Your Cart</h1>

      <div className="cart-items">
        {items.map(({ product, quantity }) => (
          <div key={product.id} className="cart-item">
            <img
              src={product.image || "https://via.placeholder.com/80"}
              alt={product.name}
              className="cart-item-img"
            />

            <div className="cart-item-info">
              <h3>{product.name}</h3>
              <p>₹{product.price} each</p>
            </div>

            <div className="cart-item-qty">
              <button onClick={() => updateQuantity(product.id, quantity - 1)}>-</button>
              <span>{quantity}</span>
              <button onClick={() => updateQuantity(product.id, quantity + 1)}>+</button>
            </div>

            <p className="cart-item-subtotal">₹{(product.price * quantity).toFixed(2)}</p>

            <button
              className="btn-remove"
              onClick={() => removeFromCart(product.id)}
            >
              ✕
            </button>
          </div>
        ))}
      </div>

      <div className="cart-summary">
        <h2>Total: ₹{totalPrice.toFixed(2)}</h2>
        <button className="btn-clear" onClick={clearCart}>Clear Cart</button>
        <button className="btn-primary" onClick={() => navigate("/checkout")}>
          Proceed to Checkout →
        </button>
      </div>
    </div>
  );
}
