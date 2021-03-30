import { Image } from "antd";
import ReactMarkdown from "react-markdown";
import {
  getAuthorByAuthorID,
  getRemoteAuthorByAuthorID,
} from "../requests/requestAuthor";
import { auth } from "../requests/URL";

async function getPostDataSet(postData) {
  const publicPosts = [];
  for (const element of postData) {
    const host = getHostname(element.author);
    let contentHTML = <p>{element.content}</p>;
    if (element.contentType !== undefined) {
      const isImage =
        element.contentType.slice(0, 5) === "image" ? true : false;
      const isMarkDown =
        element.contentType.slice(5) === "markdown" ? true : false;
      if (isImage) {
        contentHTML = <Image width={150} src={element.content} />;
      } else if (isMarkDown) {
        contentHTML = <ReactMarkdown source={element.content} />;
      }
    }
    let res;
    if (host !== window.location.hostname) {
      // remote
      res = await getRemoteAuthorByAuthorID({
        URL: element.author,
        auth: auth,
      });
    } else {
      res = await getAuthorByAuthorID({ authorID: element.author });
    }
    let rawPost = element;
    rawPost["authorName"] = res.data.displayName;
    const obj = {
      title: element.title,
      content: <div style={{ margin: "24px" }}>{contentHTML}</div>,
      datetime: <span>{element.published}</span>,
      postID: element.id,
      authorName: res.data.displayName,
      github: res.data.github,
      categories: element.categories,
      rawPost: rawPost,
      remote: false,
    };
    if (host !== window.location.hostname) {
      obj.remote = true;
    }
    publicPosts.push(obj);
  }
  return publicPosts;
}

async function getFriendDataSet(friendList) {
  const friendDataSet = [];
  for (const item of friendList) {
    const host = getHostname(item);
    let author;
    if (host !== window.location.hostname) {
      author = await getRemoteAuthorByAuthorID({
        URL: item,
        auth: auth,
      });
    } else {
      author = await getAuthorByAuthorID({ authorID: item });
    }
    const obj = {
      displayName: author.data.displayName,
      github: author.data.github,
      id: author.data.id,
    };
    friendDataSet.push(obj);
  }
  return friendDataSet;
}

const getHostname = (url) => {
  // use URL constructor and return hostname
  return new URL(url).hostname;
};

export { getPostDataSet, getFriendDataSet, getHostname };
