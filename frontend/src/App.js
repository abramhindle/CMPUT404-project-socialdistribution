import './App.css';
import RegistrationForm from './pages/Registration/Registration';
import HomePage from './pages/HomePage/HomePage';
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom';
import BaseTemplate from './pages/BaseTemplate';
import LoginPage from './pages/Login/Login';
import store from "./redux/store"
import { Provider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import { persistStore } from 'redux-persist';

let persistor = persistStore(store);

function App() {
  return  (
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <HashRouter>
          <Routes>
              <Route path="homepage" element={<HomePage />} />
              <Route path="register" element={<RegistrationForm />} />
              <Route path="" element={<LoginPage />} >
            </Route>
          </Routes>
        </HashRouter>
      </PersistGate>
    </Provider>
  )
}

export default App;
