import React from 'react';
import {shallow, mount} from 'enzyme';
import Login from '../components/Login';


describe("Login Page", () => {
  it("renders the signup flow on load", () => {
    const wrapper = shallow(<Login />);
    const loginMessage = wrapper.find(".login-message");
    expect(loginMessage.text()).toBe("Let's Get Started!");
  });

  it('should render correctly', () => {
    const component = mount(<Login />);
    expect(component).toMatchSnapshot();
  });
})

