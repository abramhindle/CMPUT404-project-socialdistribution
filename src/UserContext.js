import React from "react";

const UserContext = React.createContext(null);

export function useUserHandler() {
  return React.useContext(UserContext);
}

export default function UserProvider({children}) {
  const [loggedInUser, setLoggedInUser] = React.useState({})

  return (
    <UserContext.Provider value={{loggedInUser, setLoggedInUser}}>
        {children}
    </UserContext.Provider>
  )
}
