const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();


app.use(express.static(path.join(__dirname, 'chatfront/build')));

// Proxy requests to /api to Django
app.use('/api', createProxyMiddleware({
  target: 'http://localhost:8000', 
  changeOrigin: true,
  pathRewrite: {
    '^/api': '', 
  },
}));


app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'chatfront/build', 'index.html'));
});


const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});


