import React from "react";
import { Form , Stack} from "react-bootstrap";
import Signup from "./SignUpPage"

function LoginPage(){
  return (
    <form>
  
        <div className="form-group">
            <label style={{color: "orange"}}>Username</label>
            <input type="email" className="form-control" placeholder="Enter username" />
        </div>
  
        <div className="form-group">
            <label>Password</label>
            <input type="password" className="form-control" placeholder="Enter password" />
        </div>

  
        <button type="submit" className="btn btn-primary btn-block">Login</button>
        <p className="forgot-password text-right">
            Forgot <a href="#">password?</a>
        </p>
    </form>
  );
}

export default LoginPage();