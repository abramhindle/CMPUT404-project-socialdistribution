import { FASTElement, observable } from "@microsoft/fast-element";
import { Post } from "../../libs/api-service/SocialApiModel";

export class FeedPost extends FASTElement {
    @observable
    public post?: Post;

    public getPostUrl(): string {
        if (!this.post || !this.post.author) {
            return "/";
        }

        const url = new URL("/view-post/" + this.post.author.id + "/" + this.post.id, window.location.origin);
        
        return url.toString();
    }

    public getAuthorUrl(authorId?: string) {
        if (!this.post || !this.post.author || !authorId) {
            return "/";
        }

        const url = new URL("/profile/" + authorId, window.location.origin);
        
        return url.toString();
    }
}