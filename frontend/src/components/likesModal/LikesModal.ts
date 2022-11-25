import {attr, FASTElement, observable} from "@microsoft/fast-element";
import {SocialApi} from "../../libs/api-service/SocialApi";
import {Author, Post} from "../../libs/api-service/SocialApiModel";

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
  public post?: Post;

  @observable
  public user?: Author;

  @observable
  public likes: Like[]

  public constructor(props) {
    super();
    this.getLikes();
  }


  public connectedCallback() {
    super.connectedCallback();
  }

  public async getLikes() {
    if (!this.post || !this.post.id) {
      console.error("Post must have an id");
      return;
    }

    if (!this.user || !this.user.id) {
      console.error("User must have an id");
      return;
    }

    try {
      this.likes = await SocialApi.getPostLikes(this.post.id, this.user.id);
    } catch (e) {
      console.error(e);
    }
  }
}
