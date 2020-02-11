import React from "react";
import { shallow } from "enzyme";
import MakePost from "../../../components/post/MakePost";

describe("Post box Component", () => {
  it("should render correctly", () => {
    const component = shallow(<MakePost />);
    expect(component).toMatchSnapshot();
  });

  it("should have a text area", () => {
    const component = shallow(<MakePost />);
    expect(component.find("textarea")).toHaveLength(1);
  });

  it("should show the modal after clicking on image icon", () => {
    const component = shallow(<MakePost />);
    const { modalShow } = component.state();
    expect(modalShow).toBe(false);
    setTimeout(() => {
      component.find(".image-icon").simulate("click");

      jest.runOnlyPendingTimers();
      component.update();
      expect(modalShow).toBe(true);
    }, 500);
  });
});
