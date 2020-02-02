import React from "react";
import { shallow, mount } from "enzyme";
import Login from "../../components/Login";
import * as auth from "../../services/Authentication";

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
      passwordReentry: "mismatchedPassword",
    });
    signupButton.simulate("submit");
    expect(wrapper.state("error")).toBe("Passwords don't match");
  });

  it("should not send a request if there is an error", () => {
    const wrapper = mount(<Login />);
    const registerUserSpy = jest.spyOn(auth, "registerUser");

    wrapper.setState({
      error: "some error",
    });

    const signupButton = wrapper.find("form>.login-button");
    signupButton.simulate("submit");
    expect(registerUserSpy).toHaveBeenCalledTimes(0);

    wrapper.setState({
      signup: false, // switch to login mode
    });

    const signinButton = wrapper.find("form>.login-button");
    signinButton.simulate("submit");
    expect(registerUserSpy).toHaveBeenCalledTimes(0);
  });

  it("should send registration request if sign up fields are valid", () => {
    const wrapper = mount(<Login />);
    const signupButton = wrapper.find("form>.login-button");

    const registerUserSpy = jest.spyOn(auth, "registerUser");
    wrapper.setState({
      username: "username",
      password: "password",
      passwordReentry: "password",
    });

    signupButton.simulate("submit");
    expect(wrapper.state("error")).toBe("");
    expect(registerUserSpy).toHaveBeenCalledTimes(1);
  });

  it("should send login request if login fields are valid", () => {
    const wrapper = mount(<Login />);
    wrapper.setState({
      signup: false, // switch to login mode
    });
    const signinButton = wrapper.find("form>.login-button");

    const loginUserSpy = jest.spyOn(auth, "loginUser");
    wrapper.setState({
      username: "username",
      password: "password",
    });

    signinButton.simulate("submit");
    expect(wrapper.state("error")).toBe("");
    expect(loginUserSpy).toHaveBeenCalledTimes(1);
  });
});
