import React from 'react';
import {shallow} from 'enzyme';
import Login from '../components/Login';


describe("Login Page", () => {
  it("renders the signup flow on load", () => {
    const wrapper = shallow(<Login />);
    const loginMessage = wrapper.find(".login-message");
    expect(loginMessage.text()).toBe("Let's Get Started!");
  });
})

