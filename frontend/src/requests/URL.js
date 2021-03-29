const local = true;
const domain = local
  ? "http://localhost"
  : "https://c404-w2021-t1-social-distribut.herokuapp.com";
const port = local ? 8000 : "";

//to another member's host
const remoteDomain = "https://social-distribution-t1v2.herokuapp.com";
const auth = "Basic UmVtb3RlMTpyZW1vdGUxMjM0";
// team 4
const remoteDomain4 = "https://c404posties.herokuapp.com";
const port4 = "";
const auth4 = "Token 49998f0a42dbd0ec33787c88823d5bd32dd3778a";
// team 20
const remoteDomain20 = "";
const port20 = "";
const auth20 = "";

export {
  domain,
  port,
  remoteDomain,
  auth,
  remoteDomain4,
  port4,
  auth4,
  remoteDomain20,
  port20,
  auth20,
};
