import React from "react"
import { useState } from "react"
import authService from "../services/auth"

const Register = () => {
  const [ password, setPassword ] = useState("")
  const [ username, setUsername ] = useState("")

  const handleRegister = async (event) => {
    const res = await authService.register({ username, password });
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
      <button onClick={handleRegister}>
        Submit
      </button>
    </div>
  )
}

export default Register;