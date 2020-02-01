import React from "react";
import {shallow, mount} from "enzyme";
import Login from "../components/Login";
import * as auth from "../services/Authentication";

describe("Login Page", () => {
  it("should render correctly", () => {
    const component = shallow(<Login />);
    expect(component).toMatchSnapshot();
  });

  it("should switch to sign in on secondary button click", () => {
    const component = shallow(<Login />);
    const signinButton = component.find(".login-secondary-button");

    signinButton.simulate("click");

    expect(component).toMatchSnapshot();
  });

  it("should show error if fields are incorrect", () => {
    const wrapper = mount(<Login />);
    const signupButton = wrapper.find("form>.login-button");
    
    wrapper.setState({
      password: "password",
    });
    signupButton.simulate("submit");
    expect(wrapper.state("error")).toBe("Please fill in the username");

    wrapper.setState({
      username: "username",
      password: "password",
    });
    signupButton.simulate("submit");
    expect(wrapper.state("error")).toBe("Please confirm your password");

    wrapper.setState({
      username: "username",
      password: "password",
      passwordReentry: "wrongPassword"
    });
    signupButton.simulate("submit");
    expect(wrapper.state("error")).toBe("Passwords don't match");
  });

  it("should send registration request if sign up fields are valid", () => {
    const wrapper = mount(<Login />);
    const signupButton = wrapper.find("form>.login-button");
    
    const registerSpy = jest.spyOn(auth, "registerUser");
    wrapper.setState({
      username: "username",
      password: "password",
      passwordReentry: "password"
    });

    signupButton.simulate("submit");
    expect(wrapper.state("error")).toBe("");
    expect(registerSpy).toHaveBeenCalledTimes(1);
  });

  it("should send login request if login fields are valid", () => {
    const wrapper = mount(<Login />);
    wrapper.setState({
      signup: false // switch to login mode
    });
    const signupButton = wrapper.find("form>.login-button");
    
    const loginSpy = jest.spyOn(auth, "loginUser");
    wrapper.setState({
      username: "username",
      password: "password",
    });

    signupButton.simulate("submit");
    expect(wrapper.state("error")).toBe("");
    expect(loginSpy).toHaveBeenCalledTimes(1);
  });
  
})

