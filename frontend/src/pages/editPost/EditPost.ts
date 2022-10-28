import { Page } from "../Page";
import {SocialApi} from "../../libs/api-service/SocialApi";
import {SocialApiUrls} from "../../libs/api-service/SocialApiUrls";
import {observable} from "@microsoft/fast-element";
import {Post} from "../../libs/api-service/SocialApiModel";

export class EditPost extends Page {
  @observable
  public post?: Post;

  private postId: string | undefined;

  public form?: HTMLFormElement;

  public constructor() {
    super();

    const postId = this.getAttribute("postId");
    this.removeAttribute("postId");
    const authorId = this.getAttribute("authorId");
    this.removeAttribute("authorId");
    if (authorId && postId) {
      this.postId = postId;
      this.getPost(authorId, postId);
      // TODO: redirect to home if the post doesn't exist
    }
  }

  public connectedCallback() {
    super.connectedCallback();
  }

  private async getPost(authorId: string, postId: string) {
    try {
      const post = await SocialApi.fetchPost(postId, authorId);
      if (post) {
        this.post = post;
      } else throw new Error("Null Post");
    } catch (e) {
      console.error(e);
    }
  }

  public async editPost(e: Event) {
    e.preventDefault();

    if (!this.form) {
      return;
    }

    const formData = new FormData(this.form);
    try {
      formData.append("description", "My post description");
      formData.append("unlisted", "false");
      if (this.user) {
        if (this.postId) {
          const responseData = await SocialApi.updatePost(this.postId, this.user.id, formData);
          if (responseData) {
            const url = new URL(
              SocialApiUrls.AUTHORS + this.user.id + SocialApiUrls.POSTS + responseData.id,
              window.location.origin
            );
            window.location.replace(url);
          } else throw new Error("Null post");
        } else throw new Error("Null post id");
      } else throw new Error("Null user");
    } catch (e) {
      console.error(e);
    }
  }

  public async deletePost() {
    try {
      if (this.user) {
        if (this.postId) {
          const responseData = await SocialApi.deletePost(this.user.id, this.postId);
          if (responseData && responseData[0]?.message === 'object deleted') {
            window.location.replace(window.location.origin);
          } else throw new Error("Failed to delete post");
        }
      }
    } catch (e) {
      console.error(e);
    }
  }
}
