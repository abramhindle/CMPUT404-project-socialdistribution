import { SocialApi } from "./SocialApi";
import { FollowDecisionBody, FollowRemovalBody, FollowRequestBody } from "./SocialApiModel";
import { SocialApiUrls } from "./SocialApiUrls";

export namespace SocialApiFollowers {
    export async function checkFollowing(authorId: string, foreignAuthorId: string): Promise<any> {
        const url = new URL(SocialApiUrls.AUTHORS + authorId + SocialApiUrls.FOLLOWERS + foreignAuthorId + "/", window.location.origin)

        return SocialApi.fetchAuthorized(url, "GET");
    }

    export async function sendFollowRequest(receiverId: string, followRequest: FollowRequestBody): Promise<any> {
        const url = new URL(SocialApiUrls.AUTHORS + receiverId + SocialApiUrls.INBOX, window.location.origin)

        return SocialApi.fetchAuthorized(url, "POST", JSON.stringify(followRequest));
    }

    export async function acceptFollowing(authorId: string, foreignAuthorId: string, followDecision: FollowDecisionBody): Promise<any> {
        const url = new URL(SocialApiUrls.AUTHORS + authorId + SocialApiUrls.FOLLOWERS + foreignAuthorId + "/", window.location.origin)

        return SocialApi.fetchAuthorized(url, "PUT", JSON.stringify(followDecision));
    }

    export async function removeFollowing(authorId: string, foreignAuthorId: string, followRemoval: FollowRemovalBody): Promise<any> {
        const url = new URL(SocialApiUrls.AUTHORS + authorId + SocialApiUrls.FOLLOWERS + foreignAuthorId + "/", window.location.origin)

        return SocialApi.fetchAuthorized(url, "DELETE", JSON.stringify(followRemoval));
    }

    export async function declineFollowRequest(authorId: string, foreignAuthorId: string, followDecision: FollowDecisionBody): Promise<any> {
        const url = new URL(SocialApiUrls.AUTHORS + authorId + SocialApiUrls.FOLLOW_REQUESTS + foreignAuthorId + "/", window.location.origin)

        return SocialApi.fetchAuthorized(url, "DELETE", JSON.stringify(followDecision));
    }
}