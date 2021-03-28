const local = true;
const domain = local
  ? "http://localhost"
  : "https://c404-w2021-t1-social-distribut.herokuapp.com";
const port = local ? 8000 : "";

const remoteDomain = "https://social-distribution-t1v2.herokuapp.com"; //to another member's host
const remoteDomain4 = "https://c404posties.herokuapp.com"; // team 4
const port4 = "";
const remoteDomain20 = ""; // team 20
const port20 = "";

export {
  domain,
  port,
  remoteDomain,
  remoteDomain4,
  port4,
  remoteDomain20,
  port20,
};
