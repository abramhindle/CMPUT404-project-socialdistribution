import { rgbToHSL } from "@microsoft/fast-colors";
import { attr, FASTElement, observable } from "@microsoft/fast-element";
import { SocialApi } from "../../libs/api-service/SocialApi";
import { Author } from "../../libs/api-service/SocialApiModel";
import { SocialApiTransform } from "../../libs/api-service/SocialApiTransform";

type Like = {
  author: Author,
  post: string
}

export class LikesModal extends FASTElement {
  @attr greeting: string = 'Likes Modal';

  @observable
  public postId?: string;

  @observable
  public postAuthorId?: string;

  @observable
  public user?: Author;

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
      const response = await SocialApi.getPostLikes(postId, postAuthorId);
      if (response) {
        this.setLikes(response)
      }
    } catch (e) {
      console.error(e);
    }
  }

  private setLikes(responseData: any) {
    if (!responseData) {
      return;
    }

    // Clear likes
    this.likes.splice(0, this.likes.length);

    for (var data of responseData) {
      const newLike: any = {}
      const author = SocialApiTransform.authorDataTransform(data.author);
      if (author) {
        newLike["author"] = author
      }
      newLike["post"] = data.post
      this.likes.push(newLike)
    }
  }
}


