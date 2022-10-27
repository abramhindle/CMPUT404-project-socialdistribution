import { observable } from "@microsoft/fast-element";
import { SocialApi } from "../../libs/api-service/SocialApi";
import { PaginatedResponse, Post } from "../../libs/api-service/SocialApiModel";
import { SocialApiTransform } from "../../libs/api-service/SocialApiTransform";
import { FeedType } from "../../libs/core/PageModel";
import { Page } from "../Page";

const PAGE_SIZE = 10;

export class Home extends Page {
    @observable
    public visibilePosts: Post[] = [];

    public loadMore?: HTMLElement;

    private observer?: IntersectionObserver;

    @observable
    public paginatedResponse?: PaginatedResponse | null;

    @observable
    public feedType: FeedType = FeedType.All;

    constructor() {
        super();

        this.observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.getPosts();
                }
            })
        })

        this.getPosts()
    }

    public changeFeed(feedType: FeedType) {
        this.feedType = feedType;
        this.visibilePosts.splice(0, this.visibilePosts.length);
        this.paginatedResponse = null;
        this.observer?.disconnect();
        this.getPosts();
    }

    public getFeedTypeStyles(feedType: FeedType) {
        if (this.feedType == feedType) {
            return "tab-active";
        }
        return "";
    }

    private async getPosts() {
        const homePage = this;
        try {
            let responseData: PaginatedResponse | null;

            if (homePage.paginatedResponse?.next) {
                responseData = await SocialApi.fetchPaginatedPublicPostsNext(homePage.paginatedResponse.next);
                console.log(responseData)
                if (responseData) {
                    homePage.paginatedResponse = responseData;
                    homePage.setVisiblePosts()
                }
            } else if (!homePage.paginatedResponse) {
                responseData = await SocialApi.fetchPaginatedPublicPosts(1, PAGE_SIZE);
                console.log(responseData)
                if (responseData) {
                    homePage.paginatedResponse = responseData;
                    homePage.setVisiblePosts()
                    if (this.loadMore) {
                        this.observer?.observe(this.loadMore);
                    }
                }
            } else {
                responseData = homePage.paginatedResponse || null;
            }
        } catch (e) {
            console.error("Public post fetch failed", e);
        }
    }

    private setVisiblePosts() {
        if (!this.paginatedResponse?.results) {
            return;
        }

        for (var postData of this.paginatedResponse?.results) {
            const post = SocialApiTransform.postDataTransform(postData);
            if (post) {
                this.visibilePosts.push(post);
            }
        }
    }
}