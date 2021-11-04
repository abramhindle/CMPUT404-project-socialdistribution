import React from "react";

const UserContext = React.createContext(null);

export function useUserHandler() {
  return React.useContext(UserContext);
}

export default function UserProvider({children}) {
  const [loggedInUser, setLoggedInUser] = React.useState({})

  const providerValue = React.useMemo(() => {
    return {loggedInUser, setLoggedInUser}
  }, [loggedInUser, setLoggedInUser]);

  return (
    <UserContext.Provider value={providerValue}>
        {children}
    </UserContext.Provider>
  )
}
