import {attr, FASTElement, observable} from "@microsoft/fast-element";
import {SocialApi} from "../../libs/api-service/SocialApi";
import {Author, Post} from "../../libs/api-service/SocialApiModel";
import {Page} from "../../pages/Page";

type Like = {
  author: {
    url: string,
    id: string,
    display_name: string,
    profile_image: string,
    github_handle: string
  },
  post: string
}

export class LikesModal extends FASTElement {
  @attr greeting: string = 'Likes Modal';

  @observable
  public postId?: string;

  @observable
  public postAuthorId?: string;

  @observable
  public likes: Like[] = [];

  @observable
  public parent: any

  public constructor() {
    super();
  }


  public connectedCallback() {
    super.connectedCallback();
    console.log("Connected Callback", this.parent, this.postId, this.postAuthorId);
    this.getLikes(<string>this.postId, <string>this.postAuthorId);
  }

  public async getLikes(postId: string, postAuthorId: string) {
    console.log("Info:", postId, postAuthorId);
    if (!postId) {
      console.error("Post must have an id");
      return;
    }

    if (!postAuthorId) {
      console.error("User must have an id");
      return;
    }

    try {
      this.likes = await SocialApi.getPostLikes(postId, postAuthorId);
    } catch (e) {
      console.error(e);
    }
  }
}
