import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";

export const api = axios.create({
    baseURL: API_URL,
    withCredentials: true,
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) {
        config.headers.Authorization = `JWT ${token}`;
    }
    return config;
});