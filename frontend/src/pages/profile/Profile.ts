import { faCodePullRequest } from "@fortawesome/free-solid-svg-icons";
import { library } from "@fortawesome/fontawesome-svg-core";
import { observable } from "@microsoft/fast-element";
import { SocialApi } from "../../libs/api-service/SocialApi";
import { SocialApiFollowers } from "../../libs/api-service/SocialApiFollowers";
import { FollowInfo, FollowRemovalBody, FollowRequestBody } from "../../libs/api-service/SocialApiModel";
import { ImageHelpers } from "../../libs/core/Helpers";
import { FollowStatus } from "../../libs/core/PageModel";
import { Page } from "../Page";

export class Profile extends Page {
    public form?: HTMLFormElement;

    @observable
    public modalStateStyle = "modal-close";

    constructor() {
        super();
        this.addIcons()
    }

    public openEditModal() {
        this.modalStateStyle = "modal-open"
    }

    public closeEditModal() {
        this.modalStateStyle = "modal-close"
    }

    public async editProfile(e: Event) {
        e.preventDefault();
        this.closeEditModal();

        if (!this.form) {
            return;
        }
        
        if (!this.userId) {
            return;
        }

        if (this.profileId != this.userId) {
            return;
        }

        const formData = new FormData(this.form)
        formData.set("profile_image", this.user?.profileImage || "")
        
        // Convert image to base64 if it was uploaded
        if (formData.get("image")) {
            const base64 = await ImageHelpers.convertBase64(formData.get("image"));
            formData.delete("image")
            if (base64 && typeof base64 === 'string') {
                const imagePostData = new FormData();
                imagePostData.set("image", base64)

                let type = "image/jpeg;base64";
                if (base64.split(",").length > 0) {
                    type = base64.split(",")[0].slice(5)
                }
                imagePostData.set("content_type", type)

                try {
                    const responseData = await SocialApi.createPost(this.userId, imagePostData)
                    if (responseData && responseData.url) {
                        // Add new url to formData
                        formData.set("profile_image", responseData.url)
                    }
                } catch (e) {
                    console.warn(e)
                }
            }
        }

        try {
            const responseData = await SocialApi.editProfile(this.userId, formData);
            if (responseData && responseData.id == this.userId) {
                this.user = responseData;
                if (this.profileId == this.userId) {
                    this.profile = this.user;
                }
            }
        } catch (e) {
            console.warn(e)
        }
    }

    public async followRequest() {
        if (!this.user?.url || !this.profile?.url) {
            return;
        }

        if (!this.userId || !this.profileId) {
            return;
        }

        try {
            if (this.followStatus == FollowStatus.NotFollowing) {
                const followRequest = new FollowRequestBody();
                followRequest.sender = new FollowInfo(this.user.url, this.userId);
                followRequest.receiver = new FollowInfo(this.profile.url, this.profileId);

                const responseData = await SocialApiFollowers.sendFollowRequest(this.profileId, followRequest);
                if (responseData) {
                    // we know the request went through, they still have to accept it
                    this.followStatus = FollowStatus.Sent
                }
            } else if(this.followStatus == FollowStatus.Following) {
                const followRemoval = new FollowRemovalBody();
                followRemoval.follower = new FollowInfo(this.user.url, this.userId);

                const responseData = await SocialApiFollowers.removeFollowing(this.profileId, this.userId, followRemoval);
                if (responseData) {
                    this.followStatus = FollowStatus.NotFollowing
                }
            }
        } catch (e) {
            // Follow request or removal failed
            console.warn(e)
        }
    }

    private addIcons() {
        library.add(faCodePullRequest);
    }
}