import React from "react"
import { useState } from "react"
import authService from "../services/auth"

const Login = () => {
  const [ password, setPassword ] = useState("")
  const [ username, setUsername ] = useState("")

  const handleLogin = async (event) => {
    const res = await authService.login({ username, password });
    console.log(res);
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