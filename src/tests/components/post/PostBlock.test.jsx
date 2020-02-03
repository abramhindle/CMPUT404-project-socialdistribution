import React from "react";
import { shallow } from "enzyme";
import PostBlock from "../../../components/post/PostBlock";
import demoImage from "../../../images/demo-img.png";

describe("Post Block Components", () => {
  it("should render correctly", () => {
    const component = shallow(
      <PostBlock
        imageSrc={demoImage}
        username="testuser"
        postTime="10 hours ago"
        content="test blog content"
      />,
    );
    expect(component).toMatchSnapshot();
  });
});
