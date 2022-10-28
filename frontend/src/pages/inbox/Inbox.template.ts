import { html, ref, repeat, when } from "@microsoft/fast-element";
import { feedPost } from "../../components/feed-post";
import { followerComponent } from "../../components/follower-component";
import { FollowRequest, Post } from "../../libs/api-service/SocialApiModel";
import { LayoutHelpers } from "../../libs/core/Helpers";
import { Inbox } from "./Inbox";

feedPost;
followerComponent;

export const InboxPageTemplate = html<Inbox>`
    <page-layout
        :userId="${x => x.userId}"
        :user="${x => x.user}"
        :layoutType="${x => x.layoutType}"
        :layoutStyleClass="${x => LayoutHelpers.getLayoutStyle(x.layoutType)}">
        <h1>Inbox</h1>
        <div class="inbox-container">
            ${repeat(x => x.inbox, html`
                ${when(x => x instanceof Post, html<Post>`
                    <feed-post
                        :post=${x => x}>
                    </feed-post>
                `)}
                ${when(x => x instanceof FollowRequest, html<FollowRequest>`
                    <follower-component
                        :profile=${x => x.sender}
                        :user=${(_, c) => c.parent.user}
                        :request=${_ => true}>
                    </follower-component>
                `)}
            `)}
            <div ${ref("loadMore")} class="loading"></div>
        </div>
    </page-layout>
`;