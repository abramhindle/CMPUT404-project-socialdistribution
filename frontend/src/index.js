<<<<<<< HEAD
import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import { Provider } from "react-redux";
import { PersistGate } from "redux-persist/integration/react";
import { store, persistor } from "./reducer/store";
=======
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Inbox from './pages/Inbox/inbox';
import reportWebVitals from './reportWebVitals';
>>>>>>> 2085f5585fcd1f4046d62ae6a96dec1b031a97af

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
<<<<<<< HEAD
  <Provider store={store}>
    <PersistGate persistor={persistor}>
      <App />
    </PersistGate>
  </Provider>
=======
  <React.StrictMode>
    <Inbox />
  </React.StrictMode>
>>>>>>> 2085f5585fcd1f4046d62ae6a96dec1b031a97af
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
