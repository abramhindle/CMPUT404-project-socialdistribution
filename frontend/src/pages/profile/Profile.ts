import { SocialApi } from "../../libs/api-service/SocialApi";
import { SocialApiFollowers } from "../../libs/api-service/SocialApiFollowers";
import { Author } from "../../libs/api-service/SocialApiModel";
import { FollowStatus } from "../../libs/core/PageModel";
import { Page } from "../Page";

export class Profile extends Page {
    public profile?: Author | null;

    public followStatus: FollowStatus = FollowStatus.Unknown;

    constructor() {
        super();
        const profileId = this.getAttribute("profileId");
        this.removeAttribute("profileId");
        if (profileId) {
            this.resetProfile(profileId);
        }
    }

    public openEditModal() {

    }

    public followRequest() {
        try {
            let responseData;
            switch (this.followStatus) {
                case FollowStatus.NotFollowing:
                    responseData = await SocialApiFollowers.checkFollowing;
            }
            responseData = await SocialApiFollowers.;
            if (responseData && responseData.username == formData.get("username") && responseData.display_name == formData.get("display_name")) {
                window.location.replace("/login/");
            }
        } catch (e) {
            this.pushErrorMessages(e as string[]);
        }
    }

    public getFollowStatus(): string {
        switch (this.followStatus) {
            case FollowStatus.FollowRequest:
                return "Follow Request...";
            case FollowStatus.Following:
                return "Following";
            case FollowStatus.NotFollowing:
                return "Follow";
            default:
                return "";
        }
    }

    private async resetProfile(profileId: string | null) {
        if (!profileId) {
            return;
        }

        try {
            this.user = await SocialApi.fetchAuthor(profileId);
            if (this.user) {
                try {
                    const followStatus = await SocialApiFollowers.checkFollowing(profileId, this.user?.id);
                    if (followStatus) {
                        this.followStatus = FollowStatus.Following
                    }
                } catch (e) {
                    // Catch check following errors, error means not following or unauth
                    this.followStatus = FollowStatus.NotFollowing;
                }
            }
        } catch (e) {
            console.warn(e);
        }
    }
}