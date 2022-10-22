import { FASTElement, observable } from "@microsoft/fast-element";
import { Author } from "../libs/api-service/SocialApiModel";

export class Page extends FASTElement {
    public user?: Author | null;

    public connectedCallback() {
        super.connectedCallback();
        const isAuth = this.getAttribute("auth") == "True" ? true : false;
        const userId = this.getAttribute("userId");
        this.removeAttribute("auth");
        this.removeAttribute("userId");
    }
}