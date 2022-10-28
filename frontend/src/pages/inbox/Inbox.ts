import { observable } from "@microsoft/fast-element";
import { SocialApi } from "../../libs/api-service/SocialApi";
import { ApiObjectType, PaginatedResponse } from "../../libs/api-service/SocialApiModel";
import { SocialApiTransform } from "../../libs/api-service/SocialApiTransform";
import { PaginatedPage } from "../PaginatedPage";

const PAGE_SIZE = 10;

export class Inbox extends PaginatedPage {
    @observable
    public inbox: any[] = [];

    constructor() {
        super();
        if (this.userId) {
            this.getResults();
        }
    }

    protected async getResults() {
        if (!this.userId) {
            return;
        }

        try {
            let responseData: PaginatedResponse | null;

            if (this.paginatedResponse?.next) {
                responseData = await SocialApi.fetchPaginatedNext(this.paginatedResponse.next);
                console.log(responseData)
                if (responseData) {
                    this.paginatedResponse = responseData;
                    this.setVisibleInbox()
                }
            } else if (!this.paginatedResponse) {
                responseData = await SocialApi.fetchPaginatedInbox(this.userId, 1, PAGE_SIZE);
                console.log(responseData)
                if (responseData) {
                    this.paginatedResponse = responseData;
                    this.setVisibleInbox()
                    if (this.loadMore) {
                        this.observer?.observe(this.loadMore);
                    }
                }
            } else {
                responseData = this.paginatedResponse || null;
            }
        } catch (e) {
            console.error("Inbox fetch failed", e);
        }
    }

    private setVisibleInbox() {
        if (!this.paginatedResponse?.results) {
            return;
        }

        for (var data of this.paginatedResponse?.results) {
            if (data.type == ApiObjectType.post) {
                const post = SocialApiTransform.postDataTransform(data);
                if (post) {
                    this.inbox.push(post);
                }
            } else if (data.type == ApiObjectType.follow) {
                const followRequest = SocialApiTransform.followRequestDataTransform(data);
                if (followRequest) {
                    this.inbox.push(followRequest);
                }
            }
        }
    }
}