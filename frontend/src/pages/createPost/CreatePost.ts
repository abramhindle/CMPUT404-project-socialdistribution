import { Page } from "../Page";
import { SocialApi } from "../../libs/api-service/SocialApi";

export class CreatePost extends Page {

  public form?: HTMLFormElement;

  public connectedCallback() {
    super.connectedCallback();
  }

  public async createPost(e: Event) {
    e.preventDefault();

    if (!this.form) {
      return;
    }

    if(!this.userId) {
      return;
    }

    const formData = new FormData(this.form);
    try {
      formData.append("unlisted", "false");
      if (this.user) {
        const responseData = await SocialApi.createPost(this.userId, formData);
        if (responseData) {
          const url = new URL("/view-post/" + this.userId + "/" + responseData.id, window.location.origin);
          window.location.replace(url);
        } else throw new Error("Null post");
      } else throw new Error("Null user");
    } catch (e) {
      console.error(e);
    }
  }
}
