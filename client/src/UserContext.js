import { createContext } from "react"

export const UserContext = createContext({ user: "", setUser: (user) => {}});