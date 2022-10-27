import { FASTElement, observable } from "@microsoft/fast-element";
import { Post } from "../../../../libs/api-service/SocialApiModel";
import { SocialApiUrls } from "../../../../libs/api-service/SocialApiUrls";

export class FeedPost extends FASTElement {
    @observable
    public post?: Post;

    public getPostUrl(): string {
        if (!this.post || !this.post.author) {
            return "/";
        }

        const url = new URL(
            "/posts/", window.location.origin);
        url.searchParams.append("id", this.post.id);
        
        return url.toString();
    }
}