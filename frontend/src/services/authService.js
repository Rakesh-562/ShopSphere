import axios from axios;
const API_URL="http://localhost:5000";
// inside AuthContext
const login = (token, user) => {
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(user));
    setUser(user);
  };
export const loginuser= async (email,password) => {
    return axios.post(`${API_URL}/api/login`,{ email,password});
};