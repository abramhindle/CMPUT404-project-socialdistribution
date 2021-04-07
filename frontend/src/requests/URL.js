let _config64 = false; //process.env.REACT_APP_CONFIGBASE64;

let _domain;
let _remoteDomain;
let _remoteDomain4;
let _remoteDomain20;
let _port;
let _port4;
let _port20;
let _auth;
let _auth4;
let _auth20;

if (_config64) {
  let _config = JSON.parse(atob(_config64));
  _domain = _config.self.domain;
  _remoteDomain = _config.clone.domain;
  _remoteDomain4 = _config.team4.domain;
  _remoteDomain20 = _config.team20.domain;
  _port = _config.self.port;
  _port4 = _config.team4.port;
  _port20 = _config.team20.port;
  _auth = _config.clone.auth;
  _auth4 = _config.team4.auth;
  _auth20 = _config.team20.auth;
} else {
  _domain = "http://localhost"; //"http://localhost"; //"https://social-distribution-t1.herokuapp.com";
  _remoteDomain = "https://social-distribution-t1v2.herokuapp.com";
  _remoteDomain4 = "https://c404posties.herokuapp.com";
  _remoteDomain20 = "";
  _port = 8000; //8000;
  _port4 = 443;
  _port20 = "";
  _auth = "Basic UmVtb3RlMTpyZW1vdGUxMjM0";
  _auth4 = "Basic YWRtaW5COmFkbWluQg=="; //username: adminB, password: adminB
  _auth20 = "";
}

const domain = _domain;
const remoteDomain = _remoteDomain;
const remoteDomain4 = _remoteDomain4;
const remoteDomain20 = _remoteDomain20;
const port = _port;
const port4 = _port4;
const port20 = _port20;
const auth = _auth;
const auth4 = _auth4;
const auth20 = _auth20;

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
