import { createContext } from "react"

export const UserContext = createContext({ user: {displayName: null, id: null, profilePicture: null}, setUser: (user) => {}});