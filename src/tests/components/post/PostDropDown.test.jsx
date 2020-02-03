import React from "react";
import { shallow } from "enzyme";
import PostDropdown from "../../../components/post/PostDropDown";

describe("Post DropDown Components", () => {
  it("should render correctly", () => {
    const component = shallow(<PostDropdown />);
    expect(component).toMatchSnapshot();
  });
});
