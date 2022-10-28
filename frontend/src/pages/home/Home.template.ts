import { icon } from "@fortawesome/fontawesome-svg-core";
import { html, ref, repeat, when } from "@microsoft/fast-element";
import { socialSearch } from "../../components/social-search";
import { Post } from "../../libs/api-service/SocialApiModel";
import { LayoutHelpers } from "../../libs/core/Helpers";
import { FeedType } from "../../libs/core/PageModel";
import { feedPost } from "../../components/feed-post";
import { Home } from "./Home";
import { layoutComponent } from "../../components/base-layout";

feedPost;
layoutComponent;

export const HomePageTemplate = html<Home>`
    <page-layout
        :userId="${x => x.userId}"
        :user="${x => x.user}"
        :layoutType="${x => x.layoutType}"
        :layoutStyleClass="${x => LayoutHelpers.getLayoutStyle(x.layoutType)}">
        <div class="tab-container">
            <button @click="${x => x.changeFeed(FeedType.All)}" class="tab ${x => x.getFeedTypeStyles(FeedType.All)}">
                All Feed
            </button>
            ${when(x => x.user, html<Home>`
                <button @click="${x => x.changeFeed(FeedType.Stream)}" class="tab ${x => x.getFeedTypeStyles(FeedType.Stream)}">
                    My Feed
                </button>
                <a href="/create-post/" class="create-a-post">
                    <div class="create-post-icon" :innerHTML="${_ => icon({prefix: "fas", iconName: "pencil"}).html}"></div>
                    Create a Post
                </a>
            `)}
        </div>
        <div class="post-container">
            ${repeat(x => x.visibilePosts, html<Post>`
                <feed-post
                    :post=${x => x}>
                </feed-post>
            `)
            }
        </div>
        <div ${ref("loadMore")} class="loading"></div>
    </page-layout>
`;