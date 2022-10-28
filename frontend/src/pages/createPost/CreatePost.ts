import { Page } from "../Page";
import {SocialApi} from "../../libs/api-service/SocialApi";
import {SocialApiUrls} from "../../libs/api-service/SocialApiUrls";

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
