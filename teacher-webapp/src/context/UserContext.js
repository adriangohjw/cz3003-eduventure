import React from "react";

var UserStateContext = React.createContext();
var UserDispatchContext = React.createContext();

const url = new URL("http://127.0.0.1:5000/"); //localhost

function userReducer(state, action) {
  switch (action.type) {
    case "LOGIN_SUCCESS":
      return { ...state, isAuthenticated: true };
    case "SIGN_OUT_SUCCESS":
      return { ...state, isAuthenticated: false };
    case "LOGIN_FAILURE":
      return { ...state, isAuthenticated: false };
    default: {
      throw new Error(`Unhandled action type: ${action.type}`);
    }
  }
}

function UserProvider({ children }) {
  var [state, dispatch] = React.useReducer(userReducer, {
    isAuthenticated: !!localStorage.getItem("id"),
  });

  return (
    <UserStateContext.Provider value={state}>
      <UserDispatchContext.Provider value={dispatch}>
        {children}
      </UserDispatchContext.Provider>
    </UserStateContext.Provider>
  );
}

function useUserState() {
  var context = React.useContext(UserStateContext);
  if (context === undefined) {
    throw new Error("useUserState must be used within a UserProvider");
  }
  return context;
}

function useUserDispatch() {
  var context = React.useContext(UserDispatchContext);
  if (context === undefined) {
    throw new Error("useUserDispatch must be used within a UserProvider");
  }
  return context;
}

export {
  UserProvider,
  useUserState,
  useUserDispatch,
  loginUser,
  signUp,
  signOut,
  url,
};

// ###########################################################

function loginUser(dispatch, email, password, history, setIsLoading, setError) {
  setError(false);
  setIsLoading(true);

  fetch(url + `users/auth?email=${email}&password=${password}`, {
    method: "GET",
  })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        // dispatch({ type: "LOGIN_FAILURE" });
        setError(true);
        setIsLoading(false);
      }
    })
    .then(response => {
      //for easy retrieval by the header
      localStorage.setItem("id", response.id);
      localStorage.setItem("name", response.name);
      localStorage.setItem("email", response.email);
      setError(null);
      setIsLoading(false);
      dispatch({ type: "LOGIN_SUCCESS" });
      history.push("/app/dashboard");
    })
    .catch(error => {
      console.error("Error:", error);
      alert("Invalid Credentials");
    });
}

function signUp(
  dispatch,
  name,
  email,
  password,
  history,
  setIsLoading,
  setError,
) {
  setError(false);
  setIsLoading(true);
  fetch(url + `staffs/?email=${email}&password=${password}&name=${name}`, {
    method: "POST",
  })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        // dispatch({ type: "LOGIN_FAILURE" });
        setError(true);
        setIsLoading(false);
      }
    })
    .then(response => {
      localStorage.setItem("id", response.id);
      localStorage.setItem("name", response.name);
      localStorage.setItem("email", response.email);
      setError(null);
      setIsLoading(false);
      dispatch({ type: "LOGIN_SUCCESS" });
      history.push("/app/dashboard"); //automatically login after creating a new account
    })
    .catch(error => {
      console.error("Error:", error);
      alert("something went wrong");
    });
}

function signOut(dispatch, history) {
  localStorage.removeItem("id"); //remove previously set id
  dispatch({ type: "SIGN_OUT_SUCCESS" });
  history.push("/login");
}
