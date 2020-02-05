import React from "react";
import { shallow } from "enzyme";
import NavBar from "../../components/NavBar";

describe("Navigation bar Component", () => {
  it("should render correctly", () => {
    const component = shallow(<NavBar />);
    expect(component).toMatchSnapshot();
  });

  it("should not update class name when not being selected", () => {
    const component = shallow(<NavBar />);
    expect(component.find(".selected")).toHaveLength(0);
  });

  it("should update class name on selected", () => {
    const component = shallow(<NavBar selected="Home" />);
    expect(component.find(".selected")).toHaveLength(1);
  });
});
