const { createProxyMiddleware } = require("http-proxy-middleware")

module.exports = (app) => {
  app.use(
    ["/service"],
    createProxyMiddleware({
      target: process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:8000/' : 'https://cmput-404-socialdistribution.herokuapp.com/',
      changeOrigin: true
    })
  );
};