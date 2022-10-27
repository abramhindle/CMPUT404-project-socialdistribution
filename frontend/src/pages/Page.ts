import { FASTElement, observable } from "@microsoft/fast-element";
import { SocialApi } from "../libs/api-service/SocialApi";
import { Author } from "../libs/api-service/SocialApiModel";
import { LayoutType } from "../libs/core/PageModel";

export class Page extends FASTElement {
    @observable
    public user?: Author | null;

    @observable
    public layoutType: LayoutType = LayoutType.Desktop;

    @observable
    private vw = Math.min(document.documentElement.clientWidth || 0, window.innerWidth || 0, window.visualViewport?.width || 0);


    constructor() {
        super();
        const isAuth = this.getAttribute("auth") == "True" ? true : false;
        const userId = this.getAttribute("userId");
        this.removeAttribute("auth");
        this.removeAttribute("userId");
        if (isAuth) {
            this.resetAuthor(userId);
        }

        const page = this;
        this.setLayoutType();
        
        // Update vw and vh on resize;
        window.addEventListener("resize", function () {
            page.vw = Math.min(document.documentElement.clientWidth || 0, window.innerWidth || 0, window.visualViewport?.width || 0);
            page.setLayoutType();
        })
    }

    private setLayoutType() {
        if (this.vw >= 1200) {
            this.layoutType = LayoutType.Desktop
        } else if (this.vw >= 768) {
            this.layoutType = LayoutType.Tablet
        } else {
            this.layoutType = LayoutType.Mobile
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