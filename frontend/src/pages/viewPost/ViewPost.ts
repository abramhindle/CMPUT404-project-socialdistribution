import { Page } from "../Page";
import {attr, observable} from "@microsoft/fast-element";
import {SocialApi} from "../../libs/api-service/SocialApi";
import {Post} from "../../libs/api-service/SocialApiModel";

export class ViewPost extends Page {
  @observable
  public post?: Post;

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
}
