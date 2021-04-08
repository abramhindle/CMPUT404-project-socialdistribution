import { Image, message } from "antd";
import ReactMarkdown from "react-markdown";
import {
  getAuthorByAuthorID,
  getRemoteAuthorByAuthorID,
} from "../requests/requestAuthor";
import { getFollower, getFollowerList } from "../requests/requestFollower";
import { sendPost, sendPostToUserInbox } from "../requests/requestPost";
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

async function getLikeDataSet(likeData) {
  const likeArray = [];
  for (const like of likeData) {
    const host = getHostname(like.author);
    let authorInfo;
    if (host !== window.location.hostname) {
      authorInfo = await getRemoteAuthorByAuthorID({
        URL: like.author,
        auth: auth,
      });
    } else {
      authorInfo = await getAuthorByAuthorID({
        authorID: like.author,
      });
    }
    likeArray.push({
      authorName: authorInfo.data.displayName,
      authorID: authorInfo.data.id,
      summary: like.summary,
    });
  }
  return likeArray;
}
/**
 *
 * @param {*} url example: "https://social-distribution-t1.herokuapp.com/authorID/akdjflakjfdj"
 * @returns host: "social-distribution-t1.herokuapp.com"
 */
const getHostname = (url) => {
  // use URL constructor and return hostname
  return new URL(url).hostname;
};

/**
 *
 * @param {*} url example: "https://social-distribution-t1.herokuapp.com/authorID/akdjflakjfdj"
 * @returns domain name: "https://social-distribution-t1.herokuapp.com"
 */
const getDomainName = (url) => {
  return new URL(url).origin;
};

async function sendPostAndAppendInbox(params) {
  //create a post object
  sendPost(params).then((response) => {
    if (response.status === 200) {
      const postData = response.data;
      postData.type = "post";

      //if public, send to followers' inbox
      if (params.visibility) {
        getFollowerList({ object: params.authorID }).then((res) => {
          if (res.data.items.length !== 0) {
            for (const follower_id of res.data.items) {
              //send inbox
              let params_ = {
                URL: `${follower_id}/inbox/`,
                auth: auth,
                body: postData,
              };
              sendPostToUserInbox(params_).then((response) => {
                if (response.status === 200) {
                  message.success("Post shared!");
                } else {
                  message.error("Whoops, an error occurred while sharing.");
                }
              });
            }
          }
        });
      } else {
        //if private, send to friends' inbox
        getFollowerList({ object: params.authorID }).then((res) => {
          if (res.data.items.length !== 0) {
            for (const follower_id of res.data.items) {
              let host = getHostname(follower_id);
              let n = params.authorID.indexOf("/author/");
              let length = params.authorID.length;
              let param = {
                actor: params.authorID.substring(n + 8, length),
                object: follower_id,
              };
              if (host !== window.location.hostname) {
                // remote
                param.remote = true;
                param.auth = auth;
                getFollower(param).then((response) => {
                  if (response.data.exist) {
                    //send to friend inbox
                    let params_ = {
                      URL: `${follower_id}/inbox/`,
                      auth: auth,
                      body: postData,
                    };
                    sendPostToUserInbox(params_).then((response) => {
                      if (response.status === 200) {
                        message.success("Post shared!");
                      } else {
                        message.error(
                          "Whoops, an error occurred while sharing."
                        );
                      }
                    });
                  }
                });
              } else {
                param.auth = auth;
                param.remote = false;
                getFollower(param).then((response) => {
                  if (response.data.exist) {
                    // send to friend inbox
                    let params_ = {
                      URL: `${follower_id}/inbox/`,
                      auth: auth,
                      body: postData,
                    };
                    sendPostToUserInbox(params_).then((response) => {
                      if (response.status === 200) {
                        message.success("Post shared!");
                      } else {
                        message.error(
                          "Whoops, an error occurred while sharing."
                        );
                      }
                    });
                  }
                });
              }
            }
          }
        });
      }
      message.success("Post sent!");
      window.location.href = "/";
    } else {
      message.error("Post failed!");
    }
  });
}

export {
  getPostDataSet,
  getFriendDataSet,
  getLikeDataSet,
  getHostname,
  getDomainName,
  sendPostAndAppendInbox,
};
