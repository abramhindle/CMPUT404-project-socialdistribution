import React from "react";
import { shallow } from "enzyme";
import NavigationBar from "../../components/NavigationBar";

describe("Navigation bar Component", () => {
  it("should render correctly", () => {
    const component = shallow(<NavigationBar />);
    expect(component).toMatchSnapshot();
  });
});
