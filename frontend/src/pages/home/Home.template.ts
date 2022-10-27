import { html, ref, repeat } from "@microsoft/fast-element";
import { socialSearch } from "../../components/social-search";
import { Post } from "../../libs/api-service/SocialApiModel";
import { LayoutHelpers } from "../../libs/core/Helpers";
import { FeedType } from "../../libs/core/PageModel";
import { feedPost } from "./components/feed-post";
import { homeNavigation } from "./components/home-navigation";
import { Home } from "./Home";

homeNavigation;
feedPost;
socialSearch;

const navigationTemplate = html<Home>`
    <home-navigation
        :user=${x => x.user}
        :layoutType=${x => x.layoutType}
        :layoutStyleClass=${x => LayoutHelpers.getLayoutStyle(x.layoutType)}
        :className="${x => LayoutHelpers.getLayoutStyle(x.layoutType)}">
    </home-navigation>
`;

export const HomePageTemplate = html<Home>`
    ${navigationTemplate}
    <main class="feed-container ${x => LayoutHelpers.getLayoutStyle(x.layoutType)}">
        <div class="main-feed ${x => LayoutHelpers.getLayoutStyle(x.layoutType)}">
            <social-search>
            </social-search>
            <div class="tab-container">
                <button @click="${x => x.changeFeed(FeedType.All)}" class="tab ${x => x.getFeedTypeStyles(FeedType.All)}">
                    All Feed
                </button>
                <button @click="${x => x.changeFeed(FeedType.Stream)}" class="tab ${x => x.getFeedTypeStyles(FeedType.Stream)}">
                    My Feed
                </button>
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
        </div>
        <div class="psa-feed ${x => LayoutHelpers.getLayoutStyle(x.layoutType)}">
        </div>
    </main>
`;