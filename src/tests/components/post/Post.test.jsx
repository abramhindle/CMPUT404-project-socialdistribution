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

  it("should render markdown content correctly", () => {
    const mdContent = `# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6

1. Bullet 1
2. Bullet 2

[Google Link](https://www.google.com)

![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Some logo")

Inline \`code\` 

\`\`\`
var s = "some code";
alert(s);
\`\`\`

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

> Blockquote

---

Normal Text
    `;

    const component = shallow(
      <Post
        imageSrc={demoImage}
        username="testuser"
        postTime={new Date()}
        content={mdContent}
      />,
    );
    expect(component).toMatchSnapshot();
  });
});
