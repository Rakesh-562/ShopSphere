import { productApi } from "./axiosInstance";

// GET /products?search=&category=&page=
export const getProducts = (params) => productApi.get("/products", { params });

// GET /products/:id
export const getProductById = (id) => productApi.get(`/products/${id}`);

// GET /products/search?q=keyword
export const searchProducts = (query) =>
  productApi.get("/products/search", { params: { q: query } });
