import { attr, FASTElement, observable, volatile } from "@microsoft/fast-element";
import { SocialApi } from "../libs/api-service/SocialApi";
import { Author } from "../libs/api-service/SocialApiModel";

export class Page extends FASTElement {
    @observable
    public user?: Author | null;

    constructor() {
        super();
        const isAuth = this.getAttribute("auth") == "True" ? true : false;
        const userId = this.getAttribute("userId");
        this.removeAttribute("auth");
        this.removeAttribute("userId");
        if (isAuth) {
            this.resetAuthor(userId);
        }
    }

    private async resetAuthor(userId: string | null) {
        if (!userId) {
            return;
        }

        try {
            this.user = await SocialApi.fetchAuthor(userId);
            console.log(this.user);
        } catch (e) {
            console.warn(e);
        }
    }
}