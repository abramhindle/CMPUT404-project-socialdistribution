const local = false;
const domain = local
  ? "http://localhost"
  : "https://social-distribution-t1.herokuapp.com";
const port = local ? 8000 : "";

const remoteDomain = "https://";

export { domain, port, remoteDomain };
