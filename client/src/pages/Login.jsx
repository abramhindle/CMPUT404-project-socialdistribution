import React from "react"
import { useState } from "react"

const Login = () => {
    const [ password, setPassword ] = useState("")
    const [ username, setUsername ] = useState("")

    const handleLogin = () => {

    }

    return (
        <div>
            <label>
                Username
                <input 
                    type="username"
                    onChange={(e) => {setUsername(e.target.value)}}
                >
                </input>
            </label>
            <label>
                Password
                <input
                    type="password"
                    onChange={(e) => {setPassword(e.target.value)}}
                >
                </input>
            </label>
            <button onClick={handleLogin}>
                Submit
            </button>
        </div>
    )
}

export default Login;