const local = true;
const domain = local
  ? "http://localhost"
  : "https://c404-w2021-t1-social-distribut.herokuapp.com";
const port = local ? 8000 : "";

export { domain, port };
