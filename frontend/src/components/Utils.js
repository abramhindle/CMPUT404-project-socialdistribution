import { Image } from "antd";
import ReactMarkdown from "react-markdown";
import {
  getAuthorByAuthorID,
  getRemoteAuthorByAuthorID,
} from "../requests/requestAuthor";
import { auth } from "../requests/URL";

function getPostDataSet(postData, remote) {
  let promise = new Promise(async (resolve, reject) => {
    const publicPosts = [];
    for (const element of postData) {
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
      if (remote) {
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
      if (remote) {
        obj.remote = true;
      }
      publicPosts.push(obj);
    }
    resolve(publicPosts);
  });
  return promise;
}

async function getFriendDataSet(friendList, remote) {
  const friendDataSet = [];
  for (const item of friendList) {
    let author;
    if (remote) {
      // remote
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

export { getPostDataSet, getFriendDataSet };
