import { orderApi } from "./axiosInstance";

// GET /orders/  → list of user's orders
export const getOrders = () => orderApi.get("/orders/");

// POST /orders/  → place a new order
export const placeOrder = (data) => orderApi.post("/orders/", data);

// GET /orders/:id → single order details
export const getOrderById = (id) => orderApi.get(`/orders/${id}`);
