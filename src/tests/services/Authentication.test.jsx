import axios from "axios";
import * as auth from "../../services/Authentication";

describe("Authentication Service", () => {
  it("should correctly set payload on login", () => {
    const axiosPostSpy = jest.spyOn(axios, "post");

    auth.loginUser("username", "password");

    expect(axiosPostSpy).toHaveBeenCalledWith("/auth/login/", {
      username: "username",
      password: "password",
    });
  });

  it("should correctly set payload on register", () => {
    const axiosPostSpy = jest.spyOn(axios, "post");

    auth.registerUser("username", "password");

    expect(axiosPostSpy).toHaveBeenCalledWith("/auth/registration/", {
      username: "username",
      password1: "password",
      password2: "password",
    });
  });
});
