import { Page } from "../Page";
import { attr, observable } from "@microsoft/fast-element";
import { SocialApi } from "../../libs/api-service/SocialApi";
import { Post } from "../../libs/api-service/SocialApiModel";

export class ViewPost extends Page {
  @observable
  public post?: Post;

  public constructor() {
    super();
    const postId = this.getAttribute("postId");
    this.removeAttribute("postId");
    if (postId) {
      this.getPost(postId);
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
    }
  }
}
