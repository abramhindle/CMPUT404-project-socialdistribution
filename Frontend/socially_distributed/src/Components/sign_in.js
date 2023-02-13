import React, { useState } from "react";

function SIGN_IN(){
    const [username, set_username] =  useState("")
    const [password, set_password] = useState("")

    return (
        <form>
            <h3>Sign In</h3>
            <div className="mb-3">
                <label>Username</label>
                <input
                    type="username"
                    className="form-control"
                    placeholder="Enter Username"
                    value = {username}
                    onChange={e => set_username(e.target.value)}
                />
            </div>

            <div className="mb-3">
                <label>Password</label>
                <input
                    type="password"
                    className="form-control"
                    placeholder="Enter password"
                    value = {password}
                    onChange={e => set_password(e.target.value)}
                />
            </div>

            <div className="d-grid">
                <button type="submit" className="btn btn-primary" onClick={console.log(username, password)}>
                    Submit
                </button>
            </div>
      </form>
    )
}

export default SIGN_IN
