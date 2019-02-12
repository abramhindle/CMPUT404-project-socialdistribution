import React from 'react';
import {render} from 'react-dom';
import './index.css';
import App from './App';
import store from "./store/index";
import {Provider} from "react-redux";

/**
 * Wraps the entire application in the redux store. Makes it
 * easier to access state for components. This store is a single
 * source of truth and helps manage the state for our app.
 */

render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById("root")
);
