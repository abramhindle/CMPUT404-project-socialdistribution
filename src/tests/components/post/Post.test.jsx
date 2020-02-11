import React from "react";
import { shallow } from "enzyme";
import Post from "../../../components/post/Post";
import demoImage from "../../../images/demo-img.png";

describe("Post Block Components", () => {
  it("should render correctly", () => {
    const component = shallow(
      <Post
        imageSrc={demoImage}
        username="testuser"
        postTime={new Date()}
        content="test blog content"
      />,
    );
    expect(component).toMatchSnapshot();
  });
});
