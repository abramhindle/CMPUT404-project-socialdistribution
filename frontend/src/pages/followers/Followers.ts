import { SocialApi } from "../../libs/api-service/SocialApi";
import { SocialApiFollowers } from "../../libs/api-service/SocialApiFollowers";
import { Author, FollowInfo, FollowRequestBody, PaginatedResponse } from "../../libs/api-service/SocialApiModel";
import { FollowStatus } from "../../libs/core/PageModel";
import { Page } from "../Page";
import { observable } from "@microsoft/fast-element";
import { SocialApiTransform } from "../../libs/api-service/SocialApiTransform";
import { PaginatedPage } from "../PaginatedPage";

const PAGE_SIZE = 20;

export class Followers extends Page {
    @observable
    public followers: Author[] = [];

    constructor() {
        super();
        if (this.profileId) {
            this.getResults();
        }
    }

    protected async getResults() {
        if (!this.profileId) {
            return;
        }

        try {
            const responseData = await SocialApi.fetchPaginatedFollowers(this.profileId, 1, PAGE_SIZE);
            console.log(responseData)
            if (responseData && Array.isArray(responseData)) {
                for (var authorData of responseData) {
                    const author = SocialApiTransform.authorDataTransform(authorData);
                    if (author) {
                        this.followers.push(author);
                    }
                }
            }
        } catch (e) {
            console.error("Follower fetch failed", e);
        }
    }
}