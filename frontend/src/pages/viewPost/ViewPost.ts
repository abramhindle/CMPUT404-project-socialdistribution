import { Page } from "../Page";
import { observable } from "@microsoft/fast-element";
import { SocialApi } from "../../libs/api-service/SocialApi";
import { Post } from "../../libs/api-service/SocialApiModel";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faThumbsUp } from "@fortawesome/free-solid-svg-icons";

export class ViewPost extends Page {
  @observable
  public post?: Post;

  @observable
  public loadedPostText: string = "";

  @observable
  public viewLikes: Boolean = false;

  @observable
  public postId?: string;

  public constructor() {
    super();
    const postId = this.getAttribute("postId");
    this.removeAttribute("postId");
    if (postId) {
      this.postId = postId;
      this.getPost(postId);
    }

    this.addIcons();
  }

  public connectedCallback() {
    super.connectedCallback();
  }

  private addIcons() {
    library.add(faThumbsUp);
  }

  private async getPost(postId: string) {
    if (!this.profileId) {
      return;
    }

    try {
      const post = await SocialApi.fetchPost(postId, this.profileId);
      if (post) {
        this.post = post;
      }
    } catch (e) {
      console.error(e);
      this.loadedPostText = "Post not found.";
    }

    console.log("loaded", this.post?.id, this.user)
  }

  public async likePost() {
    if (!this.post || !this.post.author || !this.post.author.url) {
      console.error("Post must have an author with an author url");
      return;
    }

    if (!this.user || !this.user.url) {
      console.error("Current user must have a url");
      return;
    }

    try {
      const res = await SocialApi.likePost(
        this.post.id,
        this.user.id,
        this.user.url,
        this.post.author.id,
        this.post.author.url
      );
    } catch (e) {
      console.error(e);
    }
  }

  public async toggleModal() {
    console.log("Modal toggled, new value:", !this.viewLikes);
    this.viewLikes = !this.viewLikes
  }
}
