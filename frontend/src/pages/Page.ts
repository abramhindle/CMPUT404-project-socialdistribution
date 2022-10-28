import { FASTElement, observable } from "@microsoft/fast-element";
import { layoutComponent } from "../components/base-layout";
import { SocialApi } from "../libs/api-service/SocialApi";
import { SocialApiFollowers } from "../libs/api-service/SocialApiFollowers";
import { Author } from "../libs/api-service/SocialApiModel";
import { FollowStatus, LayoutType } from "../libs/core/PageModel";

layoutComponent;

export abstract class Page extends FASTElement {
    public readonly userId: string | null;

    @observable
    public user: Author | null;

    public readonly profileId: string | null;

    @observable
    public profile?: Author | null;

    @observable
    public followStatus: FollowStatus = FollowStatus.Unknown;

    @observable
    public loadedProfileText: string = "";

    @observable
    public layoutType: LayoutType = LayoutType.Desktop;

    @observable
    private vw = Math.min(document.documentElement.clientWidth || 0, window.innerWidth || 0, window.visualViewport?.width || 0);


    constructor() {
        super();
        this.user = null;
        this.profile = null;

        // Get attributes from html tag made by django
        const isAuth = this.getAttribute("auth") == "True" ? true : false;
        const userId = this.getAttribute("userId");
        this.removeAttribute("auth");
        this.removeAttribute("userId");

        if (isAuth && userId) {
            this.userId = userId
            this.resetAuthor();
        } else {
            this.userId = null;
        }

        // profile info (if not user)
        const profileId = this.getAttribute("profileId");
        this.removeAttribute("profileId");
        if (profileId) {
            this.profileId = profileId;
            this.resetProfile();
        } else {
            this.profileId = null;
        }
        

        this.setLayoutType();
        
        // Update vw and vh on resize;
        const page = this;
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

    private async resetAuthor() {
        if (!this.userId) {
            return;
        }

        try {
            this.user = await SocialApi.fetchAuthor(this.userId);
            console.log(this.user);
            if (this.profileId == this.userId) {
                this.profile = this.user;
                return;
            }
        } catch (e) {
            console.warn(e);
        }
    }

    private async resetProfile() {
        if (!this.profileId) {
            return;
        }

        if (this.profileId == this.userId) {
            return;
        }

        try {
            this.profile = await SocialApi.fetchAuthor(this.profileId);
            console.log(this.profile)
            if (this.profile && this.userId) {
                try {
                    const followStatus = await SocialApiFollowers.checkFollowing(this.profileId, this.userId);
                    if (followStatus) {
                        this.followStatus = FollowStatus.Following
                    }
                } catch (e) {
                    // Catch check following errors, error means not following or unauth
                    this.followStatus = FollowStatus.NotFollowing;
                }
            }
        } catch (e) {
            this.loadedProfileText = "Profile not found.";
            console.warn(e);
        }
    }
}