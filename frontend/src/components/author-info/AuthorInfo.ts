import { FASTElement, observable } from "@microsoft/fast-element";
import { Author } from "../../libs/api-service/SocialApiModel";

export class AuthorInfo extends FASTElement {
    @observable
    public authorId?: string;

    @observable
    public author?: Author

    @observable
    public published?: Date;

    public getAuthorUrl(authorId?: string) {
        if (!this.authorId) {
            return "/";
        }

        const url = new URL("/profile/" + authorId, window.location.origin);
        
        return url.toString();
    }
}