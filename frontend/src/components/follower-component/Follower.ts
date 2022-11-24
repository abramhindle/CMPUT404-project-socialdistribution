import { attr, FASTElement, observable } from "@microsoft/fast-element";
import { SocialApiFollowers } from "../../libs/api-service/SocialApiFollowers";
import { Author, FollowDecisionBody, FollowInfo, FollowRemovalBody, FollowRequestBody } from "../../libs/api-service/SocialApiModel";
import { FollowStatus } from "../../libs/core/PageModel";

export class Follower extends FASTElement {
    @observable
    public profile?: Author;

    @observable
    public user?: Author;

    @observable
    public layoutStyleClass: string = "";

    @observable
    public followStatus: FollowStatus = FollowStatus.Unknown;

    @observable
    public request = false;

    // remove self from page when it would no longer show up in the inbox
    @observable
    public isDeleted = false;

    constructor() {
        super();
        console.log(this.layoutStyleClass)
    }

    userChanged(oldValue: Author, newVal: Author) {
        this.getFollowStatus();
    }

    profileChanged(oldValue: Author, newVal: Author) {
        this.getFollowStatus();
    }

    public async getFollowStatus() {
        if (!this.profile?.id || !this.user?.id) {
            return;
        }

        if (this.profile?.id == this.user.id) {
            return;
        }

        try {
            const followStatus = await SocialApiFollowers.checkFollowing(this.profile?.id, this.user.id);
            if (followStatus) {
                this.followStatus = FollowStatus.Following;
            }
        } catch (e) {
            // Catch check following errors, error means not following or unauth
            this.followStatus = FollowStatus.NotFollowing;
        }
    }

    public async followRequest() {
        if (!this.user?.url || !this.profile?.url) {
            return;
        }

        try {
            if (this.followStatus == FollowStatus.NotFollowing) {
                const followRequest = new FollowRequestBody();
                followRequest.sender = new FollowInfo(this.user.url, this.user.id);
                followRequest.receiver = new FollowInfo(this.profile.url, this.profile.id);

                const responseData = await SocialApiFollowers.sendFollowRequest(this.profile.id, followRequest);
                if (responseData) {
                    // we know the request went through, they still have to accept it
                    this.followStatus = FollowStatus.Sent;
                }
            } else if (this.followStatus == FollowStatus.Following) {
                const followRemoval = new FollowRemovalBody();
                followRemoval.follower = new FollowInfo(this.user.url, this.user.id);

                const responseData = await SocialApiFollowers.removeFollowing(this.profile.id, this.user.id, followRemoval);
                if (responseData) {
                    // successfully removed as follower
                    this.followStatus = FollowStatus.NotFollowing;
                }
            }
        } catch (e) {
            // Follow request or removal failed
            console.warn(e)
        }
    }

    public async acceptRequest() {
        await this.getFollowStatus();
        if (!this.user?.url || !this.profile?.url) {
            return;
        }

        if (!this.request) {
            return;
        }

        try {
            const followDecision = new FollowDecisionBody();
            followDecision.follow_request_sender = new FollowInfo(this.profile.url, this.profile.id);

            const responseData = await SocialApiFollowers.acceptFollowing(this.user.id, this.profile.id, followDecision);
            if (responseData) {
                // successfully accepted request
                this.isDeleted = true;
            }
        } catch (e) {
            // Accepting follow request failed
            console.warn(e)
        }
    }

    public async declineRequest() {
        await this.getFollowStatus();
        if (!this.user?.url || !this.profile?.url) {
            return;
        }

        if (!this.request) {
            return;
        }

        try {
            const followDecision = new FollowDecisionBody();
            followDecision.follow_request_sender = new FollowInfo(this.profile.url, this.profile.id);

            const responseData = await SocialApiFollowers.declineFollowRequest(this.user.id, this.profile.id, followDecision);
            if (responseData) {
                // successfully declined request
                this.isDeleted = true;
            }
        } catch (e) {
            // Follow decline failed
            console.warn(e)
        }
    }
}