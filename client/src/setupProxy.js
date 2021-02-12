const { createProxyMiddleware } = require("http-proxy-middleware")

module.exports = (app) => {
  app.use(
    ["/service"],
    createProxyMiddleware({
      target: "http://localhost:8000",
      changeOrigin: true
    })
  );
};