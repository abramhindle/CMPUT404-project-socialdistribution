import { Page } from "../Page";
import {SocialApi} from "../../libs/api-service/SocialApi";
import {SocialApiUrls} from "../../libs/api-service/SocialApiUrls";
import {observable} from "@microsoft/fast-element";
import {Post} from "../../libs/api-service/SocialApiModel";

export class EditPost extends Page {

  @observable
  public post?: Post;

  public form?: HTMLFormElement;

  public constructor() {
    super();

    const postId = this.getAttribute("postId");
    this.removeAttribute("postId");
    const authorId = this.getAttribute("authorId");
    this.removeAttribute("authorId");
    if (authorId && postId) {
      this.getPost(postId, authorId);
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
      formData.append("content_type", "text/plain");
      if (this.user) {
        const responseData = await SocialApi.createPost(this.user.id, formData);
        if (responseData) {
          const url = new URL(
            SocialApiUrls.AUTHORS + this.user.id + SocialApiUrls.POSTS + responseData.id,
            window.location.origin
          );
          window.location.replace(url);
        } else throw new Error("Null post");
      } else throw new Error("Null user");
    } catch (e) {
      console.error(e);
    }
  }
}
