import Button from "@restart/ui/esm/Button";
import React from "react";
import { Link } from "react-router-dom";
import Headers from "../components/Headers"

function SignUpPage(){
  return (
    <form>
        <Headers></Headers>
        <div className="form-group">
            <label 
              style={{color: "orange", marginTop: "100px", marginLeft:"40%"}}>Username
            </label>
            <input 
              style={{color: "orange", marginTop: "5px", marginLeft:"40%", width:"300px"}} type="email" className="form-control" placeholder="Enter username" />
        </div>
  
        <div className="form-group">
            <label 
              style={{color: "orange", marginTop: "10px", marginLeft:"40%"}}>Email
            </label>
            <input 
              style={{color: "orange", marginTop: "5px", marginLeft:"40%", width:"300px"}} type="password" className="form-control" placeholder="Enter email" />
        </div>

        <div className="form-group">
            <label 
              style={{color: "orange", marginTop: "10px", marginLeft:"40%"}}>Password
            </label>
            <input 
              style={{color: "orange", marginTop: "5px", marginLeft:"40%", width:"300px"}} type="password" className="form-control" placeholder="Enter password" />
        </div>

        <div className="form-group">
            <label 
              style={{color: "orange", marginTop: "10px", marginLeft:"40%"}}>Confirm password
            </label>
            <input 
              style={{color: "orange", marginTop: "5px", marginLeft:"40%", width:"300px"}} type="password" className="form-control" placeholder="Enter password" />
        </div>

        <Link to={{pathname: "/login"}}>
        <button 
          style={{backgroundColor: "orange", marginTop: "15px", marginLeft:"43%"}} type="submit" className="btn btn-primary btn-block">
          ok
        </button>
        </Link>

        <Link to={{pathname: "/"}}>
        <button 
          style={{ marginTop: "15px", marginLeft:"70px"}} type="submit" className="btn btn-primary btn-block">
          Cancel
        </button>
        </Link>

    </form>
  );
}

export default SignUpPage;