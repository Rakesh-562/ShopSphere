import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { getOrders } from "../api/orders";

export default function DashboardPage() {
  const { user } = useAuth();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    getOrders()
      .then((res) => setOrders(res.data.orders || res.data))
      .catch(() => setError("Could not load orders."))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="dashboard-page">
      {/* Profile Section */}
      <div className="profile-card">
        <div className="avatar">{user?.name?.[0]?.toUpperCase() || "U"}</div>
        <div className="profile-info">
          <h2>{user?.name}</h2>
          <p>{user?.email}</p>
        </div>
      </div>

      {/* Order History */}
      <div className="orders-section">
        <h2>Your Orders</h2>

        {loading && <div className="loading">Loading orders...</div>}
        {error && <div className="error-msg">{error}</div>}

        {!loading && orders.length === 0 && (
          <div className="empty-state">You haven't placed any orders yet.</div>
        )}

        {orders.map((order) => (
          <div key={order.id} className="order-card">
            <div className="order-header">
              <span className="order-id">Order #{order.id}</span>
              <span className={`order-status status-${order.status?.toLowerCase()}`}>
                {order.status}
              </span>
              <span className="order-date">
                {new Date(order.created_at).toLocaleDateString()}
              </span>
            </div>

            <div className="order-items">
              {order.items?.map((item, i) => (
                <div key={i} className="order-item-row">
                  <span>{item.product_name || `Product #${item.product_id}`}</span>
                  <span>× {item.quantity}</span>
                  <span>₹{item.price}</span>
                </div>
              ))}
            </div>

            <div className="order-total">
              Total: <strong>₹{order.total}</strong>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
