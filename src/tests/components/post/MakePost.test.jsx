import React from "react";
import { shallow } from "enzyme";
import MakePost from "../../../components/post/MakePost";

describe("Post box Component", () => {
  it("should render correctly", () => {
    const component = shallow(<MakePost />);
    expect(component).toMatchSnapshot();
  });
});
