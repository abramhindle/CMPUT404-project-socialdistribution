import { SocialApi } from "./SocialApi";
import { SocialApiUrls } from "./SocialApiUrls";

export namespace SocialApiFollowers {
    export async function checkFollowing(authorId: string, foreignAuthorId: string): Promise<any> {
        const url = new URL(SocialApiUrls.AUTHORS + authorId + SocialApiUrls.FOLLOWERS + foreignAuthorId + "/", window.location.origin)

        return SocialApi.fetchAuthorized(url, "GET");
    }

    export async function acceptFollowing(authorId: string, foreignAuthorId: string): Promise<any> {
        const url = new URL(SocialApiUrls.AUTHORS + authorId + SocialApiUrls.FOLLOWERS + foreignAuthorId + "/", window.location.origin)

        return SocialApi.fetchAuthorized(url, "PUT");
    }

    export async function removeFollowing(authorId: string, foreignAuthorId: string): Promise<any> {
        const url = new URL(SocialApiUrls.AUTHORS + authorId + SocialApiUrls.FOLLOWERS + foreignAuthorId + "/", window.location.origin)

        return SocialApi.fetchAuthorized(url, "DELETE");
    }

    export async function declineFollowRequest(authorId: string, foreignAuthorId: string): Promise<any> {
        const url = new URL(SocialApiUrls.AUTHORS + authorId + SocialApiUrls.FOLLOW_REQUESTS + foreignAuthorId + "/", window.location.origin)

        return SocialApi.fetchAuthorized(url, "DELETE");
    }
}