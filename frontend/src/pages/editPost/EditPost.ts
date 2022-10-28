import { Page } from "../Page";
import {SocialApi} from "../../libs/api-service/SocialApi";
import {SocialApiUrls} from "../../libs/api-service/SocialApiUrls";
import {observable} from "@microsoft/fast-element";
import {Post} from "../../libs/api-service/SocialApiModel";

export class EditPost extends Page {
  @observable
  public post?: Post;

  private postId?: string;

  public form?: HTMLFormElement;

  @observable
  public loadedPostText: string = "";

  public constructor() {
    super();

    if (this.profileId != this.userId) {
      window.location.replace("/");
    }

    const postId = this.getAttribute("postId");
    this.removeAttribute("postId");
    if (postId) {
      this.postId = postId;
      this.getPost(postId);
    } else {
      window.location.replace("/");
    }
  }

  public connectedCallback() {
    super.connectedCallback();
  }

  private async getPost(postId: string) {
    if (!this.profileId) {
      return;
    }

    try {
      const post = await SocialApi.fetchPost(postId, this.profileId);
      if (post) {
        this.post = post;
      } else throw new Error("Null Post");
    } catch (e) {
      console.error(e);
      this.loadedPostText = "Post not found."
    }
  }

  public async editPost(e: Event) {
    e.preventDefault();

    if (!this.form) {
      return;
    }

    if (!this.userId) {
      return;
    }

    const formData = new FormData(this.form);
    try {
      formData.append("description", "My post description");
      formData.append("unlisted", "false");
      if (this.user) {
        if (this.postId) {
          const responseData = await SocialApi.updatePost(this.postId, this.userId, formData);
          if (responseData) {
            const url = new URL("/view-post/" + this.profileId + "/" + this.postId, window.location.origin);
            window.location.replace(url);
          }
        }
      }
    } catch (e) {
      console.error(e);
    }
  }

  public async deletePost() {
    try {
      if (this.user) {
        if (this.postId) {
          const responseData = await SocialApi.deletePost(this.user.id, this.postId);
          console.log(responseData);
          if (responseData && responseData.message == 'Object deleted!') {
            window.location.replace("/");
          }
        }
      }
    } catch (e) {
      console.warn(e);
    }
  }
}
