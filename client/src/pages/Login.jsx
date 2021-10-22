import React from "react"
import { useState, useContext } from "react"
import authorService from "../services/author"
import { UserContext } from "../UserContext"
import { useHistory } from "react-router";

const Login = () => {
  const [ password, setPassword ] = useState("")
  const [ username, setUsername ] = useState("")

  const { user, setUser } = useContext(UserContext);

  const history = useHistory();

  const handleLogin = async (event) => {
    try {
      const response = await authorService.login({ username, password });
      console.log(response);
      setUser({ 
        displayName: response.data.displayName,
        profileImage: response.data.profileImage,
        id: response.data.id.split("/").at(-1),
      });
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