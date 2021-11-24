import React from "react";
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import AttachmentPost from "../components/AttachmentPost";
import ImagePost from "../components/ImagePost";
import TextPost from "../components/TextPost";

let container = null;
beforeEach(() => {
  // setup a DOM element as a render target
  container = document.createElement("div");
  document.body.appendChild(container);
});

afterEach(() => {
  // cleanup on exiting
  unmountComponentAtNode(container);
  container.remove();
  container = null;
});

it("AttachmentPost renders correctly", async () => {
  const post = {
    description: "yee haw!",
    title: "test link!",
    content: "green ham. green ham.",
  }

  act(() => {
    render(<AttachmentPost post={post} />, container);
  });

  expect(container.querySelector("p").textContent).toBe(post.description);
  expect(container.querySelector("a").download).toBe(post.title);
});

it("plain TextPost renders correctly", async () => {
  const post = {
    description: "yee haw!",
    title: "test link!",
    content: "green ham. green ham.",
    contentType: "text/plain",
  }

  act(() => {
    render(<TextPost post={post} />, container);
  });

  expect(container.querySelector("p").textContent).toBe(post.content);
});

it("markdown TextPost renders correctly", async () => {
  const post = {
    description: "yee haw!",
    title: "test link!",
    content: "green **ham**. green ham.",
    contentType: "text/markdown",
  }

  act(() => {
    render(<TextPost post={post} />, container);
  });

  expect(container.querySelector(".textPostContainer").innerHTML).toEqual("<p>green <strong>ham</strong>. green ham.</p>\n");
});


it("ImagePost renders correctly", async () => {
  const post = {
    title: "test link!",
    content: "https://mms.businesswire.com/media/20210511005474/en/877537/5/epic_logo_blue_RGB_%281%29.jpg",
  }

  act(() => {
    render(<ImagePost post={post} />, container);
  });

  expect(container.querySelector("img").src).toEqual(post.content);
});

