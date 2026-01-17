import axios from "axios";

const API_BASE = "/api";

// ========================================================
//   AXIOS INSTANCE
// ========================================================
const api = axios.create({
    baseURL: API_BASE,
});

// ========================================================
//   ADD ACCESS TOKEN TO ALL REQUESTS AUTOMATICALLY
// ========================================================
api.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// ========================================================
//   AUTO REFRESH TOKEN WHEN ACCESS TOKEN EXPIRES
// ========================================================
api.interceptors.response.use(
    (response) => response,

    async (error) => {
        const originalRequest = error.config;

        // Token expired → refresh token
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refresh = localStorage.getItem("refresh_token");

                const res = await axios.post(`${API_BASE}/accounts/refresh/`, {
                    refresh,
                });

                // Store new token
                localStorage.setItem("access_token", res.data.access);

                // Apply token to axios
                api.defaults.headers.Authorization = `Bearer ${res.data.access}`;
                originalRequest.headers.Authorization = `Bearer ${res.data.access}`;

                // Retry original request
                return api(originalRequest);
            } catch (err) {
                // Refresh token expired → logout
                localStorage.clear();
                window.location.href = "/login";
            }
        }

        return Promise.reject(error);
    }
);

// ========================================================
//   AUTH APIS
// ========================================================
export const loginApi = (email, password) =>
    api.post("/accounts/login/", { email, password });

export const registerApi = (data) =>
    api.post("/accounts/register/", data);

export const getProfileApi = () =>
    api.get("/accounts/profile/");

export const updateProfileApi = (data) =>
    api.put("/accounts/profile/update/", data);

// ========================================================
//   DONATION APIs
// ========================================================

// ✔ Create donation (supports images via FormData)
export const createDonationApi = (formData) =>
    api.post("/donations/create/", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });

// ✔ Get all donations
export const getDonationsApi = () =>
    api.get("/donations/");

// ✔ Get donations by type
export const getDonationByTypeApi = (type) =>
    api.get(`/donations/${type}/`);

// ✔ Get single donation by ID
export const getDonationByIdApi = (id) =>
    api.get(`/donations/${id}/`);

export default api;
