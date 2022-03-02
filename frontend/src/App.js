import './App.css';
import RegistrationForm from './pages/Registration/Registration';
import HomePage from './pages/HomePage/HomePage';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
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
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<BaseTemplate />} >
              <Route path="" element={<HomePage />} />
              <Route path="login" element={<LoginPage />} />
              <Route path="register" element={<RegistrationForm />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </PersistGate>
    </Provider>
  )
}

export default App;
