import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCart } from "../context/CartContext";
import { placeOrder } from "../api/orders";

export default function CheckoutPage() {
  const { items, totalPrice, clearCart } = useCart();
  const navigate = useNavigate();

  const [address, setAddress] = useState({
    street: "", city: "", state: "", pincode: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) =>
    setAddress({ ...address, [e.target.name]: e.target.value });

  const handleOrder = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    // Build the order payload your teammate's Orders API expects
    const orderPayload = {
      items: items.map((i) => ({
        product_id: i.product.id,
        quantity: i.quantity,
        price: i.product.price,
      })),
      shipping_address: address,
      total: totalPrice,
    };

    try {
      await placeOrder(orderPayload);
      clearCart();
      navigate("/dashboard"); // take user to dashboard after ordering
    } catch (err) {
      setError(err.response?.data?.message || "Failed to place order. Try again.");
    } finally {
      setLoading(false);
    }
  };

  if (items.length === 0) {
    return (
      <div className="empty-cart">
        <h2>Nothing to checkout!</h2>
        <button onClick={() => navigate("/products")} className="btn-primary">
          Shop Now
        </button>
      </div>
    );
  }

  return (
    <div className="checkout-page">
      <h1>Checkout</h1>

      <div className="checkout-layout">
        {/* Left: Address form */}
        <div className="checkout-form-section">
          <h2>Shipping Address</h2>
          {error && <div className="error-msg">{error}</div>}

          <form onSubmit={handleOrder} className="auth-form">
            <label>Street</label>
            <input name="street" value={address.street} onChange={handleChange} required placeholder="123 Main Street" />

            <label>City</label>
            <input name="city" value={address.city} onChange={handleChange} required placeholder="Hyderabad" />

            <label>State</label>
            <input name="state" value={address.state} onChange={handleChange} required placeholder="Telangana" />

            <label>Pincode</label>
            <input name="pincode" value={address.pincode} onChange={handleChange} required placeholder="500072" />

            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? "Placing Order..." : `Place Order · ₹${totalPrice.toFixed(2)}`}
            </button>
          </form>
        </div>

        {/* Right: Order summary */}
        <div className="order-summary">
          <h2>Order Summary</h2>
          {items.map(({ product, quantity }) => (
            <div key={product.id} className="summary-item">
              <span>{product.name} × {quantity}</span>
              <span>₹{(product.price * quantity).toFixed(2)}</span>
            </div>
          ))}
          <hr />
          <div className="summary-total">
            <strong>Total</strong>
            <strong>₹{totalPrice.toFixed(2)}</strong>
          </div>
        </div>
      </div>
    </div>
  );
}
