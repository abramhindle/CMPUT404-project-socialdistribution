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
  public userId?: string;

  @observable
  public likes: Like[] = [];

  @observable
  public parent: any

  public constructor() {
    super();
  }


  public connectedCallback() {
    super.connectedCallback();
    console.log("Connected Callback", this.parent, this.postId, this.userId);
    this.getLikes(<string>this.postId, <string>this.userId);
  }

  public async getLikes(postId: string, userId: string) {
    console.log("Info:", postId, userId);
    if (!postId) {
      console.error("Post must have an id");
      return;
    }

    if (!userId) {
      console.error("User must have an id");
      return;
    }

    try {
      this.likes = await SocialApi.getPostLikes(postId, userId);
    } catch (e) {
      console.error(e);
    }
  }
}
