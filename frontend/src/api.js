import axios from "axios";

const apiUrl = "/choreo-apis/awbo/backend/rest-api-be2/v1.0";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : apiUrl,
  withCredentials: true,  // Asegura que las cookies de sesión se envíen con cada solicitud
});

// Interceptor de solicitud para manejar cualquier configuración adicional si es necesario
api.interceptors.request.use(
  (config) => {
    // Puedes agregar lógica adicional aquí si es necesario
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor de respuesta para manejar errores o refrescar cookies si es necesario
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Maneja los errores aquí si es necesario
    return Promise.reject(error);
  }
);

export default api;
