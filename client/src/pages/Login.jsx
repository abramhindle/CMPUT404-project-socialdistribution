import React from "react"
import { useState, useContext } from "react"
import authService from "../services/auth"
import { UserContext } from "../UserContext"
import { useHistory } from "react-router";

const Login = () => {
  const [ password, setPassword ] = useState("")
  const [ username, setUsername ] = useState("")

  const { setUser } = useContext(UserContext);

  const history = useHistory();

  const handleLogin = async (event) => {
    try {
      console.log(await authService.login({ username, password }));
      setUser(username);
      localStorage.setItem("username", username);
      history.push("/");
    } catch (e) {
      setUsername("");
      setPassword("");
    } 
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