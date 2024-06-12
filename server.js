const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

// Middleware para servir archivos estáticos
app.use(express.static(path.join(__dirname, 'chatfront/build')));

// Proxy requests to /api to Django
app.use('/api', createProxyMiddleware({
  target: 'https://chatbot-tfg-863d13080855.herokuapp.com', // Cambia esto a tu dominio de Heroku
  changeOrigin: true,
  pathRewrite: {
    '^/api': '/api', // asegúrate de que /api se mantenga en el backend
  },
}));

// Servir el archivo index.html para cualquier ruta no definida
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'chatfront/build', 'index.html'));
});

// Configurar el puerto y escuchar
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
