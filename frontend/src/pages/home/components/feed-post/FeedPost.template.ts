import { html } from "@microsoft/fast-element";
import { FeedPost } from "./FeedPost";

export const FeedPostTemplate = html<FeedPost>`
    <a href="${x => x.getPostUrl()}">
        <article class="post">
            <h3>${x => x.post?.title}</h3>
            <h4>${x => x.post?.author?.displayName} | ${x => new Date(x.post?.published || new Date()).toLocaleDateString()}
            <p>${x => x.post?.description}</p>
        </article>
    </a>
`;